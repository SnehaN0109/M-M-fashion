import sys
sys.path.insert(0, 'backend')
from app import app, db
from sqlalchemy import text

with app.app_context():
    with db.engine.connect() as conn:
        try:
            conn.execute(text("ALTER TABLE `order` ADD COLUMN payment_status VARCHAR(20) DEFAULT 'PENDING'"))
            conn.commit()
            print("✅ Added payment_status column")
        except Exception as e:
            print(f"⚠️ payment_status: {e}")
        try:
            conn.execute(text("ALTER TABLE `order` ADD COLUMN payment_proof VARCHAR(500) NULL"))
            conn.commit()
            print("✅ Added payment_proof column")
        except Exception as e:
            print(f"⚠️ payment_proof: {e}")

    print("✅ Migration complete!")
