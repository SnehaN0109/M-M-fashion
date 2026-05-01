from app import create_app
from models import db, ProductVariant

app = create_app()
with app.app_context():
    variants = ProductVariant.query.all()
    for v in variants:
        print(f"ID: {v.id}, B2C: {v.price_b2c}, TTD: {v.price_b2b_ttd}, MH: {v.price_b2b_maharashtra}")
