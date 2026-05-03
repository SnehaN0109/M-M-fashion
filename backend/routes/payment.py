"""
Payment system routes for M&M Fashion.
Handles payment proof uploads and admin verification.
"""
import os
import uuid
from flask import Blueprint, jsonify, request, current_app
from werkzeug.utils import secure_filename
from functools import wraps
import jwt as pyjwt
from models import db, Order
from utils import assign_tracking_number

payment_bp = Blueprint('payment', __name__)

# ─── Configuration ────────────────────────────────────────────────────────────
PAYMENT_PROOF_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'uploads', 'payment_proofs')
PAYMENT_PROOF_FOLDER = os.path.normpath(PAYMENT_PROOF_FOLDER)
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'pdf', 'webp'}

def allowed_file(filename):
    """Check if file extension is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def save_payment_proof(file):
    """Save uploaded payment proof and return the file path."""
    os.makedirs(PAYMENT_PROOF_FOLDER, exist_ok=True)
    
    # Generate unique filename
    ext = file.filename.rsplit('.', 1)[1].lower()
    filename = f"{uuid.uuid4().hex}.{ext}"
    filepath = os.path.join(PAYMENT_PROOF_FOLDER, filename)
    
    # Save file
    file.save(filepath)
    
    # Return relative URL path
    return f"/uploads/payment_proofs/{filename}"


# ─── Admin Authentication Decorator ───────────────────────────────────────────

def admin_required(f):
    """Verify JWT admin token on protected admin routes."""
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization', '')
        if not auth_header.startswith('Bearer '):
            return jsonify({"error": "Missing or invalid Authorization header"}), 401
        
        token = auth_header.split(' ', 1)[1]
        try:
            payload = pyjwt.decode(
                token,
                current_app.config['SECRET_KEY'],
                algorithms=['HS256']
            )
            if payload.get('role') != 'admin':
                return jsonify({"error": "Admin access required"}), 403
        except pyjwt.ExpiredSignatureError:
            return jsonify({"error": "Session expired. Please log in again."}), 401
        except pyjwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401
        
        return f(*args, **kwargs)
    return decorated


# ═══════════════════════════════════════════════════════════════════════════════
# USER APIs - Payment Proof Upload
# ═══════════════════════════════════════════════════════════════════════════════

@payment_bp.route('/api/orders/<int:order_id>/mark-paid', methods=['POST'])
def mark_order_paid(order_id):
    """
    User uploads payment proof for an order.
    
    Request:
        - Form data with optional 'payment_proof' file
        - Optional 'whatsapp_number' for verification
    
    Response:
        - Success message with order details
        - Payment status remains PENDING (awaiting admin verification)
    """
    # Get order
    order = Order.query.get_or_404(order_id)
    
    # Optional: Verify user owns this order (only if whatsapp_number is provided)
    whatsapp = request.form.get('whatsapp_number', '').strip()
    if whatsapp:
        if order.user:
            # Registered user: check linked user's whatsapp
            if order.user.whatsapp_number != whatsapp:
                return jsonify({"error": "Unauthorized: This order does not belong to you"}), 403
        else:
            # Guest order: check customer phone
            if order.customer_phone != whatsapp:
                return jsonify({"error": "Unauthorized: Phone number does not match order"}), 403
    
    # Check if order is in correct state
    if order.payment_status == 'VERIFIED':
        return jsonify({"error": "Payment already verified for this order"}), 400

    # Block re-upload if proof already submitted (with or without file)
    if order.payment_proof:
        return jsonify({"error": "Payment proof already submitted. Awaiting admin verification."}), 400

    # Handle file upload
    payment_proof_url = None
    if 'payment_proof' in request.files:
        file = request.files['payment_proof']

        if file and file.filename:
            if not allowed_file(file.filename):
                return jsonify({
                    "error": "Invalid file type. Allowed: jpg, jpeg, png, pdf, webp"
                }), 400

            try:
                payment_proof_url = save_payment_proof(file)
            except Exception as e:
                return jsonify({"error": f"Failed to save file: {str(e)}"}), 500

    # Mark as submitted — use uploaded path if file provided, else sentinel value
    # This ensures re-upload is blocked even when no file was attached
    order.payment_proof = payment_proof_url if payment_proof_url else "submitted"
    
    # Keep payment_status as PENDING (awaiting admin verification)
    # Do NOT change order status yet
    
    db.session.commit()
    
    return jsonify({
        "message": "Payment proof uploaded successfully. Awaiting admin verification.",
        "order_id": order.id,
        "payment_status": order.payment_status,
        "payment_proof": order.payment_proof,
        "status": order.status
    }), 200


# ═══════════════════════════════════════════════════════════════════════════════
# ADMIN APIs - Payment Verification
# ═══════════════════════════════════════════════════════════════════════════════

@payment_bp.route('/api/admin/orders/<int:order_id>/payment-action', methods=['POST'])
@admin_required
def admin_payment_action(order_id):
    """
    Admin verifies or rejects payment.
    
    Request Body:
        {
            "action": "verify" | "reject",
            "reason": "Optional rejection reason"
        }
    
    Actions:
        - verify: Set payment_status=VERIFIED, order status=PLACED
        - reject: Set payment_status=FAILED, keep order status
    """
    order = Order.query.get_or_404(order_id)
    
    data = request.get_json(silent=True) or {}
    action = data.get('action', '').lower()
    reason = data.get('reason', '').strip()
    
    if action not in ['verify', 'reject']:
        return jsonify({"error": "Invalid action. Must be 'verify' or 'reject'"}), 400
    
    if action == 'verify':
        order.payment_status = 'VERIFIED'

        # Move order to PLACED status (ready for fulfillment)
        if order.status == 'PENDING_PAYMENT':
            order.status = 'PLACED'

        # Generate tracking number now that payment is confirmed
        assign_tracking_number(order, db.session)

        db.session.commit()

        return jsonify({
            "message": "Payment verified successfully",
            "order_id": order.id,
            "payment_status": order.payment_status,
            "status": order.status,
            "tracking_number": order.tracking_number,
        }), 200
    
    elif action == 'reject':
        # Reject payment
        order.payment_status = 'FAILED'
        
        # Optionally store rejection reason (would need a new field in model)
        # For now, we just set status to FAILED
        
        db.session.commit()
        
        return jsonify({
            "message": "Payment rejected",
            "order_id": order.id,
            "payment_status": order.payment_status,
            "status": order.status,
            "reason": reason if reason else None
        }), 200


@payment_bp.route('/api/admin/payment-proof/<int:order_id>', methods=['GET'])
@admin_required
def get_payment_proof(order_id):
    """
    Admin retrieves payment proof URL for an order.
    
    Response:
        {
            "order_id": 123,
            "payment_proof": "/uploads/payment_proofs/abc123.jpg",
            "payment_status": "PENDING",
            "customer_name": "John Doe",
            "total_amount": 1499.0
        }
    """
    order = Order.query.get_or_404(order_id)
    
    return jsonify({
        "order_id": order.id,
        "payment_proof": order.payment_proof,
        "payment_status": order.payment_status,
        "payment_method": order.payment_method,
        "customer_name": order.customer_name,
        "customer_email": order.customer_email,
        "customer_phone": order.customer_phone,
        "total_amount": float(order.total_amount),
        "created_at": order.created_at.isoformat() if order.created_at else None
    }), 200


# ═══════════════════════════════════════════════════════════════════════════════
# UTILITY APIs
# ═══════════════════════════════════════════════════════════════════════════════

@payment_bp.route('/api/orders/<int:order_id>/payment-status', methods=['GET'])
def get_payment_status(order_id):
    """
    Public endpoint to check payment status of an order.
    
    Query params:
        - whatsapp_number: Optional verification
    
    Response:
        {
            "order_id": 123,
            "payment_status": "PENDING",
            "payment_method": "UPI",
            "has_payment_proof": true
        }
    """
    order = Order.query.get_or_404(order_id)
    
    # Optional: Verify user owns this order
    whatsapp = request.args.get('whatsapp_number', '').strip()
    if whatsapp:
        if order.user and order.user.whatsapp_number != whatsapp:
            return jsonify({"error": "Unauthorized"}), 403
        elif order.customer_phone != whatsapp:
            return jsonify({"error": "Unauthorized"}), 403
    
    return jsonify({
        "order_id": order.id,
        "payment_status": order.payment_status,
        "payment_method": order.payment_method,
        "has_payment_proof": bool(order.payment_proof),
        "status": order.status
    }), 200
