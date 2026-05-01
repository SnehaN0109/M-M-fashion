from app import create_app
from models import db, ProductVariant
import sys

def check_prices():
    """Check and display all product variant prices."""
    try:
        app = create_app()
        with app.app_context():
            # Test database connection first
            db.session.execute(db.text("SELECT 1"))
            print("✓ Database connection successful")
            
            # Query all variants
            variants = ProductVariant.query.all()
            
            if not variants:
                print("No product variants found in database.")
                return
            
            print(f"\nFound {len(variants)} product variants:")
            print("-" * 80)
            print(f"{'ID':<5} {'B2C Price':<12} {'TTD Price':<12} {'MH Price':<12} {'Product ID':<12}")
            print("-" * 80)
            
            for v in variants:
                print(f"{v.id:<5} {v.price_b2c:<12} {v.price_b2b_ttd:<12} {v.price_b2b_maharashtra:<12} {v.product_id:<12}")
                
    except Exception as e:
        print(f"❌ Error occurred: {str(e)}")
        print(f"Error type: {type(e).__name__}")
        sys.exit(1)

if __name__ == "__main__":
    check_prices()
