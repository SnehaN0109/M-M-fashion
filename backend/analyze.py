from app import create_app
from models import db

app = create_app()
with app.app_context():
    tables = [
        'user','product','productvariant','order','orderitem',
        'cart','cartitem','wishlist','discountcode','review',
        'userphoto','sitesetting','address','productimage','productvideo'
    ]
    print("=== DATABASE STATS ===")
    for t in tables:
        try:
            n = db.session.execute(db.text("SELECT COUNT(*) FROM `" + t + "`")).scalar()
            print(f"  {t:<22} {n} rows")
        except Exception as e:
            print(f"  {t:<22} ERROR: {e}")

    # Key stats
    print("\n=== KEY METRICS ===")
    orders = db.session.execute(db.text("SELECT COUNT(*) FROM `order`")).scalar()
    upi = db.session.execute(db.text("SELECT COUNT(*) FROM `order` WHERE payment_method='UPI'")).scalar()
    verified = db.session.execute(db.text("SELECT COUNT(*) FROM `order` WHERE payment_status='VERIFIED'")).scalar()
    pending = db.session.execute(db.text("SELECT COUNT(*) FROM `order` WHERE payment_status='PENDING'")).scalar()
    with_tracking = db.session.execute(db.text("SELECT COUNT(*) FROM `order` WHERE tracking_number IS NOT NULL")).scalar()
    print(f"  Total orders:          {orders}")
    print(f"  UPI orders:            {upi}")
    print(f"  Payment verified:      {verified}")
    print(f"  Payment pending:       {pending}")
    print(f"  With tracking number:  {with_tracking}")

    products = db.session.execute(db.text("SELECT COUNT(*) FROM product")).scalar()
    variants = db.session.execute(db.text("SELECT COUNT(*) FROM productvariant")).scalar()
    in_stock = db.session.execute(db.text("SELECT COUNT(*) FROM productvariant WHERE quantity > 0")).scalar()
    print(f"\n  Total products:        {products}")
    print(f"  Total variants:        {variants}")
    print(f"  In-stock variants:     {in_stock}")

    users = db.session.execute(db.text("SELECT COUNT(*) FROM user")).scalar()
    wholesalers = db.session.execute(db.text("SELECT COUNT(*) FROM user WHERE role='WHOLESALER'")).scalar()
    print(f"\n  Total users:           {users}")
    print(f"  Wholesalers (B2B):     {wholesalers}")
    print(f"  B2C users:             {users - wholesalers}")
