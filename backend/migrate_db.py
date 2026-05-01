import traceback
from app import app
from models import db
from sqlalchemy import text

def run_migration():
    try:
        with app.app_context():
            print("Connecting to database...")
            # We use `order` in backticks since order is a reserved keyword in SQL
            db.session.execute(text("ALTER TABLE `order` ADD COLUMN payment_status VARCHAR(50) DEFAULT 'PENDING'"))
            db.session.commit()
            print("Migration successful! payment_status column added.")
    except Exception as e:
        print("Migration failed:")
        traceback.print_exc()

if __name__ == '__main__':
    run_migration()
