import jwt
import datetime
from flask import Blueprint, jsonify, request, current_app
from models import db, User

auth_bp = Blueprint('auth', __name__)

DEMO_OTP = "1234"  # Hardcoded for presentation — replace with real WhatsApp OTP later


@auth_bp.route('/send-otp', methods=['POST'])
def send_otp():
    data = request.get_json(silent=True) or {}
    whatsapp_number = data.get('whatsapp_number', '').strip()

    if not whatsapp_number or len(whatsapp_number) != 10:
        return jsonify({"error": "Valid 10-digit WhatsApp number is required"}), 400

    # Create user if not exists
    user = User.query.filter_by(whatsapp_number=whatsapp_number).first()
    if not user:
        user = User(whatsapp_number=whatsapp_number)
        db.session.add(user)
        db.session.commit()

    # TODO: Send real OTP via WhatsApp Business API here
    # For now, OTP is hardcoded as "1234" for demo

    return jsonify({"message": "OTP sent successfully", "user_id": user.id})


@auth_bp.route('/verify-otp', methods=['POST'])
def verify_otp():
    data = request.get_json(silent=True) or {}
    whatsapp_number = data.get('whatsapp_number', '').strip()
    otp = data.get('otp', '').strip()

    if not whatsapp_number or not otp:
        return jsonify({"error": "whatsapp_number and otp are required"}), 400

    if otp != DEMO_OTP:
        return jsonify({"error": "Invalid OTP. Please try again."}), 401

    user = User.query.filter_by(whatsapp_number=whatsapp_number).first()
    if not user:
        return jsonify({"error": "User not found. Please request OTP again."}), 404

    # Generate JWT token
    token = jwt.encode(
        {
            "user_id": user.id,
            "whatsapp_number": whatsapp_number,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(days=30)
        },
        current_app.config["SECRET_KEY"],
        algorithm="HS256"
    )

    return jsonify({
        "message": "Login successful",
        "token": token,
        "user_id": user.id,
        "whatsapp_number": whatsapp_number
    })


# Keep old route for backward compatibility
@auth_bp.route('/whatsapp-login', methods=['POST'])
def whatsapp_login():
    data = request.get_json(silent=True) or {}
    whatsapp_number = data.get('whatsapp_number', '').strip()

    if not whatsapp_number:
        return jsonify({"error": "WhatsApp number is required"}), 400

    user = User.query.filter_by(whatsapp_number=whatsapp_number).first()
    if not user:
        user = User(whatsapp_number=whatsapp_number)
        db.session.add(user)
        db.session.commit()

    return jsonify({"message": "Login successful", "user_id": user.id})
