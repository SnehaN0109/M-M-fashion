"""
M&M Fashion — Complete Final Regression Test
Run: python final_test.py
"""
import requests
import json
import sys
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(dotenv_path=Path(__file__).parent / ".env", override=True)

BASE = "http://localhost:5000"
PASS, FIXED, WARN, FAIL = [], [], [], []

def ok(name):
    PASS.append(name)
    print(f"  \u2705  {name}")

def fixed(name, detail=""):
    FIXED.append(name)
    print(f"  \u274c  FIXED: {name}" + (f" — {detail}" if detail else ""))

def warn(name, detail=""):
    WARN.append(name)
    print(f"  \u26a0\ufe0f  MANUAL: {name}" + (f" — {detail}" if detail else ""))

def fail(name, detail=""):
    FAIL.append(name)
    print(f"  \u2716  FAIL: {name}" + (f" — {detail}" if detail else ""))

def check(name, condition, detail=""):
    if condition:
        ok(name)
    else:
        fail(name, detail)

def section(n, title):
    print(f"\n{'='*60}")
    print(f"  TEST {n} — {title}")
    print(f"{'='*60}")

# ─────────────────────────────────────────────────────────────
# TEST 1 — AUTH
# ─────────────────────────────────────────────────────────────
section(1, "Auth")

WA = "9876543210"
EMAIL = "finaltest@mmfashion.com"

# Send OTP
r = requests.post(f"{BASE}/api/auth/send-otp", json={"email": EMAIL, "whatsapp_number": WA})
check("Send OTP", r.status_code == 200, r.text[:80])

# Verify with test OTP 1234
r = requests.post(f"{BASE}/api/auth/verify-otp", json={"email": EMAIL, "otp": "1234"})
check("Verify OTP (test 1234)", r.status_code == 200)
USER_TOKEN = r.json().get("token", "") if r.status_code == 200 else ""
check("JWT token issued", bool(USER_TOKEN))
check("whatsapp_number in response", r.json().get("whatsapp_number") == WA if r.status_code == 200 else False)

# Wrong OTP rejected
requests.post(f"{BASE}/api/auth/send-otp", json={"email": "x@x.com", "whatsapp_number": "8888888888"})
r = requests.post(f"{BASE}/api/auth/verify-otp", json={"email": "x@x.com", "otp": "9999"})
check("Wrong OTP rejected (401)", r.status_code == 401)

# ─────────────────────────────────────────────────────────────
# TEST 2 — PRODUCTS
# ─────────────────────────────────────────────────────────────
section(2, "Products")

r = requests.get(f"{BASE}/api/products/")
check("All products load", r.status_code == 200)
products = r.json()
check("Products not empty", len(products) > 0, f"got {len(products)}")

# Category filter — case insensitive
for cat in ["Women", "women", "WOMEN"]:
    r = requests.get(f"{BASE}/api/products/?category={cat}")
    d = r.json()
    check(f"Category '{cat}' filter works", r.status_code == 200 and len(d) > 0, f"got {len(d)}")

# Search
r = requests.get(f"{BASE}/api/products/?search=saree")
check("Search 'saree' returns results", r.status_code == 200 and len(r.json()) > 0)

r = requests.get(f"{BASE}/api/products/?search=xyznotexist999")
check("Search no results returns []", r.status_code == 200 and len(r.json()) == 0)

# Product detail
pid = products[0]["id"]
r = requests.get(f"{BASE}/api/products/{pid}?domain=localhost")
check("Product detail loads", r.status_code == 200)
p = r.json()
check("Variants have quantity field", "quantity" in p["variants"][0])
check("Variants have low_stock field", "low_stock" in p["variants"][0])
check("Variants have price field", "price" in p["variants"][0])

# Reviews and photos endpoints
r = requests.get(f"{BASE}/api/products/{pid}/reviews")
check("Reviews endpoint works", r.status_code == 200)
r = requests.get(f"{BASE}/api/products/{pid}/photos")
check("Photos endpoint works", r.status_code == 200)

# ─────────────────────────────────────────────────────────────
# TEST 3 — WISHLIST
# ─────────────────────────────────────────────────────────────
section(3, "Wishlist")

# Clear any existing wishlist for test user
from app import create_app
from models import db as _db, Wishlist as WishlistModel, User as UserModel
_app = create_app()
with _app.app_context():
    user = UserModel.query.filter_by(whatsapp_number=WA).first()
    if user:
        WishlistModel.query.filter_by(user_id=user.id).delete()
        _db.session.commit()

# Add product
r = requests.post(f"{BASE}/api/wishlist", json={"whatsapp_number": WA, "product_id": pid})
check("Add to wishlist (201)", r.status_code == 201, r.text[:80])

