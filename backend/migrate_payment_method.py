import sys
sys.path.insert(0, 'backend')
from app import app, db
from sqlalchemy import text
with app.app_context():
    with db.engine.connect() as conn:
        try:
            conn.execute(text("ALTER TABLE `order` ADD COLUMN payment_method VARCHAR(50) DEFAULT 'COD'"))
            conn.commit()
            print('Added payment_method column')
        except Exception as e:
            print(f'Column may already exist: {e}')
