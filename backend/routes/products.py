from flask import Blueprint, jsonify, request
from models import db, Product, ProductVariant

products_bp = Blueprint('products', __name__)

@products_bp.route('/', methods=['GET'])
def get_products():
    domain = request.args.get('domain')
    category = request.args.get('category')
    size = request.args.get('size')
    color = request.args.get('color')
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    search = request.args.get('search')

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
            # Pricing logic
            if domain == "ttd.in":
                price = float(v.price_b2b_ttd) if v.price_b2b_ttd else 0.0
            elif domain == "maharashtra":
                price = float(v.price_b2b_maharashtra) if v.price_b2b_maharashtra else 0.0
            else:
                price = float(v.price_b2c) if v.price_b2c else 0.0

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

@products_bp.route('/<int:product_id>', methods=['GET'])
def get_product(product_id):
    domain = request.args.get('domain')
    p = Product.query.get_or_404(product_id)
    
    variant_data = []
    for v in p.variants:
        if domain == "ttd.in":
            price = float(v.price_b2b_ttd) if v.price_b2b_ttd else 0.0
        elif domain == "maharashtra":
            price = float(v.price_b2b_maharashtra) if v.price_b2b_maharashtra else 0.0
        else:
            price = float(v.price_b2c) if v.price_b2c else 0.0

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