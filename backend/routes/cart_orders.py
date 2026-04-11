from flask import Blueprint, jsonify, request
from models import db, Order, OrderItem, Cart, CartItem, ProductVariant, DiscountCode, User

cart_orders_bp = Blueprint('cart_orders', __name__)

@cart_orders_bp.route('/cart/add', methods=['POST'])
def add_to_cart():
    data = request.json
    whatsapp_number = data.get('whatsapp_number')
    variant_id = data.get('variant_id')
    quantity = data.get('quantity', 1)
    
    # Require WhatsApp signup for cart parsing as per requirements
    if not whatsapp_number:
        return jsonify({"error": "WhatsApp number is required to add items to the cart"}), 401
    
    user = User.query.filter_by(whatsapp_number=whatsapp_number).first()
    if not user:
        user = User(whatsapp_number=whatsapp_number)
        db.session.add(user)
        db.session.commit()
        
    variant = ProductVariant.query.get(variant_id)
    if not variant or variant.quantity < quantity:
        return jsonify({"error": "Insufficient stock"}), 400
        
    cart = Cart.query.filter_by(user_id=user.id).first()
    if not cart:
        cart = Cart(user_id=user.id)
        db.session.add(cart)
        db.session.commit()
    
    cart_item = CartItem.query.filter_by(cart_id=cart.id, variant_id=variant_id).first()
    if cart_item:
        cart_item.quantity += quantity
    else:
        cart_item = CartItem(cart_id=cart.id, variant_id=variant_id, quantity=quantity)
        db.session.add(cart_item)
        
    db.session.commit()
    return jsonify({"message": "Added to cart", "cart_id": cart.id})

@cart_orders_bp.route('/cart/apply_discount', methods=['POST'])
def apply_discount():
    data = request.json
    code = data.get('code')
    cart_total = data.get('cart_total', 0)
    
    discount = DiscountCode.query.filter_by(code=code, is_active=True).first()
    if not discount:
        return jsonify({"error": "Invalid or expired discount code"}), 400
        
    if discount.min_cart_value and cart_total < discount.min_cart_value:
        return jsonify({"error": f"Minimum cart value of {discount.min_cart_value} required"}), 400
        
    return jsonify({
        "message": "Discount applied",
        "discount_percentage": discount.discount_percentage,
        "discount_flat": discount.discount_flat
    })

@cart_orders_bp.route('/track/<tracking_number>', methods=['GET'])
def track_order(tracking_number):
    order = Order.query.filter_by(tracking_number=tracking_number).first_or_404()
    return jsonify({"status": order.status, "tracking_number": order.tracking_number})
