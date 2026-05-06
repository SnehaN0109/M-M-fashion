"""
Verification + live test for Twilio WhatsApp integration.
Run: python test_whatsapp.py [phone_number]
  e.g. python test_whatsapp.py 9876543210
"""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load .env before importing service
load_dotenv(dotenv_path=Path(__file__).parent / ".env", override=True)

from whatsapp_service import _format_phone, build_order_confirmation, send_whatsapp_text

SEP = "=" * 55

print(SEP)
print("WhatsApp (Twilio) - Verification & Live Test")
print(SEP)

# ── 1. Credentials ────────────────────────────────────────────
print("\n[1] Credentials in .env:")
sid   = os.getenv("TWILIO_ACCOUNT_SID",   "")
token = os.getenv("TWILIO_AUTH_TOKEN",    "")
frm   = os.getenv("TWILIO_WHATSAPP_FROM", "")

def masked(v):
    return v[:6] + "..." + v[-4:] if len(v) > 10 else "(empty)"

print("  TWILIO_ACCOUNT_SID    :", masked(sid)   if sid   else "NOT SET")
print("  TWILIO_AUTH_TOKEN     :", masked(token) if token else "NOT SET")
print("  TWILIO_WHATSAPP_FROM  :", frm           if frm   else "NOT SET")
creds_ok = bool(sid and token and frm)
print("  Status:", "READY" if creds_ok else "MISSING - add to backend/.env")

# ── 2. Phone normalisation ────────────────────────────────────
print("\n[2] Phone normalisation:")
cases = [
    ("9876543210",      "919876543210"),
    ("+91 98765 43210", "919876543210"),
    ("919876543210",    "919876543210"),
    ("+919876543210",   "919876543210"),
]
all_ok = True
for raw, expected in cases:
    result = _format_phone(raw)
    ok = result == expected
    if not ok:
        all_ok = False
    print("  {:4}  {!r:25} -> {}".format("OK" if ok else "FAIL", raw, result))
print("  Result:", "ALL PASS" if all_ok else "SOME FAILED")

# ── 3. Message preview ────────────────────────────────────────
print("\n[3] Message preview (ASCII-safe for console):")

class _Variant:
    class product:
        name = "Cotton Saree"

class _Item:
    variant = _Variant()
    quantity = 2
    price_at_purchase = 700.0

class _Order:
    id = 99
    status = "PLACED"
    total_amount = 1499.0
    payment_method = "COD"
    customer_phone = "9876543210"
    user = None
    items = [_Item()]

msg = build_order_confirmation(_Order())
# Print safely on Windows cp1252 console
print(msg.encode("ascii", "replace").decode("ascii"))

# ── 4. Live send ──────────────────────────────────────────────
print("\n[4] Live send:")
if not creds_ok:
    print("  SKIPPED - credentials not set.")
else:
    # Accept phone from command line arg or env var
    test_phone = ""
    if len(sys.argv) > 1:
        test_phone = sys.argv[1].strip()
    if not test_phone:
        test_phone = os.getenv("TEST_WHATSAPP_NUMBER", "").strip()

    if not test_phone:
        print("  No test number provided.")
        print("  Usage: python test_whatsapp.py 9876543210")
        print("  Or set TEST_WHATSAPP_NUMBER=9876543210 in .env")
    else:
        formatted = _format_phone(test_phone)
        print("  Sending to: whatsapp:+{}".format(formatted))
        result = send_whatsapp_text(test_phone, msg)
        if result["success"]:
            print("  SUCCESS - SID:", result["sid"])
            print("  Check your WhatsApp now!")
        else:
            detail_safe = str(result["detail"]).encode("ascii", "replace").decode("ascii")
            print("  FAILED -", detail_safe)

# ── 5. orders.py integration ──────────────────────────────────
print("\n[5] orders.py integration:")
src = Path("routes/orders.py").read_text()
checks = {
    "imports send_order_confirmation":  "from whatsapp_service import send_order_confirmation" in src,
    "calls send_order_confirmation":    "send_order_confirmation(order)" in src,
    "wrapped in try/except":            "try:" in src and "send_order_confirmation(order)" in src,
    "except passes silently":           "except Exception:" in src and "pass" in src,
    "notify-whatsapp endpoint exists":  "notify-whatsapp" in src,
}
for label, passed in checks.items():
    print("  {:4}  {}".format("OK" if passed else "FAIL", label))

print("\n" + SEP)
print("Done.")
print(SEP)
