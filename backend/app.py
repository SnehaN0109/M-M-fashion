from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from config import Config
from models import db
from sqlalchemy import text
import os


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app, resources={r"/api/*": {
        "origins": [
            "http://localhost:5173",
            "http://localhost:5174",
            "http://localhost:5175",
            "http://localhost:5176",
            "https://garba.shop",
            "https://ttd.in"
        ],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
    }})

    db.init_app(app)

    # ── Register Blueprints ──────────────────────────────────────────────────
    from routes.products import products_bp
    from routes.admin_dashboard import admin_bp
    from routes.auth import auth_bp
    from routes.orders import orders_bp
    from routes.cart_orders import cart_orders_bp

    app.register_blueprint(products_bp, url_prefix='/api/products')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(orders_bp, url_prefix='/api/orders')
    app.register_blueprint(cart_orders_bp, url_prefix='/api')

    # ── Health check ─────────────────────────────────────────────────────────
    @app.route("/")
    def home():
        return jsonify({"message": "M&M Fashion backend running"})

    @app.route("/uploads/photos/<path:filename>")
    def serve_photo(filename):
        upload_dir = os.path.join(os.path.dirname(__file__), 'uploads', 'photos')
        return send_from_directory(upload_dir, filename)

    @app.route("/api/test-db")
    def test_db():
        try:
            db.session.execute(text("SELECT 1"))
            return jsonify({"status": "connected", "message": "Database connection successful"})
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 500

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True, port=5000, use_reloader=False)
