from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from flask_mail import Mail
from config import Config
from models import db
import os

# Absolute path to the backend directory — used for all file serving
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOADS_DIR = os.path.join(BASE_DIR, 'uploads')


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Allow all origins for both API routes and static upload files
    CORS(app, resources={
        r"/api/*":     {"origins": "*", "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"]},
        r"/uploads/*": {"origins": "*", "methods": ["GET", "OPTIONS"]},
    })

    db.init_app(app)

    # Initialize Flask-Mail
    mail = Mail(app)
    app.mail = mail

    # ── Register Blueprints ──────────────────────────────────────────────────
    from routes.products import products_bp
    from routes.admin_dashboard import admin_bp
    from routes.auth import auth_bp
    from routes.orders import orders_bp
    from routes.cart_orders import cart_orders_bp
    from routes.payment import payment_bp
    from routes.wishlist import wishlist_bp
    from routes.test_sms import test_sms_bp

    app.register_blueprint(products_bp, url_prefix='/api/products')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(orders_bp, url_prefix='/api/orders')
    app.register_blueprint(cart_orders_bp, url_prefix='/api')
    app.register_blueprint(payment_bp)
    app.register_blueprint(wishlist_bp, url_prefix='/api')
    app.register_blueprint(test_sms_bp, url_prefix='/api/test')

    # ── Static file serving — single route handles all upload subfolders ────
    # Covers: /uploads/payment_proofs/*, /uploads/products/*, /uploads/photos/*
    @app.route('/uploads/<path:filename>')
    def serve_uploads(filename):
        return send_from_directory(UPLOADS_DIR, filename)

    # ── Error Handlers ───────────────────────────────────────────────────────
    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"error": "Resource not found"}), 404

    @app.errorhandler(500)
    def internal_error(e):
        return jsonify({"error": "Internal server error"}), 500

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True, port=5000, use_reloader=False)
