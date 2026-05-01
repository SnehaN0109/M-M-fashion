from app import app, db
from models import DiscountCode

with app.app_context():
    # Check if discount codes already exist
    existing = DiscountCode.query.all()
    if existing:
        print(f"Found {len(existing)} existing discount codes:")
        for code in existing:
            print(f"  - {code.code}: {code.discount_percentage}% / ₹{code.discount_flat} flat (Active: {code.is_active})")
    else:
        print("No discount codes found. Adding test codes...")
        
        # Add test discount codes
        codes = [
            DiscountCode(code='SAVE10', discount_percentage=10, discount_flat=None, min_cart_value=500, is_active=True),
            DiscountCode(code='FLAT100', discount_percentage=None, discount_flat=100, min_cart_value=1000, is_active=True),
            DiscountCode(code='WELCOME20', discount_percentage=20, discount_flat=None, min_cart_value=0, is_active=True),
            DiscountCode(code='FLAT200', discount_percentage=None, discount_flat=200, min_cart_value=1500, is_active=True),
        ]
        
        for code in codes:
            db.session.add(code)
        
        db.session.commit()
        print("✅ Added 4 test discount codes:")
        print("  - SAVE10: 10% off (min cart ₹500)")
        print("  - FLAT100: ₹100 off (min cart ₹1000)")
        print("  - WELCOME20: 20% off (no minimum)")
        print("  - FLAT200: ₹200 off (min cart ₹1500)")
