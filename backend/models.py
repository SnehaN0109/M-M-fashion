from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    whatsapp_number = db.Column(db.String(20), unique=True, nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=True)
    name = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    orders = db.relationship('Order', backref='user', lazy=True)
    reviews = db.relationship('Review', backref='user', lazy=True)
    photos = db.relationship('UserPhoto', backref='user', lazy=True)
    wishlist = db.relationship('Wishlist', backref='user', lazy=True)

class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    description = db.Column(db.Text)
    category = db.Column(db.String(100))
    image_url = db.Column(db.Text)
    video_url = db.Column(db.Text)
    
    # Relationships
    variants = db.relationship('ProductVariant', backref='product', lazy=True, cascade="all, delete-orphan")
    reviews = db.relationship('Review', backref='product', lazy=True)
    photos = db.relationship('UserPhoto', backref='product', lazy=True)

class ProductVariant(db.Model):
    __tablename__ = 'productvariant'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    design_id = db.Column(db.String(100))
    color = db.Column(db.String(50))
    size = db.Column(db.String(10))
    quantity = db.Column(db.Integer)
    
    # Pricing
    price_b2c = db.Column(db.Numeric(10, 2))
    price_b2b_ttd = db.Column(db.Numeric(10, 2))
    price_b2b_maharashtra = db.Column(db.Numeric(10, 2))

class ProductImage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    image_url = db.Column(db.String(500), nullable=False)
    is_video = db.Column(db.Boolean, default=False)

class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True) # Null for guest
    session_id = db.Column(db.String(100), nullable=True) # For guest cart
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    items = db.relationship('CartItem', backref='cart', lazy=True, cascade="all, delete-orphan")

class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.Integer, db.ForeignKey('cart.id'), nullable=False)
    variant_id = db.Column(db.Integer, db.ForeignKey('product_variant.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    email = db.Column(db.String(120), nullable=True) # Required at checkout
    total_amount = db.Column(db.Float, nullable=False)
    discount_amount = db.Column(db.Float, default=0.0)
    shipping_charge = db.Column(db.Float, default=0.0)
    tax_amount = db.Column(db.Float, default=0.0)
    domain_origin = db.Column(db.String(100)) # e.g. 'ttd.in', 'garba.shop'
    status = db.Column(db.String(50), default='Pending') # Pending, Paid, Shipped, Delivered
    tracking_number = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    items = db.relationship('OrderItem', backref='order', lazy=True, cascade="all, delete-orphan")

class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    variant_id = db.Column(db.Integer, db.ForeignKey('product_variant.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price_at_purchase = db.Column(db.Float, nullable=False)

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    rating = db.Column(db.Integer, nullable=False) # 1 to 5
    comment = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class UserPhoto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    photo_url = db.Column(db.String(500), nullable=False)
    is_approved = db.Column(db.Boolean, default=False) # Admin moderation
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class DiscountCode(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50), unique=True, nullable=False)
    discount_percentage = db.Column(db.Float, nullable=True)
    discount_flat = db.Column(db.Float, nullable=True)
    min_cart_value = db.Column(db.Float, default=0.0)
    is_active = db.Column(db.Boolean, default=True)

class Wishlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)