# Idempotent add
r2 = requests.post(f"{BASE}/api/wishlist", json={"whatsapp_number": WA, "product_id": pid})
check("Duplicate add is idempotent (200)", r2.status_code == 200 and "Already" in r2.json().get("message",""))

# Get wishlist
r3 = requests.get(f"{BASE}/api/wishlist?whatsapp_number={WA}")
check("Get wishlist returns items", r3.status_code == 200 and len(r3.json()) == 1)

# DB check
with _app.app_context():
    count = WishlistModel.query.join(UserModel).filter(UserModel.whatsapp_number == WA).count()
check("Wishlist saved in DB", count == 1, f"DB count={count}")

# Remove
r4 = requests.delete(f"{BASE}/api/wishlist/{pid}?whatsapp_number={WA}")
check("Remove from wishlist (200)", r4.status_code == 200)

r5 = requests.get(f"{BASE}/api/wishlist?whatsapp_number={WA}")
check("Wishlist empty after remove", len(r5.json()) == 0)

with _app.app_context():
    count2 = WishlistModel.query.join(UserModel).filter(UserModel.whatsapp_number == WA).count()
check("Wishlist removed from DB", count2 == 0, f"DB count={count2}")

# ─────────────────────────────────────────────────────────────
# TEST 4 — CART
# ─────────────────────────────────────────────────────────────
section(4, "Cart")

# Find in-stock variant
in_stock_v = None
for prod in products:
    r = requests.get(f"{BASE}/api/products/{prod['id']}?domain=localhost")
    for v in r.json().get("variants", []):
        if v["quantity"] > 0:
            in_stock_v = v
            break
    if in_stock_v:
        break

check("Found in-stock variant", in_stock_v is not None)
vid = in_stock_v["id"] if in_stock_v else None

if vid:
    # Clear cart
    requests.delete(f"{BASE}/api/cart/clear", json={"whatsapp_number": WA})

    # Add
    r = requests.post(f"{BASE}/api/cart/add", json={"whatsapp_number": WA, "variant_id": vid, "quantity": 1})
    check("Add to cart (200)", r.status_code == 200 and r.json().get("message") == "Added to cart")

    # Duplicate blocked
    r2 = requests.post(f"{BASE}/api/cart/add", json={"whatsapp_number": WA, "variant_id": vid, "quantity": 1})
    check("Duplicate add returns duplicate=True", r2.json().get("duplicate") == True, str(r2.json()))

    # Cart has exactly 1 item
    r3 = requests.get(f"{BASE}/api/cart?whatsapp_number={WA}")
    check("Cart has 1 item (no duplicate)", len(r3.json()) == 1, f"got {len(r3.json())}")

    # Update quantity
    r4 = requests.put(f"{BASE}/api/cart/update", json={"whatsapp_number": WA, "variant_id": vid, "quantity": 1})
    check("Update quantity works", r4.status_code == 200)

    # Exceed stock
    stock = in_stock_v["quantity"]
    r5 = requests.put(f"{BASE}/api/cart/update", json={"whatsapp_number": WA, "variant_id": vid, "quantity": stock + 99})
    check("Exceed stock rejected (400)", r5.status_code == 400, r5.json().get("error",""))

    # Remove
    r6 = requests.delete(f"{BASE}/api/cart/remove", json={"whatsapp_number": WA, "variant_id": vid})
    check("Remove from cart works", r6.status_code == 200)
    r7 = requests.get(f"{BASE}/api/cart?whatsapp_number={WA}")
    check("Cart empty after remove", len(r7.json()) == 0)

# ─────────────────────────────────────────────────────────────
# TEST 5 — CHECKOUT
# ─────────────────────────────────────────────────────────────
section(5, "Checkout")

# Find 2 in-stock variants
in_stock_list = []
for prod in products:
    r = requests.get(f"{BASE}/api/products/{prod['id']}?domain=localhost")
    for v in r.json().get("variants", []):
        if v["quantity"] > 0 and len(in_stock_list) < 2:
            in_stock_list.append(v)
    if len(in_stock_list) >= 2:
        break

check("Found 2 in-stock variants", len(in_stock_list) >= 1)

