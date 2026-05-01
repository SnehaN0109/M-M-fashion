#!/usr/bin/env python3
"""
Test database connection and show detailed diagnostics.
Run this to verify your database setup is working.
"""
from app import create_app
from models import db, Product, ProductVariant
from sqlalchemy import text
import sys

def test_connection():
    """Test database connection with detailed diagnostics."""
    print("🔍 Testing M&M Fashion Database Connection...")
    print("=" * 60)
    
    try:
        app = create_app()
        with app.app_context():
            # Test 1: Basic connection
            print("1️⃣ Testing basic connection...")
            result = db.session.execute(text("SELECT 1 as test"))
            print("   ✅ Database connection successful!")
            
            # Test 2: Check if tables exist
            print("\n2️⃣ Checking database tables...")
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            
            required_tables = ['product', 'productvariant', 'user', 'order']
            missing_tables = [t for t in required_tables if t not in tables]
            
            if missing_tables:
                print(f"   ❌ Missing tables: {missing_tables}")
                print("   💡 Run: python init_db.py to create tables")
                return False
            else:
                print(f"   ✅ All required tables exist: {tables}")
            
            # Test 3: Check for data
            print("\n3️⃣ Checking for product data...")
            product_count = Product.query.count()
            variant_count = ProductVariant.query.count()
            
            print(f"   📊 Products: {product_count}")
            print(f"   📊 Variants: {variant_count}")
            
            if product_count == 0:
                print("   ⚠️  No products found - database is empty")
                print("   💡 Add products via admin dashboard or import script")
            else:
                print("   ✅ Products found in database!")
                
                # Show sample data
                sample_products = Product.query.limit(3).all()
                print("\n   📋 Sample products:")
                for p in sample_products:
                    variant_count = len(p.variants)
                    print(f"      • {p.name} (ID: {p.id}, Variants: {variant_count})")
            
            # Test 4: Test API endpoint simulation
            print("\n4️⃣ Testing data retrieval (API simulation)...")
            products = Product.query.all()
            api_data = []
            
            for p in products:
                variants_with_prices = []
                for v in p.variants:
                    if v.price_b2c and v.price_b2c > 0:
                        variants_with_prices.append({
                            'id': v.id,
                            'price_b2c': float(v.price_b2c),
                            'quantity': v.quantity
                        })
                
                if variants_with_prices:
                    api_data.append({
                        'id': p.id,
                        'name': p.name,
                        'variants': variants_with_prices
                    })
            
            print(f"   📊 Products with valid pricing: {len(api_data)}")
            
            if len(api_data) == 0:
                print("   ⚠️  No products have valid B2C pricing")
                print("   💡 Check product variants have price_b2c > 0")
            else:
                print("   ✅ Products ready for API responses!")
            
            print("\n" + "=" * 60)
            print("🎉 Database connection test completed successfully!")
            return True
            
    except ImportError as e:
        print(f"❌ Import Error: {e}")
        print("💡 Install missing packages: pip install -r requirements.txt")
        return False
        
    except Exception as e:
        print(f"❌ Database Error: {e}")
        print(f"   Error Type: {type(e).__name__}")
        
        # Common error diagnostics
        error_str = str(e).lower()
        if "access denied" in error_str:
            print("💡 Check DB_USERNAME and DB_PASSWORD in .env")
        elif "unknown host" in error_str or "can't connect" in error_str:
            print("💡 Check DB_HOST and DB_PORT in .env")
        elif "unknown database" in error_str:
            print("💡 Check DB_NAME in .env - database may not exist")
        elif "ssl" in error_str:
            print("💡 SSL connection issue - check DB_USE_SSL setting")
        
        return False

if __name__ == "__main__":
    success = test_connection()
    sys.exit(0 if success else 1)