"""
Safe B2B migration — adds new columns with defaults.
Run once: python migrate_b2b.py
Idempotent: safe to run multiple times.
"""
from app import create_app
from models import db
from sqlalchemy import text, inspect

app = create_app()
with app.app_context():
    inspector = inspect(db.engine)

    # ── user.role ─────────────────────────────────────────────────────────────
    user_cols = [c['name'] for c in inspector.get_columns('user')]
    if 'role' not in user_cols:
        db.session.execute(
            text("ALTER TABLE `user` ADD COLUMN role VARCHAR(20) NOT NULL DEFAULT 'B2C'")
        )
        print('✓ Added role column to user table')
    else:
        print('· role column already exists')

    # ── productvariant.moq_b2b ────────────────────────────────────────────────
    variant_cols = [c['name'] for c in inspector.get_columns('productvariant')]
    if 'moq_b2b' not in variant_cols:
        db.session.execute(
            text('ALTER TABLE `productvariant` ADD COLUMN moq_b2b INTEGER NULL')
        )
        print('✓ Added moq_b2b column to productvariant table')
    else:
        print('· moq_b2b column already exists')

    # ── order.business_name ───────────────────────────────────────────────────
    order_cols = [c['name'] for c in inspector.get_columns('order')]
    if 'business_name' not in order_cols:
        db.session.execute(
            text('ALTER TABLE `order` ADD COLUMN business_name VARCHAR(200) NULL')
        )
        print('✓ Added business_name column to order table')
    else:
        print('· business_name column already exists')

    # ── order.gst_number ──────────────────────────────────────────────────────
    if 'gst_number' not in order_cols:
        db.session.execute(
            text('ALTER TABLE `order` ADD COLUMN gst_number VARCHAR(20) NULL')
        )
        print('✓ Added gst_number column to order table')
    else:
        print('· gst_number column already exists')

    db.session.commit()
    print('\nMigration complete. All B2B columns are in place.')
