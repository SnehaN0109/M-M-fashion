"""Add payment_proof column to order table."""
from app import create_app
from models import db

app = create_app()
with app.app_context():
    # Add the column
    try:
        db.session.execute(db.text("ALTER TABLE `order` ADD COLUMN payment_proof VARCHAR(500) NULL"))
        db.session.commit()
        print("SUCCESS: payment_proof column added")
    except Exception as e:
        if '1060' in str(e) or 'Duplicate column' in str(e):
            print("INFO: Column already exists, skipping")
            db.session.rollback()
        else:
            print(f"ERROR: {e}")
            db.session.rollback()

    # Verify
    result = db.session.execute(db.text("SHOW COLUMNS FROM `order` LIKE 'payment_proof'"))
    cols = result.fetchall()
    if cols:
        print(f"VERIFIED: payment_proof column exists - {cols[0]}")
    else:
        print("ERROR: Column not found after migration")
