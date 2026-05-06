import requests
import time
import sys
import json

BASE_URL = "http://localhost:5000"
VERBOSE = "--verbose" in sys.argv

def log_verbose(method, url, res):
    if VERBOSE:
        print(f"\n[VERBOSE] {method} {url}")
        print(f"[VERBOSE] Status: {res.status_code}")
        try:
            print(f"[VERBOSE] Response: {json.dumps(res.json(), indent=2)}")
        except:
            print(f"[VERBOSE] Response: {res.text[:200]}")

results = []

def run_test(name, func):
    start = time.time()
    try:
        func()
        duration = int((time.time() - start) * 1000)
        print(f"[PASS] {name:<30} ({duration}ms)")
        results.append((name, True, duration, None))
    except Exception as e:
        duration = int((time.time() - start) * 1000)
        print(f"[FAIL] {name:<30}")
        safe_msg = str(e).encode('ascii', 'ignore').decode('ascii')
        print(f"   -> {safe_msg[:500]}...")
        results.append((name, False, duration, str(e)))

# Global state
state = {}
timestamp = int(time.time())
test_phone = f"+91999{timestamp % 10000000:07d}"

def test_health_check():
    # Hit products as health check
    res = requests.get(f"{BASE_URL}/api/products")
    log_verbose("GET", f"{BASE_URL}/api/products", res)
    assert res.status_code == 200, f"Expected 200, got {res.status_code}"

def test_user_reg_login():
    email = f"test_mmfashion_{timestamp}@test.com"
    # Send OTP
    res = requests.post(f"{BASE_URL}/api/auth/send-otp", json={
        "email": email,
        "phone_number": test_phone
    })
    log_verbose("POST", "/api/auth/send-otp", res)
    assert res.status_code == 200, f"Send OTP failed: {res.text}"
    
    # Verify OTP (hardcoded 1234)
    res = requests.post(f"{BASE_URL}/api/auth/verify-otp", json={
        "email": email,
        "otp": "1234"
    })
    log_verbose("POST", "/api/auth/verify-otp", res)
    assert res.status_code == 200, f"Verify OTP failed: {res.text}"
    data = res.json()
    assert "token" in data, "No token returned"
    state["user_token"] = data["token"]
    state["user_phone"] = data["phone_number"]

def test_admin_login():
    res = requests.post(f"{BASE_URL}/api/admin/login", json={"password": "admin@mmfashion2024"})
    log_verbose("POST", "/api/admin/login", res)
    assert res.status_code == 200, f"Admin login failed: {res.text}"
    data = res.json()
    assert "token" in data, "No admin token returned"
    state["admin_token"] = data["token"]
    
    # Verify on protected route
    res = requests.get(f"{BASE_URL}/api/admin/orders", headers={"Authorization": f"Bearer {state['admin_token']}"})
    log_verbose("GET", "/api/admin/orders", res)
    assert res.status_code == 200, "Admin token didn't work on protected route"

def test_product_catalog():
    res = requests.get(f"{BASE_URL}/api/products")
    log_verbose("GET", "/api/products", res)
    assert res.status_code == 200, "Products list failed"
    products = res.json()
    assert len(products) > 0, "No products returned"
    
    # Filter
    res = requests.get(f"{BASE_URL}/api/products?category=Women")
    log_verbose("GET", "/api/products?category=Women", res)
    assert res.status_code == 200, "Filtered products list failed"
    
    # Single product with variant stock > 0
    variant_id = 1
    for p in products:
        res = requests.get(f"{BASE_URL}/api/products/{p['id']}")
        data = res.json()
        if "variants" in data:
            for v in data["variants"]:
                # The quantity in variant might be 'quantity' or 'stock'
                if v.get("quantity", 0) > 2 or v.get("stock", 0) > 2:
                    state["test_product_id"] = p["id"]
                    variant_id = v["id"]
                    break
        if "test_product_id" in state:
            break
    state["test_variant_id"] = variant_id

def test_cart_operations():
    var_id = state.get("test_variant_id", 1)
    
    # Add
    res = requests.post(f"{BASE_URL}/api/cart/add", json={
        "phone_number": state["user_phone"],
        "variant_id": var_id,
        "quantity": 1
    })
    log_verbose("POST", "/api/cart/add", res)
    assert res.status_code == 200, f"Add to cart failed: {res.text}"
    
    # Check
    res = requests.get(f"{BASE_URL}/api/cart", params={"phone_number": state["user_phone"]})
    log_verbose("GET", "/api/cart", res)
    assert res.status_code == 200, "Get cart failed"
    cart_items = res.json()
    assert len(cart_items) > 0, "Cart is empty"
    item_id = cart_items[0]["cart_item_id"]
    
    # Update
    res = requests.put(f"{BASE_URL}/api/cart/update", json={
        "phone_number": state["user_phone"],
        "variant_id": var_id,
        "quantity": 2
    })
    log_verbose("PUT", "/api/cart/update", res)
    assert res.status_code == 200, f"Update cart failed: {res.text}"
    
    # Remove
    res = requests.delete(f"{BASE_URL}/api/cart/remove", json={
        "phone_number": state["user_phone"],
        "variant_id": var_id
    })
    log_verbose("DELETE", "/api/cart/remove", res)
    assert res.status_code == 200, f"Remove from cart failed: {res.text}"

