from flask import Blueprint, jsonify, request
from models import db, Product, ProductVariant, UserPhoto, DiscountCode

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/add-product', methods=['POST'])
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
        gender=data.get('gender')
    )
    db.session.add(p)
    db.session.commit()
    
    variants = data.get('variants', [])
    for v in variants:
        pv = ProductVariant(
            product_id=p.id,
            design_id=v.get('design_id'),
            color=v.get('color'),
            size=v.get('size'),
            quantity=v.get('quantity', 0),
            price_ttd=v.get('price_ttd', 0),
            price_garba=v.get('price_garba', 0),
            price_maha=v.get('price_maha', 0)
        )
        db.session.add(pv)
        
    db.session.commit()
    return jsonify({"message": "Product created successfully", "product_id": p.id})

@admin_bp.route('/approve-photo/<int:photo_id>', methods=['POST'])
def approve_photo(photo_id):
    photo = UserPhoto.query.get_or_404(photo_id)
    photo.is_approved = True
    db.session.commit()
    return jsonify({"message": "Photo approved"})

@admin_bp.route('/discount-codes', methods=['POST'])
def create_discount():
    data = request.json
    code = DiscountCode(
        code=data.get('code'),
        discount_percentage=data.get('discount_percentage'),
        discount_flat=data.get('discount_flat'),
        min_cart_value=data.get('min_cart_value', 0)
    )
    db.session.add(code)
    db.session.commit()
    return jsonify({"message": "Discount code created"})

@admin_bp.route('/discount-codes', methods=['GET'])
def get_discounts():
    codes = DiscountCode.query.all()
    return jsonify([{
        "id": c.id,
        "code": c.code,
        "percentage": c.discount_percentage,
        "flat": c.discount_flat,
        "active": c.is_active
    } for c in codes])
