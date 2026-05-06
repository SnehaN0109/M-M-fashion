"""
Diagnose and test WhatsApp order confirmation.
Run: python check_whatsapp.py
"""
from dotenv import load_dotenv
from pathlib import Path
load_dotenv(dotenv_path=Path(__file__).parent / ".env", override=True)

from app import create_app
from models import db
from whatsapp_service import send_order_confirmation, send_whatsapp_text, _format_phone

app = create_app()

print("=" * 55)
print("WhatsApp Diagnosis")
print("=" * 55)

with app.app_context():
    # Check last 5 orders
    rows = db.session.execute(db.text(
        "SELECT id, customer_phone, customer_name FROM `order` ORDER BY id DESC LIMIT 5"
    )).fetchall()

    print("\n[1] Recent orders and their phone numbers:")
    for r in rows:
        phone = r[1] or ""
        formatted = _format_phone(phone) if phone else "MISSING"
        print(f"  order={r[0]} name={r[2]} phone={repr(phone)} -> formatted={formatted}")

    # Test send on the most recent order
    from models import Order
    latest = Order.query.order_by(Order.id.desc()).first()
    if latest:
        print(f"\n[2] Testing send on order #{latest.id}:")
        print(f"  customer_phone = {repr(latest.customer_phone)}")
        print(f"  customer_name  = {latest.customer_name}")

        result = send_order_confirmation(latest)
        print(f"  Result: {result}")

    # Direct send test to a known number
    print("\n[3] Direct send test to 7498177669:")
    r2 = send_whatsapp_text("7498177669", "WhatsApp test from M&M Fashion - order confirmation working!")
    print(f"  Result: {r2}")

print("\n" + "=" * 55)
