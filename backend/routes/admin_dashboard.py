import os
import uuid
from flask import Blueprint, jsonify, request, current_app
from werkzeug.utils import secure_filename
from functools import wraps
import jwt as pyjwt
import datetime
from models import db, Product, ProductVariant, ProductImage, UserPhoto, DiscountCode, Order, SiteSetting, User

# ─── Upload helpers ────────────────────────────────────────────────────────────
PRODUCT_UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), '..', 'uploads', 'products')
ALLOWED_EXTENSIONS    = {'jpg', 'jpeg', 'png', 'webp'}

def _allowed(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def _save_image(file):
    os.makedirs(PRODUCT_UPLOAD_FOLDER, exist_ok=True)
    ext = file.filename.rsplit('.', 1)[1].lower()
    fname = f"{uuid.uuid4().hex}.{ext}"
    file.save(os.path.join(PRODUCT_UPLOAD_FOLDER, fname))
    return f"/uploads/products/{fname}"

admin_bp = Blueprint('admin', __name__)


# ─── Auth decorator ───────────────────────────────────────────────────────────

def admin_required(f):
    """Verify JWT admin token on every protected admin route."""
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


# ─── Auth ─────────────────────────────────────────────────────────────────────

@admin_bp.route('/login', methods=['POST'])
def admin_login():
    data = request.json or {}
    password = data.get('password', '')
    if password != current_app.config.get('ADMIN_PASSWORD'):
        return jsonify({"error": "Invalid password"}), 401

    token = pyjwt.encode(
        {
            "role": "admin",
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        },
        current_app.config['SECRET_KEY'],
        algorithm='HS256'
    )
    return jsonify({"success": True, "token": token})


# ─── Products ────────────────────────────────────────────────────────────────

@admin_bp.route('/products', methods=['GET'])
@admin_required
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
@admin_required
def add_product():
    # Support both multipart/form-data (file upload) and application/json
    is_multipart = request.content_type and 'multipart/form-data' in request.content_type

    if is_multipart:
        data = request.form
    else:
        data = request.json or {}

    name = data.get('name')
    if not name:
        return jsonify({"error": "Product name is required"}), 400

    # ── Handle image upload ──────────────────────────────────────────────────
    image_url = data.get('image_url', '')
    if is_multipart and 'image' in request.files:
        file = request.files['image']
        if file and file.filename and _allowed(file.filename):
            image_url = _save_image(file)
        elif file and file.filename:
            return jsonify({"error": "Invalid image type. Allowed: jpg, jpeg, png, webp"}), 400

    import json
    p = Product(
        name=name,
        description=data.get('description'),
        category=data.get('category'),
        fabric=data.get('fabric'),
        occasion=data.get('occasion'),
        pattern=data.get('pattern'),
        gender=data.get('gender'),
        image_url=image_url or None,
        video_url=data.get('video_url')
    )
    db.session.add(p)
    db.session.flush()

    # ── Variants ─────────────────────────────────────────────────────────────
    variants_raw = data.get('variants', '[]')
    variants = variants_raw if isinstance(variants_raw, list) else json.loads(variants_raw)
    for v in variants:
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

    # ── Extra images ──────────────────────────────────────────────────────────
    images_raw = data.get('images', '[]')
    images = images_raw if isinstance(images_raw, list) else json.loads(images_raw)
    for idx, img_url in enumerate(images):
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
@admin_required
def edit_product(product_id):
    p = Product.query.get_or_404(product_id)

    is_multipart = request.content_type and 'multipart/form-data' in request.content_type
    data = request.form if is_multipart else (request.json or {})

    p.name        = data.get('name', p.name)
    p.description = data.get('description', p.description)
    p.category    = data.get('category', p.category)
    p.fabric      = data.get('fabric', p.fabric)
    p.occasion    = data.get('occasion', p.occasion)
    p.pattern     = data.get('pattern', p.pattern)
    p.gender      = data.get('gender', p.gender)
    p.video_url   = data.get('video_url', p.video_url)

    # Only replace image_url if a new file was uploaded
    if is_multipart and 'image' in request.files:
        file = request.files['image']
        if file and file.filename and _allowed(file.filename):
            p.image_url = _save_image(file)
        elif file and file.filename:
            return jsonify({"error": "Invalid image type. Allowed: jpg, jpeg, png, webp"}), 400
    elif not is_multipart and 'image_url' in data:
        p.image_url = data.get('image_url', p.image_url)

    db.session.commit()
    return jsonify({"message": "Product updated"})


@admin_bp.route('/products/<int:product_id>', methods=['DELETE'])
@admin_required
def delete_product(product_id):
    p = Product.query.get_or_404(product_id)
    db.session.delete(p)
    db.session.commit()
    return jsonify({"message": "Product deleted"})


# ─── Orders ──────────────────────────────────────────────────────────────────

@admin_bp.route('/orders', methods=['GET'])
@admin_required
def list_orders():
    status_filter = request.args.get('status')
    domain_filter = request.args.get('domain')   # e.g. ?domain=ttd.in
    query = Order.query.order_by(Order.created_at.desc())
    if status_filter:
        query = query.filter_by(status=status_filter)
    if domain_filter:
        query = query.filter(Order.domain_origin.ilike(f"%{domain_filter}%"))
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
            "business_name": o.business_name,
            "gst_number": o.gst_number,
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
@admin_required
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
@admin_required
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
@admin_required
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
@admin_required
def toggle_discount(code_id):
    code = DiscountCode.query.get_or_404(code_id)
    code.is_active = not code.is_active
    db.session.commit()
    return jsonify({"message": "Updated", "is_active": code.is_active})


@admin_bp.route('/discount-codes/<int:code_id>', methods=['DELETE'])
@admin_required
def delete_discount(code_id):
    code = DiscountCode.query.get_or_404(code_id)
    db.session.delete(code)
    db.session.commit()
    return jsonify({"message": "Deleted"})


# ─── User Photos (moderation) ─────────────────────────────────────────────────

@admin_bp.route('/photos/pending', methods=['GET'])
@admin_required
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
@admin_required
def approve_photo(photo_id):
    photo = UserPhoto.query.get_or_404(photo_id)
    photo.is_approved = True
    db.session.commit()
    return jsonify({"message": "Photo approved"})


@admin_bp.route('/photos/<int:photo_id>/reject', methods=['DELETE'])
@admin_required
def reject_photo(photo_id):
    photo = UserPhoto.query.get_or_404(photo_id)
    db.session.delete(photo)
    db.session.commit()
    return jsonify({"message": "Photo rejected and deleted"}), 200


# ─── Site Settings ───────────────────────────────────────────────────────────

@admin_bp.route('/settings/popup', methods=['GET'], strict_slashes=False)
@admin_required
def get_popup_setting():
    setting = SiteSetting.query.filter_by(key='welcome_popup').first()
    if not setting:
        return jsonify({"message": "", "is_active": False})
    return jsonify({"message": setting.value, "is_active": setting.is_active})

@admin_bp.route('/settings/popup', methods=['POST', 'PUT'], strict_slashes=False)
@admin_required
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


# ─── User Role Management (B2B wholesaler control) ────────────────────────────

@admin_bp.route('/users', methods=['GET'])
@admin_required
def list_users():
    """List all users with their roles."""
    users = User.query.order_by(User.created_at.desc()).all()
    return jsonify([{
        "id": u.id,
        "whatsapp_number": u.whatsapp_number,
        "name": u.name,
        "email": u.email,
        "role": u.role or 'B2C',
        "created_at": u.created_at.isoformat()
    } for u in users])


@admin_bp.route('/users/<int:user_id>/role', methods=['PUT'])
@admin_required
def set_user_role(user_id):
    """Promote or demote a user between B2C and WHOLESALER."""
    user = User.query.get_or_404(user_id)
    data = request.json or {}
    new_role = data.get('role', '').upper()
    if new_role not in ('B2C', 'WHOLESALER'):
        return jsonify({"error": "role must be 'B2C' or 'WHOLESALER'"}), 400
    user.role = new_role
    db.session.commit()
    return jsonify({"message": f"User role updated to {new_role}", "user_id": user_id, "role": new_role})
