from flask import Flask, jsonify
from flask_cors import CORS
from config import Config
from models import db
from sqlalchemy import text

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app, resources={r"/api/*": {"origins": "http://localhost:5173"}})
    db.init_app(app)

    # Register Blueprints
    from routes.products import products_bp
    app.register_blueprint(products_bp, url_prefix='/api/products')

    @app.route("/")
    def home():
        return {"message": "M&M Fashion backend running"}

    # Test Routes
    @app.route("/api/test-db")
    def test_db():
        try:
            db.session.execute(text("SELECT 1"))
            return jsonify({"status": "connected", "message": "Database connection successful"})
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 500

    @app.route("/api/test-products")
    def test_products():
        from models import Product
        try:
            products = Product.query.all()
            return jsonify([{"id": p.id, "name": p.name} for p in products])
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True, port=5000)