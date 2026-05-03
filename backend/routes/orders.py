from flask import Blueprint, jsonify, request
from models import db, Order, OrderItem, ProductVariant, DiscountCode, User
from utils import resolve_price_key, is_b2b_domain, assign_tracking_number
from whatsapp_service import send_order_confirmation

orders_bp = Blueprint('orders', __name__)


# ─── Checkout ────────────────────────────────────────────────────────────────

@orders_bp.route('/checkout', methods=['POST'])
def checkout():
    data = request.get_json(silent=True) or {}

    # Validate required fields
    required = ['customer_name', 'customer_email', 'customer_phone',
                'address_line1', 'city', 'state', 'pincode', 'items', 'domain']
    for field in required:
        if not data.get(field):
            return jsonify({"error": f"{field} is required"}), 400

    items = data.get('items', [])
    if not items:
        return jsonify({"error": "Cart is empty"}), 400

    domain = data.get('domain', 'garba.shop')
    b2b = is_b2b_domain(domain)

    # ── Role check: B2B domains require WHOLESALER role ──────────────────────
    # If user is not a wholesaler, silently fall back to B2C pricing (safe degradation)
    effective_domain = domain
    whatsapp = data.get('whatsapp_number', '').strip()
    if b2b and whatsapp:
        user_check = User.query.filter_by(whatsapp_number=whatsapp).first()
        if not user_check or user_check.role != 'WHOLESALER':
            # Non-wholesaler attempting B2B domain — fall back to B2C pricing
            effective_domain = 'garba.shop'
            b2b = False

    # Resolve price_key server-side from effective domain — never trust client-provided price_key
    price_key = resolve_price_key(effective_domain)

    def get_price(variant):
        return float(getattr(variant, price_key) or 0)

    # Calculate subtotal and validate stock
    subtotal = 0.0
    order_items_data = []

    for item in items:
        variant_id = item.get('variant_id')
        if not variant_id:
            return jsonify({"error": "One or more cart items is missing a variant. Please re-add items to cart."}), 400
        # with_for_update() acquires a row-level lock so concurrent checkouts
        # are serialised — prevents overselling when two requests race.
        variant = ProductVariant.query.with_for_update().get(variant_id)
        if not variant:
            return jsonify({"error": f"Variant {variant_id} not found. It may have been removed."}), 400

        qty = item.get('quantity', 1)

        # ── Stock check ───────────────────────────────────────────────────────
        if variant.quantity < qty:
            return jsonify({"error": f"Only {variant.quantity} units available for a selected item."}), 400

        # ── MOQ check (B2B only) ──────────────────────────────────────────────
        if b2b and variant.moq_b2b and qty < variant.moq_b2b:
            return jsonify({
                "error": f"Minimum order quantity is {variant.moq_b2b} units for this item."
            }), 400

        # ── Price safety check ────────────────────────────────────────────────
        price = get_price(variant)
        if price is None or price <= 0:
            return jsonify({
                "error": "Invalid price configuration for one or more items. Please contact support."
            }), 400

        subtotal += price * qty
        order_items_data.append({
            "variant": variant,
            "quantity": qty,
            "price": price
        })

    # Apply discount code if provided
    discount_amount = 0.0
    discount_code_used = None
    code_str = data.get('discount_code', '').strip().upper()
    if code_str:
        code = DiscountCode.query.filter_by(code=code_str, is_active=True).first()
        if code:
            if subtotal >= (code.min_cart_value or 0):
                if code.discount_flat:
                    discount_amount = float(code.discount_flat)
                elif code.discount_percentage:
                    discount_amount = round(subtotal * float(code.discount_percentage) / 100, 2)
                discount_code_used = code_str

    # ── Shipping: B2B always free; B2C free above ₹999 ───────────────────────
    if b2b:
        shipping_charge = 0.0
    else:
        shipping_charge = 0.0 if subtotal >= 999 else 99.0

    total_amount = subtotal - discount_amount + shipping_charge

    # Create order
    order = Order(
        customer_name=data['customer_name'],
        customer_email=data['customer_email'],
        customer_phone=data['customer_phone'],
        address_line1=data['address_line1'],
        address_line2=data.get('address_line2', ''),
        city=data['city'],
        state=data['state'],
        pincode=data['pincode'],
        subtotal=subtotal,
        discount_amount=discount_amount,
        discount_code=discount_code_used,
        shipping_charge=shipping_charge,
        tax_amount=0.0,
        total_amount=total_amount,
        domain_origin=domain,
        payment_method=data.get('payment_method', 'UPI'),
        status='PENDING_PAYMENT',
        payment_status='PENDING',
        # B2B optional fields
        business_name=data.get('business_name') if b2b else None,
        gst_number=data.get('gst_number') if b2b else None,
    )

    # Link to user if whatsapp number provided
    if whatsapp:
        user = User.query.filter_by(whatsapp_number=whatsapp).first()
        if user:
            order.user_id = user.id

    db.session.add(order)
    db.session.flush()  # get order.id

    # Create order items and deduct stock
    for item_data in order_items_data:
        oi = OrderItem(
            order_id=order.id,
            variant_id=item_data['variant'].id,
            quantity=item_data['quantity'],
            price_at_purchase=item_data['price']
        )
        db.session.add(oi)
        # Deduct stock
        item_data['variant'].quantity -= item_data['quantity']

    # ── Auto-generate tracking number at order creation ───────────────────────
    # Assigned immediately so it's available in the WhatsApp message and
    # on the success page — admin never needs to enter it manually.
    assign_tracking_number(order, db.session)

    db.session.commit()

    # ── Send WhatsApp order confirmation (fire-and-forget, never blocks order) ─
    try:
        send_order_confirmation(order)
    except Exception:
        pass  # WhatsApp failure must never fail the order

    return jsonify({
        "message": "Order placed successfully",
        "order_id": order.id,
        "total_amount": total_amount,
        "status": order.status,
        "payment_status": order.payment_status,
        "payment_method": order.payment_method,
        "tracking_number": order.tracking_number,
    }), 201


