from flask import Blueprint, jsonify, request
from models import db, Product, ProductVariant, ProductImage, UserPhoto, DiscountCode, Order, SiteSetting
from flask import current_app

admin_bp = Blueprint('admin', __name__)


# ─── Auth ─────────────────────────────────────────────────────────────────────

@admin_bp.route('/login', methods=['POST'])
def admin_login():
    data = request.json or {}
    password = data.get('password', '')
    if password == current_app.config.get('ADMIN_PASSWORD'):
        return jsonify({"success": True, "token": "admin-authenticated"})
    return jsonify({"error": "Invalid password"}), 401


# ─── Products ────────────────────────────────────────────────────────────────

@admin_bp.route('/products', methods=['GET'])
def list_products():
    products = Product.query.order_by(Product.created_at.desc()).all()
    result = []
    for p in products:
        result.append({
            "id": p.id,
            "name": p.name,
            "category": p.category,
            "fabric": p.fabric,
            "occasion": p.occasion,
            "pattern": p.pattern,
            "gender": p.gender,
            "image_url": p.image_url,
            "variant_count": len(p.variants),
            "created_at": p.created_at.isoformat()
        })
    return jsonify(result)


@admin_bp.route('/products/add', methods=['POST'])
def add_product():
    data = request.json
    name = data.get('name')
    if not name:
        return jsonify({"error": "Product name is required"}), 400

    p = Product(
        name=name,
        description=data.get('description'),
        category=data.get('category'),
        fabric=data.get('fabric'),
        occasion=data.get('occasion'),
        pattern=data.get('pattern'),
        gender=data.get('gender'),
        image_url=data.get('image_url'),
        video_url=data.get('video_url')
    )
    db.session.add(p)
    db.session.flush()  # get p.id before commit

    # Add variants
    for v in data.get('variants', []):
        pv = ProductVariant(
            product_id=p.id,
            design_id=v.get('design_id'),
            color=v.get('color'),
            size=v.get('size'),
            quantity=v.get('quantity', 0),
            price_b2c=v.get('price_b2c', 0),
            price_b2b_ttd=v.get('price_b2b_ttd', 0),
            price_b2b_maharashtra=v.get('price_b2b_maharashtra', 0)
        )
        db.session.add(pv)

    # Add extra images
    for idx, img_url in enumerate(data.get('images', [])):
        pi = ProductImage(
            product_id=p.id,
            image_url=img_url,
            is_primary=(idx == 0),
            sort_order=idx
        )
        db.session.add(pi)

    db.session.commit()
    return jsonify({"message": "Product created successfully", "product_id": p.id}), 201


@admin_bp.route('/products/<int:product_id>', methods=['PUT'])
def edit_product(product_id):
    p = Product.query.get_or_404(product_id)
    data = request.json

    p.name = data.get('name', p.name)
    p.description = data.get('description', p.description)
    p.category = data.get('category', p.category)
    p.fabric = data.get('fabric', p.fabric)
    p.occasion = data.get('occasion', p.occasion)
    p.pattern = data.get('pattern', p.pattern)
    p.gender = data.get('gender', p.gender)
    p.image_url = data.get('image_url', p.image_url)
    p.video_url = data.get('video_url', p.video_url)

    db.session.commit()
    return jsonify({"message": "Product updated"})


@admin_bp.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    p = Product.query.get_or_404(product_id)
    db.session.delete(p)
    db.session.commit()
    return jsonify({"message": "Product deleted"})


# ─── Orders ──────────────────────────────────────────────────────────────────

@admin_bp.route('/orders', methods=['GET'])
def list_orders():
    status_filter = request.args.get('status')
    query = Order.query.order_by(Order.created_at.desc())
    if status_filter:
        query = query.filter_by(status=status_filter)
    orders = query.all()
    result = []
    for o in orders:
        result.append({
            "id": o.id,
            "customer_name": o.customer_name,
            "customer_email": o.customer_email,
            "customer_phone": o.customer_phone,
            "total_amount": o.total_amount,
            "status": o.status,
            "payment_method": o.payment_method,
            "domain_origin": o.domain_origin,
            "tracking_number": o.tracking_number,
            "created_at": o.created_at.isoformat(),
            "items": [
                {
                    "variant_id": item.variant_id,
                    "quantity": item.quantity,
                    "price_at_purchase": item.price_at_purchase
                } for item in o.items
            ]
        })
    return jsonify(result)


