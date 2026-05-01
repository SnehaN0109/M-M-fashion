from flask import Blueprint, jsonify, request
from models import db, Order, OrderItem, Cart, CartItem, ProductVariant, DiscountCode, User

cart_orders_bp = Blueprint('cart_orders', __name__)


def _get_or_create_cart(whatsapp_number):
    """Helper: get or create cart for a user by whatsapp number."""
    user = User.query.filter_by(whatsapp_number=whatsapp_number).first()
    if not user:
        user = User(whatsapp_number=whatsapp_number)
        db.session.add(user)
        db.session.flush()
    cart = Cart.query.filter_by(user_id=user.id).first()
    if not cart:
        cart = Cart(user_id=user.id)
        db.session.add(cart)
        db.session.flush()
    return user, cart


@cart_orders_bp.route('/cart', methods=['GET'])
def get_cart():
    """Return all cart items for a user with full product/variant details."""
    whatsapp_number = request.args.get('whatsapp_number', '').strip()
    if not whatsapp_number:
        return jsonify({"error": "whatsapp_number is required"}), 400

    user = User.query.filter_by(whatsapp_number=whatsapp_number).first()
    if not user:
        return jsonify([])

    cart = Cart.query.filter_by(user_id=user.id).first()
    if not cart:
        return jsonify([])

    result = []
    for ci in cart.items:
        v = ProductVariant.query.get(ci.variant_id)
        if not v:
            continue
        p = v.product
        result.append({
            "cart_item_id": ci.id,
            "variant_id": v.id,
            "product_id": p.id,
            "name": p.name,
            "image_url": p.image_url,
            "category": p.category,
            "color": v.color,
            "size": v.size,
            "quantity": ci.quantity,
            "stock": v.quantity,
            "price_b2c": float(v.price_b2c or 0),
            "price_b2b_ttd": float(v.price_b2b_ttd or 0),
            "price_b2b_maharashtra": float(v.price_b2b_maharashtra or 0),
        })
    return jsonify(result)


@cart_orders_bp.route('/cart/add', methods=['POST'])
def add_to_cart():
    data = request.get_json(silent=True) or {}
    whatsapp_number = data.get('whatsapp_number', '').strip()
    variant_id = data.get('variant_id')
    quantity = int(data.get('quantity', 1))

    if not whatsapp_number:
        return jsonify({"error": "whatsapp_number is required"}), 401
    if not variant_id:
        return jsonify({"error": "variant_id is required"}), 400

    variant = ProductVariant.query.get(variant_id)
    if not variant:
        return jsonify({"error": "Variant not found"}), 404
    if variant.quantity < quantity:
        return jsonify({"error": "Insufficient stock"}), 400

    user, cart = _get_or_create_cart(whatsapp_number)

    cart_item = CartItem.query.filter_by(cart_id=cart.id, variant_id=variant_id).first()
    if cart_item:
        cart_item.quantity += quantity
    else:
        cart_item = CartItem(cart_id=cart.id, variant_id=variant_id, quantity=quantity)
        db.session.add(cart_item)

    db.session.commit()
    return jsonify({"message": "Added to cart", "cart_item_id": cart_item.id})


@cart_orders_bp.route('/cart/remove', methods=['DELETE'])
def remove_from_cart():
    data = request.get_json(silent=True) or {}
    whatsapp_number = data.get('whatsapp_number', '').strip()
    variant_id = data.get('variant_id')

    if not whatsapp_number or not variant_id:
        return jsonify({"error": "whatsapp_number and variant_id are required"}), 400

    user = User.query.filter_by(whatsapp_number=whatsapp_number).first()
    if not user:
        return jsonify({"error": "User not found"}), 404

    cart = Cart.query.filter_by(user_id=user.id).first()
    if not cart:
        return jsonify({"error": "Cart not found"}), 404

    cart_item = CartItem.query.filter_by(cart_id=cart.id, variant_id=variant_id).first()
    if cart_item:
        db.session.delete(cart_item)
        db.session.commit()

    return jsonify({"message": "Item removed"})


