"""
Wishlist API routes for M&M Fashion.
Syncs wishlist to the database so it persists across devices and sessions.
"""
from flask import Blueprint, jsonify, request
from models import db, Wishlist, Product, User

wishlist_bp = Blueprint('wishlist', __name__)


def _get_user(whatsapp_number: str):
    """Return user by whatsapp_number or None."""
    return User.query.filter_by(whatsapp_number=whatsapp_number.strip()).first()


# ── GET /api/wishlist?whatsapp_number=XXXXXXXXXX ──────────────────────────────
@wishlist_bp.route('/wishlist', methods=['GET'])
def get_wishlist():
    """Return all wishlist products for a user."""
    wa = request.args.get('whatsapp_number', '').strip()
    if not wa:
        return jsonify({"error": "whatsapp_number is required"}), 400

    user = _get_user(wa)
    if not user:
        return jsonify([])

    items = Wishlist.query.filter_by(user_id=user.id).all()
    result = []
    for w in items:
        p = Product.query.get(w.product_id)
        if not p:
            continue
        result.append({
            "wishlist_id": w.id,
            "id": p.id,
            "name": p.name,
            "image_url": p.image_url,
            "category": p.category,
        })
    return jsonify(result)


# ── POST /api/wishlist ────────────────────────────────────────────────────────
@wishlist_bp.route('/wishlist', methods=['POST'])
def add_to_wishlist():
    """Add a product to the user's wishlist. Idempotent — no duplicates."""
    data = request.get_json(silent=True) or {}
    wa = data.get('whatsapp_number', '').strip()
    product_id = data.get('product_id')

    if not wa:
        return jsonify({"error": "whatsapp_number is required"}), 400
    if not product_id:
        return jsonify({"error": "product_id is required"}), 400

    user = _get_user(wa)
    if not user:
        return jsonify({"error": "User not found"}), 404

    if not Product.query.get(product_id):
        return jsonify({"error": "Product not found"}), 404

    # Idempotent — skip if already in wishlist
    existing = Wishlist.query.filter_by(user_id=user.id, product_id=product_id).first()
    if existing:
        return jsonify({"message": "Already in wishlist", "wishlist_id": existing.id}), 200

    entry = Wishlist(user_id=user.id, product_id=product_id)
    db.session.add(entry)
    db.session.commit()
    return jsonify({"message": "Added to wishlist", "wishlist_id": entry.id}), 201


# ── DELETE /api/wishlist/<product_id> ─────────────────────────────────────────
@wishlist_bp.route('/wishlist/<int:product_id>', methods=['DELETE'])
def remove_from_wishlist(product_id):
    """Remove a product from the user's wishlist."""
    wa = request.args.get('whatsapp_number', '').strip()
    if not wa:
        # Also accept from JSON body
        data = request.get_json(silent=True) or {}
        wa = data.get('whatsapp_number', '').strip()

    if not wa:
        return jsonify({"error": "whatsapp_number is required"}), 400

    user = _get_user(wa)
    if not user:
        return jsonify({"error": "User not found"}), 404

    entry = Wishlist.query.filter_by(user_id=user.id, product_id=product_id).first()
    if entry:
        db.session.delete(entry)
        db.session.commit()

    return jsonify({"message": "Removed from wishlist"}), 200