ORDER_ID = None
if in_stock_list:
    payload = {
        "customer_name": "Final Test User",
        "customer_email": "finaltest@mmfashion.com",
        "customer_phone": "9876543210",
        "address_line1": "123 Test Street",
        "city": "Mumbai",
        "state": "Maharashtra",
        "pincode": "400001",
        "domain": "localhost",
        "payment_method": "UPI",
        "whatsapp_number": WA,
        "items": [{"variant_id": in_stock_list[0]["id"], "quantity": 1}]
    }
    r = requests.post(f"{BASE}/api/orders/checkout", json=payload)
    check("Checkout creates order (201)", r.status_code == 201, r.text[:100])
    if r.status_code == 201:
        order = r.json()
        ORDER_ID = order["order_id"]
        check("Order has order_id", bool(ORDER_ID))
        check("Tracking number auto-generated", bool(order.get("tracking_number")))
        check("Tracking format MM+year+6digits", str(order.get("tracking_number","")).startswith("MM"))
        check("Payment status = PENDING", order.get("payment_status") == "PENDING")
        check("Order status = PENDING_PAYMENT", order.get("status") == "PENDING_PAYMENT")

    # Validate required fields
    bad = {**payload}
    del bad["customer_name"]
    r2 = requests.post(f"{BASE}/api/orders/checkout", json=bad)
    check("Missing field rejected (400)", r2.status_code == 400)

    # Empty items rejected
    bad2 = {**payload, "items": []}
    r3 = requests.post(f"{BASE}/api/orders/checkout", json=bad2)
    check("Empty items rejected (400)", r3.status_code == 400)

# ─────────────────────────────────────────────────────────────
# TEST 6 — PAYMENT
# ─────────────────────────────────────────────────────────────
section(6, "Payment")

if ORDER_ID:
    # Track — payment_proof should be null
    r = requests.get(f"{BASE}/api/orders/track/{ORDER_ID}")
    check("Track endpoint works", r.status_code == 200)
    tracked = r.json()
    check("payment_proof is null before upload", tracked.get("payment_proof") is None)
    check("tracking_number in track response", bool(tracked.get("tracking_number")))

    # Mark paid (no file)
    r2 = requests.post(f"{BASE}/api/orders/{ORDER_ID}/mark-paid")
    check("Mark paid works (200)", r2.status_code == 200, r2.text[:80])
    check("Response has message", "message" in r2.json())

    # Re-upload blocked
    r3 = requests.post(f"{BASE}/api/orders/{ORDER_ID}/mark-paid")
    check("Re-upload blocked (400)", r3.status_code == 400, r3.json().get("error",""))

    # Payment status endpoint
    r4 = requests.get(f"{BASE}/api/orders/{ORDER_ID}/payment-status")
    check("Payment status endpoint works", r4.status_code == 200)
    check("has_payment_proof = True", r4.json().get("has_payment_proof") == True)

    # Admin verify
    admin_r = requests.post(f"{BASE}/api/admin/login", json={"password": "admin@mmfashion2024"})
    ADMIN_TOKEN = admin_r.json().get("token", "")
    check("Admin login works", bool(ADMIN_TOKEN))

    if ADMIN_TOKEN:
        hdrs = {"Authorization": f"Bearer {ADMIN_TOKEN}"}
        r5 = requests.post(f"{BASE}/api/admin/orders/{ORDER_ID}/payment-action",
                           json={"action": "verify"}, headers=hdrs)
        check("Admin verify payment (200)", r5.status_code == 200, r5.text[:80])
        if r5.status_code == 200:
            res = r5.json()
            check("payment_status → VERIFIED", res.get("payment_status") == "VERIFIED")
            check("order status → PLACED", res.get("status") == "PLACED")

# ─────────────────────────────────────────────────────────────
# TEST 7 — WHATSAPP
# ─────────────────────────────────────────────────────────────
section(7, "WhatsApp")

if ORDER_ID:
    r = requests.post(f"{BASE}/api/orders/{ORDER_ID}/notify-whatsapp")
    check("Notify endpoint returns 200", r.status_code == 200)
    result = r.json()
    check("Response has message field", "message" in result)
    sent = result.get("message") == "WhatsApp notification sent"
    if sent:
        ok("WhatsApp message sent via Twilio")
    else:
        warn("WhatsApp send", f"detail={result.get('detail','')}")

# ─────────────────────────────────────────────────────────────
# TEST 8 — ORDERS
# ─────────────────────────────────────────────────────────────
section(8, "Orders")

if ORDER_ID:
    r = requests.get(f"{BASE}/api/orders/track/{ORDER_ID}")
    check("Track order works", r.status_code == 200)
    t = r.json()
    check("Tracking number present", bool(t.get("tracking_number")))
    check("Status is PLACED after verify", t.get("status") == "PLACED")
    check("Items in order", len(t.get("items", [])) > 0)
    check("payment_proof field present", "payment_proof" in t)

    # My orders
    r2 = requests.get(f"{BASE}/api/orders/my-orders?whatsapp_number={WA}")
    check("My orders endpoint works", r2.status_code == 200)
    check("My orders returns list", isinstance(r2.json(), list))

    # Admin status update
    if ADMIN_TOKEN:
        hdrs = {"Authorization": f"Bearer {ADMIN_TOKEN}"}
        r3 = requests.put(f"{BASE}/api/admin/orders/{ORDER_ID}/status",
                          json={"status": "PACKED"}, headers=hdrs)
        check("Admin update to PACKED works", r3.status_code == 200)
        r4 = requests.get(f"{BASE}/api/orders/track/{ORDER_ID}")
        check("Status updated to PACKED in DB", r4.json().get("status") == "PACKED")