@admin_bp.route('/orders/<int:order_id>/status', methods=['PUT'])
def update_order_status(order_id):
    o = Order.query.get_or_404(order_id)
    data = request.json
    valid_statuses = ['pending_payment', 'confirmed', 'packed', 'shipped', 'delivered', 'cancelled']
    new_status = data.get('status')
    if new_status not in valid_statuses:
        return jsonify({"error": f"Invalid status. Must be one of {valid_statuses}"}), 400
    o.status = new_status
    if data.get('tracking_number'):
        o.tracking_number = data.get('tracking_number')
    db.session.commit()
    return jsonify({"message": "Order status updated", "status": o.status})


# ─── Discount Codes ───────────────────────────────────────────────────────────

@admin_bp.route('/discount-codes', methods=['GET'])
def get_discounts():
    codes = DiscountCode.query.order_by(DiscountCode.created_at.desc()).all()
    return jsonify([{
        "id": c.id,
        "code": c.code,
        "discount_percentage": c.discount_percentage,
        "discount_flat": c.discount_flat,
        "min_cart_value": c.min_cart_value,
        "is_active": c.is_active
    } for c in codes])


@admin_bp.route('/discount-codes', methods=['POST'])
def create_discount():
    data = request.json
    if not data.get('code'):
        return jsonify({"error": "Code is required"}), 400
    if DiscountCode.query.filter_by(code=data['code']).first():
        return jsonify({"error": "Code already exists"}), 400
    code = DiscountCode(
        code=data['code'].upper().strip(),
        discount_percentage=data.get('discount_percentage'),
        discount_flat=data.get('discount_flat'),
        min_cart_value=data.get('min_cart_value', 0)
    )
    db.session.add(code)
    db.session.commit()
    return jsonify({"message": "Discount code created", "id": code.id}), 201


@admin_bp.route('/discount-codes/<int:code_id>', methods=['PUT'])
def toggle_discount(code_id):
    code = DiscountCode.query.get_or_404(code_id)
    code.is_active = not code.is_active
    db.session.commit()
    return jsonify({"message": "Updated", "is_active": code.is_active})


@admin_bp.route('/discount-codes/<int:code_id>', methods=['DELETE'])
def delete_discount(code_id):
    code = DiscountCode.query.get_or_404(code_id)
    db.session.delete(code)
    db.session.commit()
    return jsonify({"message": "Deleted"})


# ─── User Photos (moderation) ─────────────────────────────────────────────────

@admin_bp.route('/photos/pending', methods=['GET'])
def pending_photos():
    photos = UserPhoto.query.filter_by(is_approved=False).all()
    return jsonify([{
        "id": p.id,
        "product_id": p.product_id,
        "user_id": p.user_id,
        "photo_url": p.photo_url,
        "created_at": p.created_at.isoformat()
    } for p in photos])


@admin_bp.route('/photos/<int:photo_id>/approve', methods=['POST'])
def approve_photo(photo_id):
    photo = UserPhoto.query.get_or_404(photo_id)
    photo.is_approved = True
    db.session.commit()
    return jsonify({"message": "Photo approved"})


@admin_bp.route('/photos/<int:photo_id>/reject', methods=['DELETE'])
def reject_photo(photo_id):
    photo = UserPhoto.query.get_or_404(photo_id)
    db.session.delete(photo)
    db.session.commit()
    return jsonify({"message": "Photo rejected and deleted"}), 200


# ─── Site Settings ───────────────────────────────────────────────────────────

@admin_bp.route('/settings/popup', methods=['GET'], strict_slashes=False)
def get_popup_setting():
    setting = SiteSetting.query.filter_by(key='welcome_popup').first()
    if not setting:
        return jsonify({"message": "", "is_active": False})
    return jsonify({"message": setting.value, "is_active": setting.is_active})

@admin_bp.route('/settings/popup', methods=['POST', 'PUT'], strict_slashes=False)
def update_popup_setting():
    data = request.json
    setting = SiteSetting.query.filter_by(key='welcome_popup').first()
    if not setting:
        setting = SiteSetting(key='welcome_popup', value=data.get('message', ''), is_active=data.get('is_active', False))
        db.session.add(setting)
    else:
        setting.value = data.get('message', setting.value)
        if 'is_active' in data:
            setting.is_active = data['is_active']
    db.session.commit()
    return jsonify({"success": True})
