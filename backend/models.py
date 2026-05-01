from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    whatsapp_number = db.Column(db.String(20), unique=True, nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=True)
    name = db.Column(db.String(100), nullable=True)
    # B2B role: 'B2C' (default) or 'WHOLESALER'
    # server_default ensures existing rows in DB get 'B2C' without a data migration
    role = db.Column(db.String(20), nullable=False, server_default='B2C', default='B2C')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    orders = db.relationship('Order', backref='user', lazy=True)
    reviews = db.relationship('Review', backref='user', lazy=True)
    photos = db.relationship('UserPhoto', backref='user', lazy=True)
    wishlist = db.relationship('Wishlist', backref='user', lazy=True)
    addresses = db.relationship('Address', backref='user', lazy=True)


class Address(db.Model):
    __tablename__ = 'address'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    line1 = db.Column(db.String(255), nullable=False)
    line2 = db.Column(db.String(255), nullable=True)
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(100), nullable=False)
    pincode = db.Column(db.String(10), nullable=False)
    is_default = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(100))   # Men, Women, Kids, Ethnic, Western, Party Wear
    fabric = db.Column(db.String(100))     # Cotton, Silk, Georgette, etc.
    occasion = db.Column(db.String(100))   # Casual, Festive, Wedding, etc.
    pattern = db.Column(db.String(100))    # Solid, Printed, Embroidered, etc.
    gender = db.Column(db.String(20))      # Men, Women, Kids, Unisex
    image_url = db.Column(db.Text)         # primary/cover image
    video_url = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    variants = db.relationship('ProductVariant', backref='product', lazy=True, cascade="all, delete-orphan")
    images = db.relationship('ProductImage', backref='product', lazy=True, cascade="all, delete-orphan")
    videos = db.relationship('ProductVideo', backref='product', lazy=True, cascade="all, delete-orphan")
    reviews = db.relationship('Review', backref='product', lazy=True, cascade="all, delete-orphan")
    photos = db.relationship('UserPhoto', backref='product', lazy=True, cascade="all, delete-orphan")
    wishlist = db.relationship('Wishlist', backref='product', lazy=True, cascade="all, delete-orphan")


class ProductVariant(db.Model):
    __tablename__ = 'productvariant'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    design_id = db.Column(db.String(100))  # unique design identifier
    color = db.Column(db.String(50))
    size = db.Column(db.String(10))
    quantity = db.Column(db.Integer, default=0)

    # 3 pricing columns — one per domain
    price_b2c = db.Column(db.Numeric(10, 2), default=0)           # garba.shop
    price_b2b_ttd = db.Column(db.Numeric(10, 2), default=0)       # ttd.in
    price_b2b_maharashtra = db.Column(db.Numeric(10, 2), default=0)  # maharashtra domain

    # B2B minimum order quantity (optional, only enforced for B2B domains)
    moq_b2b = db.Column(db.Integer, nullable=True)

    order_items = db.relationship('OrderItem', backref='variant', lazy=True, cascade="all, delete-orphan")
    cart_items = db.relationship('CartItem', backref='variant', lazy=True, cascade="all, delete-orphan")


class ProductImage(db.Model):
    __tablename__ = 'productimage'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    image_url = db.Column(db.String(500), nullable=False)
    is_primary = db.Column(db.Boolean, default=False)
    sort_order = db.Column(db.Integer, default=0)


class ProductVideo(db.Model):
    __tablename__ = 'productvideo'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    video_url = db.Column(db.String(500), nullable=False)


class Cart(db.Model):
    __tablename__ = 'cart'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    session_id = db.Column(db.String(100), nullable=True)  # for guest cart
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    items = db.relationship('CartItem', backref='cart', lazy=True, cascade="all, delete-orphan")


class CartItem(db.Model):
    __tablename__ = 'cartitem'
    id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.Integer, db.ForeignKey('cart.id'), nullable=False)
    variant_id = db.Column(db.Integer, db.ForeignKey('productvariant.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)


class Order(db.Model):
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)

    # Customer details captured at checkout
    customer_name = db.Column(db.String(100))
    customer_email = db.Column(db.String(120))
    customer_phone = db.Column(db.String(20))

    # Shipping address
    address_line1 = db.Column(db.String(255))
    address_line2 = db.Column(db.String(255))
    city = db.Column(db.String(100))
    state = db.Column(db.String(100))
    pincode = db.Column(db.String(10))

    # Financials
    subtotal = db.Column(db.Float, default=0.0)
    discount_amount = db.Column(db.Float, default=0.0)
    discount_code = db.Column(db.String(50), nullable=True)
    shipping_charge = db.Column(db.Float, default=0.0)
    tax_amount = db.Column(db.Float, default=0.0)
    total_amount = db.Column(db.Float, nullable=False)

    # Meta
    domain_origin = db.Column(db.String(100))
    payment_method = db.Column(db.String(50), default='COD')
    status = db.Column(db.String(50), default='PENDING_PAYMENT')
    payment_status = db.Column(db.String(50), default='PENDING')
    # Status flow: PENDING_PAYMENT → PLACED → PACKED → SHIPPED → OUT_FOR_DELIVERY → DELIVERED
    tracking_number = db.Column(db.String(100), nullable=True)
    # B2B fields (optional — only populated for wholesaler orders)
    business_name = db.Column(db.String(200), nullable=True)
    gst_number = db.Column(db.String(20), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    items = db.relationship('OrderItem', backref='order', lazy=True, cascade="all, delete-orphan")


class OrderItem(db.Model):
    __tablename__ = 'orderitem'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    variant_id = db.Column(db.Integer, db.ForeignKey('productvariant.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price_at_purchase = db.Column(db.Float, nullable=False)  # snapshot of price when ordered


class Review(db.Model):
    __tablename__ = 'review'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    rating = db.Column(db.Integer, nullable=False)  # 1 to 5
    comment = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class UserPhoto(db.Model):
    __tablename__ = 'userphoto'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    photo_url = db.Column(db.String(500), nullable=False)
    is_approved = db.Column(db.Boolean, default=False)  # admin must approve before showing
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class DiscountCode(db.Model):
    __tablename__ = 'discountcode'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50), unique=True, nullable=False)
    discount_percentage = db.Column(db.Float, nullable=True)   # e.g. 10 for 10%
    discount_flat = db.Column(db.Float, nullable=True)         # e.g. 200 for ₹200 off
    min_cart_value = db.Column(db.Float, default=0.0)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Wishlist(db.Model):
    __tablename__ = 'wishlist'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class SiteSetting(db.Model):
    __tablename__ = 'sitesetting'
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(50), unique=True, nullable=False)
    value = db.Column(db.Text, nullable=True)
    is_active = db.Column(db.Boolean, default=True)