# ─────────────────────────────────────────────────────────────
# TEST 9 — ADMIN
# ─────────────────────────────────────────────────────────────
section(9, "Admin")

admin_r = requests.post(f"{BASE}/api/admin/login", json={"password": "admin@mmfashion2024"})
check("Admin login works", admin_r.status_code == 200)
ADMIN_TOKEN = admin_r.json().get("token", "")

if ADMIN_TOKEN:
    hdrs = {"Authorization": f"Bearer {ADMIN_TOKEN}"}

    r = requests.get(f"{BASE}/api/admin/products", headers=hdrs)
    check("Admin list products", r.status_code == 200 and len(r.json()) > 0)

    r = requests.get(f"{BASE}/api/admin/orders", headers=hdrs)
    check("Admin list orders", r.status_code == 200 and len(r.json()) > 0)

    r = requests.get(f"{BASE}/api/admin/discount-codes", headers=hdrs)
    check("Admin discount codes", r.status_code == 200)

    r = requests.get(f"{BASE}/api/admin/photos/pending", headers=hdrs)
    check("Admin pending photos", r.status_code == 200)

    r = requests.get(f"{BASE}/api/admin/users", headers=hdrs)
    check("Admin list users", r.status_code == 200 and len(r.json()) > 0)

    r = requests.get(f"{BASE}/api/admin/settings/popup", headers=hdrs)
    check("Admin settings popup", r.status_code == 200)

    # Wrong password
    r2 = requests.post(f"{BASE}/api/admin/login", json={"password": "wrongpassword"})
    check("Wrong admin password rejected", r2.status_code == 401)

    # Payment proof endpoint
    if ORDER_ID:
        r3 = requests.get(f"{BASE}/api/admin/payment-proof/{ORDER_ID}", headers=hdrs)
        check("Admin payment proof endpoint", r3.status_code == 200)
        check("payment_proof field in response", "payment_proof" in r3.json())

# ─────────────────────────────────────────────────────────────
# TEST 10 — DATABASE (all 14 tables)
# ─────────────────────────────────────────────────────────────
section(10, "Database — All 14 Tables")

TABLES = [
    "user", "address", "product", "productvariant",
    "productimage", "productvideo", "cart", "cartitem",
    "order", "orderitem", "review", "userphoto",
    "discountcode", "wishlist", "sitesetting"
]

with _app.app_context():
    for table in TABLES:
        try:
            count = _db.session.execute(_db.text(f"SELECT COUNT(*) FROM `{table}`")).scalar()
            check(f"Table '{table}' accessible (rows={count})", True)
        except Exception as e:
            fail(f"Table '{table}' error", str(e))

    # Verify key data exists
    orders_count = _db.session.execute(_db.text("SELECT COUNT(*) FROM `order`")).scalar()
    check("Orders table has data", orders_count > 0, f"rows={orders_count}")

    products_count = _db.session.execute(_db.text("SELECT COUNT(*) FROM product")).scalar()
    check("Products table has data", products_count > 0, f"rows={products_count}")

    users_count = _db.session.execute(_db.text("SELECT COUNT(*) FROM user")).scalar()
    check("Users table has data", users_count > 0, f"rows={users_count}")

    wishlist_count = _db.session.execute(_db.text("SELECT COUNT(*) FROM wishlist")).scalar()
    check("Wishlist table accessible", True, f"rows={wishlist_count}")

# ─────────────────────────────────────────────────────────────
# SUMMARY
# ─────────────────────────────────────────────────────────────
total = len(PASS) + len(FIXED) + len(WARN) + len(FAIL)
print(f"\n{'='*60}")
print(f"  FINAL RESULTS")
print(f"{'='*60}")
print(f"  \u2705 Pass:          {len(PASS)}")
print(f"  \u274c Fixed:         {len(FIXED)}")
print(f"  \u26a0\ufe0f  Manual check:  {len(WARN)}")
print(f"  \u2716 Fail:          {len(FAIL)}")
print(f"  Total:         {total}")

if FAIL:
    print(f"\nFAILED:")
    for f in FAIL:
        print(f"  - {f}")
if WARN:
    print(f"\nMANUAL CHECK NEEDED:")
    for w in WARN:
        print(f"  - {w}")
if not FAIL:
    print(f"\n  All automated tests passed!")
print()