@cart_orders_bp.route('/cart/update', methods=['PUT'])
def update_cart_quantity():
    """Update the quantity of a cart item — syncs frontend changes to database."""
    data = request.get_json(silent=True) or {}
    whatsapp_number = data.get('whatsapp_number', '').strip()
    variant_id = data.get('variant_id')
    new_quantity = data.get('quantity')

    # Validation
    if not whatsapp_number:
        return jsonify({"error": "whatsapp_number is required"}), 401
    if not variant_id:
        return jsonify({"error": "variant_id is required"}), 400
    if new_quantity is None or new_quantity < 1:
        return jsonify({"error": "quantity must be at least 1"}), 400

    # Get user and cart
    user = User.query.filter_by(whatsapp_number=whatsapp_number).first()
    if not user:
        return jsonify({"error": "User not found"}), 404

    cart = Cart.query.filter_by(user_id=user.id).first()
    if not cart:
        return jsonify({"error": "Cart not found"}), 404

    # Find cart item
    cart_item = CartItem.query.filter_by(cart_id=cart.id, variant_id=variant_id).first()
    if not cart_item:
        return jsonify({"error": "Item not found in cart"}), 404

    # Check stock availability
    variant = ProductVariant.query.get(variant_id)
    if not variant:
        return jsonify({"error": "Product variant not found"}), 404
    
    if variant.quantity < new_quantity:
        return jsonify({
            "error": f"Only {variant.quantity} items available in stock",
            "available_stock": variant.quantity
        }), 400

    # Update quantity
    cart_item.quantity = new_quantity
    db.session.commit()

    return jsonify({
        "message": "Cart updated successfully",
        "cart_item_id": cart_item.id,
        "variant_id": variant_id,
        "new_quantity": new_quantity
    })


@cart_orders_bp.route('/cart/clear', methods=['DELETE'])
def clear_cart():
    """Delete all cart items for a user — called after order is placed."""
    data = request.get_json(silent=True) or {}
    whatsapp_number = data.get('whatsapp_number', '').strip()

    if not whatsapp_number:
        return jsonify({"error": "whatsapp_number is required"}), 400

    user = User.query.filter_by(whatsapp_number=whatsapp_number).first()
    if not user:
        return jsonify({"message": "No cart to clear"})

    cart = Cart.query.filter_by(user_id=user.id).first()
    if cart:
        CartItem.query.filter_by(cart_id=cart.id).delete()
        db.session.commit()

    return jsonify({"message": "Cart cleared"})


@cart_orders_bp.route('/cart/apply_discount', methods=['POST'])
def apply_discount():
    data = request.get_json(silent=True) or {}
    code = data.get('code', '').strip().upper()
    cart_total = data.get('cart_total', 0)

    if not code:
        return jsonify({"error": "code is required"}), 400

    discount = DiscountCode.query.filter_by(code=code, is_active=True).first()
    if not discount:
        return jsonify({"error": "Invalid or expired discount code"}), 400

    if discount.min_cart_value and cart_total < discount.min_cart_value:
        return jsonify({"error": f"Minimum cart value of ₹{discount.min_cart_value} required"}), 400

    return jsonify({
        "message": "Discount applied",
        "discount_percentage": float(discount.discount_percentage) if discount.discount_percentage else None,
        "discount_flat": float(discount.discount_flat) if discount.discount_flat else None
    })

@cart_orders_bp.route('/track/<string:identifier>', methods=['GET'])
def track_by_identifier(identifier):
    """Smart route: accepts either a numeric order ID or a tracking number string."""
    if identifier.isdigit():
        order = Order.query.get(int(identifier))
    else:
        order = Order.query.filter_by(tracking_number=identifier).first()
    if not order:
        return jsonify({"error": "Order not found"}), 404
    return jsonify({"status": order.status, "tracking_number": order.tracking_number, "order_id": order.id})
