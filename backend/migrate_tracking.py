"""
Migration: Add UNIQUE constraint to tracking_number + backfill existing orders.

Safe to run multiple times (idempotent).
"""
from app import create_app
from models import db
from utils import generate_tracking_number

app = create_app()

with app.app_context():
    # ── Step 1: Add UNIQUE constraint if not already present ─────────────────
    try:
        db.session.execute(db.text(
            "ALTER TABLE `order` MODIFY COLUMN tracking_number VARCHAR(100) NULL"
        ))
        db.session.execute(db.text(
            "ALTER TABLE `order` ADD UNIQUE INDEX uq_tracking_number (tracking_number)"
        ))
        db.session.commit()
        print("✓ UNIQUE constraint added to tracking_number")
    except Exception as e:
        db.session.rollback()
        if 'Duplicate key name' in str(e) or 'already exists' in str(e).lower():
            print("✓ UNIQUE constraint already exists — skipping")
        else:
            print(f"  Note: {e}")

    # ── Step 2: Backfill COD orders that have no tracking number ─────────────
    cod_no_tracking = db.session.execute(db.text(
        "SELECT id FROM `order` WHERE payment_method = 'COD' AND tracking_number IS NULL"
    )).fetchall()

    print(f"\nBackfilling {len(cod_no_tracking)} COD orders with no tracking number...")
    for row in cod_no_tracking:
        order_id = row[0]
        tracking = generate_tracking_number(order_id)
        db.session.execute(db.text(
            "UPDATE `order` SET tracking_number = :t, status = CASE WHEN status = 'PENDING_PAYMENT' THEN 'PLACED' ELSE status END WHERE id = :id"
        ), {"t": tracking, "id": order_id})
        print(f"  Order #{order_id} → {tracking}")

    db.session.commit()
    print("✓ COD backfill complete")

    # ── Step 3: Backfill UPI VERIFIED orders with no tracking number ──────────
    upi_verified_no_tracking = db.session.execute(db.text(
        "SELECT id FROM `order` WHERE payment_method = 'UPI' AND payment_status = 'VERIFIED' AND tracking_number IS NULL"
    )).fetchall()

    print(f"\nBackfilling {len(upi_verified_no_tracking)} verified UPI orders with no tracking number...")
    for row in upi_verified_no_tracking:
        order_id = row[0]
        tracking = generate_tracking_number(order_id)
        db.session.execute(db.text(
            "UPDATE `order` SET tracking_number = :t WHERE id = :id"
        ), {"t": tracking, "id": order_id})
        print(f"  Order #{order_id} → {tracking}")

    db.session.commit()
    print("✓ UPI verified backfill complete")

    # ── Step 4: Final summary ─────────────────────────────────────────────────
    total = db.session.execute(db.text("SELECT COUNT(*) FROM `order`")).scalar()
    with_tracking = db.session.execute(db.text("SELECT COUNT(*) FROM `order` WHERE tracking_number IS NOT NULL")).scalar()
    without_tracking = db.session.execute(db.text("SELECT COUNT(*) FROM `order` WHERE tracking_number IS NULL")).scalar()

    print(f"\n── Summary ──────────────────────────────")
    print(f"  Total orders:          {total}")
    print(f"  With tracking number:  {with_tracking}")
    print(f"  Without (UPI pending): {without_tracking}")
    print(f"────────────────────────────────────────")
    print("Migration complete.")