def test_full_order_placement():
    var_id = state.get("test_variant_id", 1)
    # Add item back for order
    requests.post(f"{BASE_URL}/api/cart/add", json={"phone_number": state["user_phone"], "variant_id": var_id, "quantity": 1})
    
    payload = {
        "customer_name": "Test Order User",
        "customer_email": f"test_{timestamp}@example.com",
        "customer_phone": state["user_phone"],
        "address_line1": "123 Main St",
        "city": "Mumbai",
        "state": "Maharashtra",
        "pincode": "400001",
        "items": [{"variant_id": var_id, "quantity": 1}],
        "domain": "garba.shop",
        "phone_number": state["user_phone"]
    }
    res = requests.post(f"{BASE_URL}/api/orders/checkout", json=payload)
    log_verbose("POST", "/api/orders/checkout", res)
    assert res.status_code == 201, f"Checkout failed: {res.text}"
    data = res.json()
    assert "order_id" in data, "No order_id in checkout response"
    state["test_order_id"] = data["order_id"]
    
    # User orders
    res = requests.get(f"{BASE_URL}/api/orders/my-orders", params={"phone_number": state["user_phone"]})
    log_verbose("GET", "/api/orders/my-orders", res)
    assert res.status_code == 200, "Failed to get my orders"
    orders = res.json()
    assert any(o["order_id"] == state["test_order_id"] for o in orders), "Order not found in user orders"

def test_payment_proof_upload():
    order_id = state["test_order_id"]
    files = {'proof': ('test.jpg', b'dummy content', 'image/jpeg')}
    res = requests.post(f"{BASE_URL}/api/orders/{order_id}/mark-paid", files=files)
    log_verbose("POST", f"/api/orders/{order_id}/mark-paid", res)
    assert res.status_code == 200, f"Proof upload failed: {res.text}"
    
    # Verify status changed
    res = requests.get(f"{BASE_URL}/api/orders/track/{order_id}")
    log_verbose("GET", f"/api/orders/track/{order_id}", res)
    assert res.json().get("status") in ["PAID", "PROOF_SUBMITTED"], f"Unexpected status: {res.json().get('status')}"

def test_admin_payment_verification():
    order_id = state["test_order_id"]
    payload = {
        "status": "PLACED",
        "payment_status": "VERIFIED",
        "tracking_number": f"TEST{timestamp}"
    }
    headers = {"Authorization": f"Bearer {state['admin_token']}"}
    res = requests.put(f"{BASE_URL}/api/admin/orders/{order_id}/status", json=payload, headers=headers)
    log_verbose("PUT", f"/api/admin/orders/{order_id}/status", res)
    assert res.status_code == 200, f"Admin update failed: {res.text}"
    data = res.json()
    assert data.get("success") is True, "Success flag not true"
    assert data["order"]["status"] == "PLACED", f"Status not PLACED, got {data['order'].get('status')}"
    
    # Track as user
    res = requests.get(f"{BASE_URL}/api/orders/track/{order_id}")
    log_verbose("GET", f"/api/orders/track/{order_id}", res)
    track_data = res.json()
    assert track_data.get("status") == "PLACED", f"User sees wrong status: {track_data.get('status')}"
    assert track_data.get("payment_status") == "VERIFIED", "User sees wrong payment_status"
    assert track_data.get("tracking_number") == f"TEST{timestamp}", "User sees wrong tracking_number"

def test_admin_order_rejection():
    var_id = state.get("test_variant_id", 1)
    requests.post(f"{BASE_URL}/api/cart/add", json={"phone_number": state["user_phone"], "variant_id": var_id, "quantity": 1})
    payload = {
        "customer_name": "Test Order User",
        "customer_email": f"test_{timestamp}@example.com",
        "customer_phone": state["user_phone"],
        "address_line1": "123 Main St",
        "city": "Mumbai",
        "state": "Maharashtra",
        "pincode": "400001",
        "items": [{"variant_id": var_id, "quantity": 1}],
        "domain": "garba.shop",
        "phone_number": state["user_phone"]
    }
    res = requests.post(f"{BASE_URL}/api/orders/checkout", json=payload)
    order_id = res.json()["order_id"]
    
    headers = {"Authorization": f"Bearer {state['admin_token']}"}
    res = requests.put(f"{BASE_URL}/api/admin/orders/{order_id}/status", json={"status": "CANCELLED", "payment_status": "FAILED"}, headers=headers)
    log_verbose("PUT", f"/api/admin/orders/{order_id}/status", res)
    assert res.status_code == 200, f"Rejection failed: {res.text}"
    
    res = requests.get(f"{BASE_URL}/api/orders/track/{order_id}")
    assert res.json().get("status") == "CANCELLED", f"Expected CANCELLED, got {res.json().get('status')}"

