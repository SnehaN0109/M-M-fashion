import os
import uuid
from flask import Blueprint, jsonify, request
from werkzeug.utils import secure_filename
from models import db, Product, ProductVariant, Review, UserPhoto, User, SiteSetting

products_bp = Blueprint('products', __name__)

@products_bp.route('/', methods=['GET'], strict_slashes=False)
def get_products():
    domain = request.args.get('domain')
    category = request.args.get('category')
    size = request.args.get('size')
    color = request.args.get('color')
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    search = request.args.get('search')

    VALID_PRICE_KEYS = {'price_b2c', 'price_b2b_ttd', 'price_b2b_maharashtra'}
    price_key = request.args.get('price_key', 'price_b2c')
    if price_key not in VALID_PRICE_KEYS:
        price_key = 'price_b2c'

    query = Product.query

    if search:
        query = query.filter(Product.name.ilike(f"%{search}%"))
    if category:
        query = query.filter_by(category=category)

    products = query.all()
    result = []

    for p in products:
        variants = p.variants
        
        # Filter variants by size/color
        if size:
            variants = [v for v in variants if v.size == size]
        if color:
            variants = [v for v in variants if v.color.lower() == color.lower()]
            
        if not variants and (size or color):
            continue

        variant_data = []
        for v in variants:
            # Use price_key to select correct price column
            price = float(getattr(v, price_key) or 0)

            # Price range filter
            if min_price is not None and price < min_price:
                continue
            if max_price is not None and price > max_price:
                continue

            variant_data.append({
                "id": v.id,
                "color": v.color,
                "size": v.size,
                "quantity": v.quantity,
                "price": price,
                "design_id": v.design_id,
                "low_stock": v.quantity < 5 if v.quantity is not None else False
            })

        if not variant_data:
            continue

        result.append({
            "id": p.id,
            "name": p.name,
            "description": p.description,
            "category": p.category,
            "image_url": p.image_url,
            "video_url": p.video_url,
            "variants": variant_data
        })

    return jsonify(result)

@products_bp.route('/<int:product_id>', methods=['GET'], strict_slashes=False)
def get_product(product_id):
    VALID_PRICE_KEYS = {'price_b2c', 'price_b2b_ttd', 'price_b2b_maharashtra'}
    price_key = request.args.get('price_key', 'price_b2c')
    if price_key not in VALID_PRICE_KEYS:
        price_key = 'price_b2c'

    p = Product.query.get_or_404(product_id)

    variant_data = []
    for v in p.variants:
        price = float(getattr(v, price_key) or 0)

        variant_data.append({
            "id": v.id,
            "color": v.color,
            "size": v.size,
            "quantity": v.quantity,
            "price": price,
            "design_id": v.design_id,
            "low_stock": v.quantity < 5 if v.quantity is not None else False
        })
        
    return jsonify({
        "id": p.id,
        "name": p.name,
        "description": p.description,
        "category": p.category,
        "image_url": p.image_url,
        "video_url": p.video_url,
        "variants": variant_data
    })


UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), '..', 'uploads', 'photos')
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# ─── Reviews ─────────────────────────────────────────────────────────────────

@products_bp.route('/<int:product_id>/reviews', methods=['GET'], strict_slashes=False)
def get_reviews(product_id):
    Product.query.get_or_404(product_id)
    reviews = Review.query.filter_by(product_id=product_id).order_by(Review.created_at.desc()).all()
    return jsonify([{
        "id": r.id,
        "rating": r.rating,
        "comment": r.comment,
        "created_at": r.created_at.isoformat()
    } for r in reviews])


@products_bp.route('/<int:product_id>/reviews', methods=['POST'], strict_slashes=False)
def add_review(product_id):
    Product.query.get_or_404(product_id)
    data = request.json
    rating = data.get('rating')
    if not rating or not (1 <= int(rating) <= 5):
        return jsonify({"error": "Rating must be between 1 and 5"}), 400

    whatsapp = data.get('whatsapp_number')
    user_id = None
    if whatsapp:
        user = User.query.filter_by(whatsapp_number=whatsapp).first()
        if user:
            user_id = user.id

    review = Review(
        product_id=product_id,
        user_id=user_id,
        rating=int(rating),
        comment=data.get('comment', '').strip() or None
    )
    db.session.add(review)
    db.session.commit()
    return jsonify({"message": "Review submitted", "id": review.id}), 201


# ─── User Photos ─────────────────────────────────────────────────────────────

@products_bp.route('/<int:product_id>/photos', methods=['GET'], strict_slashes=False)
def get_photos(product_id):
    Product.query.get_or_404(product_id)
    photos = UserPhoto.query.filter_by(product_id=product_id, is_approved=True).all()
    return jsonify([{
        "id": p.id,
        "photo_url": p.photo_url,
        "created_at": p.created_at.isoformat()
    } for p in photos])


@products_bp.route('/<int:product_id>/photos', methods=['POST'], strict_slashes=False)
def upload_photo(product_id):
    Product.query.get_or_404(product_id)

    whatsapp = request.form.get('whatsapp_number')
    if not whatsapp:
        return jsonify({"error": "whatsapp_number is required"}), 400

    user = User.query.filter_by(whatsapp_number=whatsapp).first()
    if not user:
        return jsonify({"error": "User not found. Please login first."}), 404

    if 'photo' not in request.files:
        return jsonify({"error": "No photo file provided"}), 400

    file = request.files['photo']
    if file.filename == '' or not allowed_file(file.filename):
        return jsonify({"error": "Invalid file. Allowed: jpg, jpeg, png, webp"}), 400

    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    ext = file.filename.rsplit('.', 1)[1].lower()
    filename = f"{uuid.uuid4().hex}.{ext}"
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    photo_url = f"/uploads/photos/{filename}"

    photo = UserPhoto(
        product_id=product_id,
        user_id=user.id,
        photo_url=photo_url,
        is_approved=False  # pending admin approval
    )
    db.session.add(photo)
    db.session.commit()
    return jsonify({"message": "Photo uploaded successfully. Pending admin approval.", "id": photo.id}), 201


@products_bp.route('/settings/popup', methods=['GET'], strict_slashes=False)
def get_public_popup():
    setting = SiteSetting.query.filter_by(key='welcome_popup').first()
    if not setting:
        return jsonify({"message": "", "is_active": False})
    return jsonify({"message": setting.value, "is_active": setting.is_active})
