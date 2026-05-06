from app import create_app
from models import db

app = create_app()
with app.app_context():
    # Check column exists
    rows = db.session.execute(db.text("SHOW COLUMNS FROM `order` LIKE 'tracking_number'")).fetchall()
    print("tracking_number column:", rows)

    # Check a sample of recent orders
    orders = db.session.execute(db.text(
        "SELECT id, payment_method, payment_status, tracking_number FROM `order` ORDER BY id DESC LIMIT 10"
    )).fetchall()
    print("\nRecent orders:")
    for o in orders:
        print(f"  id={o[0]} method={o[1]} pay_status={o[2]} tracking={o[3]}")