def test_admin_status_progression():
    order_id = state["test_order_id"]
    headers = {"Authorization": f"Bearer {state['admin_token']}"}
    statuses = ["PLACED", "PACKED", "SHIPPED", "OUT_FOR_DELIVERY", "DELIVERED"]
    
    for status in statuses:
        res = requests.put(f"{BASE_URL}/api/admin/orders/{order_id}/status", json={"status": status}, headers=headers)
        log_verbose("PUT", f"/api/admin/orders/{order_id}/status ({status})", res)
        assert res.status_code == 200, f"Failed to update to {status}"
        
        track_res = requests.get(f"{BASE_URL}/api/orders/track/{order_id}")
        assert track_res.json().get("status") == status, f"Expected {status}, got {track_res.json().get('status')}"

def test_wishlist():
    product_id = state.get("test_product_id", 1)
    payload = {"whatsapp_number": state["user_phone"], "product_id": product_id}
    res = requests.post(f"{BASE_URL}/api/wishlist", json=payload)
    log_verbose("POST", f"/api/wishlist", res)
    assert res.status_code in (200, 201), f"Add to wishlist failed: {res.text}"
    
    res = requests.get(f"{BASE_URL}/api/wishlist", params={"whatsapp_number": state["user_phone"]})
    log_verbose("GET", f"/api/wishlist", res)
    assert res.status_code == 200
    wishlist = res.json()
    assert any(w["id"] == product_id for w in wishlist), "Product not found in wishlist"
    
    res = requests.delete(f"{BASE_URL}/api/wishlist/{product_id}", json=payload)
    log_verbose("DELETE", f"/api/wishlist/{product_id}", res)
    assert res.status_code == 200, f"Remove from wishlist failed: {res.text}"

def test_edge_cases():
    # Wrong password
    res = requests.post(f"{BASE_URL}/api/admin/login", json={"password": "wrongpassword123"})
    log_verbose("POST", "/api/admin/login", res)
    assert res.status_code == 401, "Expected 401 for wrong password"
    
    # Empty cart order
    res = requests.post(f"{BASE_URL}/api/orders/checkout", json={
        "customer_name": "Test", "customer_email": "test@test.com", "customer_phone": "9999999999",
        "address_line1": "123", "city": "M", "state": "MH", "pincode": "400", "items": [], "domain": "garba.shop", "phone_number": "9999999999"
    })
    log_verbose("POST", "/api/orders/checkout", res)
    assert res.status_code == 400, "Expected 400 for empty cart"
    
    # Invalid status
    headers = {"Authorization": f"Bearer {state['admin_token']}"}
    res = requests.put(f"{BASE_URL}/api/admin/orders/{state['test_order_id']}/status", json={"status": "INVALID_STATUS"}, headers=headers)
    log_verbose("PUT", "/api/admin/orders/{}/status", res)
    assert res.status_code == 400, "Expected 400 for invalid status"
    
    # Non-existent order
    res = requests.get(f"{BASE_URL}/api/orders/track/999999")
    log_verbose("GET", "/api/orders/track/999999", res)
    assert res.status_code == 404, "Expected 404 for non-existent order"

if __name__ == "__main__":
    print("========================================")
    print("   M&M Fashion Integration Test Report  ")
    print("========================================")
    
    start_time = time.time()
    run_test("Health Check", test_health_check)
    run_test("User Registration & Login", test_user_reg_login)
    run_test("Admin Login", test_admin_login)
    run_test("Product Catalog", test_product_catalog)
    run_test("Cart Operations", test_cart_operations)
    run_test("Full Order Placement Flow", test_full_order_placement)
    run_test("Payment Proof Upload", test_payment_proof_upload)
    run_test("Admin Payment Verification", test_admin_payment_verification)
    run_test("Admin Order Rejection", test_admin_order_rejection)
    run_test("Full Status Progression", test_admin_status_progression)
    run_test("Wishlist", test_wishlist)
    run_test("Edge Cases & Invalid Inputs", test_edge_cases)
    total_time = time.time() - start_time
    
    passed = sum(1 for r in results if r[1])
    total = len(results)
    
    print("========================================")
    print(f"Results: {passed}/{total} PASSED  |  Total: {total_time:.1f}s")
    print("========================================")
    
    # Write to report file
    with open("tests/last_run_report.txt", "w", encoding="utf-8") as f:
        f.write("========================================\n")
        f.write("   M&M Fashion Integration Test Report  \n")
        f.write("========================================\n")
        for r in results:
            status = "✅ PASS" if r[1] else "❌ FAIL"
            f.write(f"{status}  {r[0]:<30} ({r[2]}ms)\n")
            if not r[1]:
                f.write(f"   → {r[3]}\n")
        f.write("========================================\n")
        f.write(f"Results: {passed}/{total} PASSED  |  Total: {total_time:.1f}s\n")
        f.write("========================================\n")

    if passed != total:
        sys.exit(1)