# ─── Track Order ─────────────────────────────────────────────────────────────

@orders_bp.route('/track/<int:order_id>', methods=['GET'])
def track_order(order_id):
    o = Order.query.get_or_404(order_id)
    
    # Get full item details with product info
    items_detail = []
    for item in o.items:
        variant = ProductVariant.query.get(item.variant_id)
        if variant and variant.product:
            items_detail.append({
                "variant_id": item.variant_id,
                "product_id": variant.product.id,
                "product_name": variant.product.name,
                "image_url": variant.product.image_url,
                "color": variant.color,
                "size": variant.size,
                "quantity": item.quantity,
                "price_at_purchase": float(item.price_at_purchase)
            })
    
    return jsonify({
        "order_id": o.id,
        "status": o.status,
        "payment_status": o.payment_status,
        "payment_proof": o.payment_proof,
        "tracking_number": o.tracking_number,
        "customer_name": o.customer_name,
        "customer_email": o.customer_email,
        "customer_phone": o.customer_phone,
        "address": {
            "line1": o.address_line1,
            "line2": o.address_line2,
            "city": o.city,
            "state": o.state,
            "pincode": o.pincode
        },
        "subtotal": float(o.subtotal),
        "discount_amount": float(o.discount_amount),
        "discount_code": o.discount_code,
        "shipping_charge": float(o.shipping_charge),
        "total_amount": float(o.total_amount),
        "payment_method": o.payment_method,
        "created_at": o.created_at.isoformat(),
        "items": items_detail
    })


# ─── WhatsApp Notify (manual retry) ─────────────────────────────────────────

@orders_bp.route('/<int:order_id>/notify-whatsapp', methods=['POST'])
def notify_whatsapp(order_id):
    """
    Manually trigger a WhatsApp order confirmation.
    Useful for retrying failed sends or testing without re-placing an order.
    Always returns 200 — WhatsApp failure is non-critical.
    """
    order = Order.query.get_or_404(order_id)
    result = send_order_confirmation(order)
    if result["success"]:
        return jsonify({"message": "WhatsApp notification sent", "order_id": order_id}), 200
    return jsonify({
        "message": "WhatsApp notification failed (order not affected)",
        "detail": result["detail"],
        "order_id": order_id,
    }), 200


# ─── My Orders ───────────────────────────────────────────────────────────────

@orders_bp.route('/my-orders', methods=['GET'])
def my_orders():
    whatsapp = request.args.get('whatsapp_number')
    if not whatsapp:
        return jsonify({"error": "whatsapp_number is required"}), 400
    user = User.query.filter_by(whatsapp_number=whatsapp).first()
    if not user:
        return jsonify([])
    orders = Order.query.filter_by(user_id=user.id).order_by(Order.created_at.desc()).all()
    result = []
    for o in orders:
        result.append({
            "order_id": o.id,
            "status": o.status,
            "payment_status": o.payment_status,
            "total_amount": o.total_amount,
            "payment_method": o.payment_method,
            "created_at": o.created_at.isoformat(),
            "tracking_number": o.tracking_number,
            "items": [
                {
                    "variant_id": item.variant_id,
                    "quantity": item.quantity,
                    "price_at_purchase": item.price_at_purchase
                } for item in o.items
            ]
        })
    return jsonify(result)
