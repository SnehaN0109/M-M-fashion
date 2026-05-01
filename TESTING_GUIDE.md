# 🧪 PHASE 1 TESTING GUIDE

## ✅ Servers Running

- **Backend (Flask)**: http://127.0.0.1:5000
- **Frontend (Vite)**: http://localhost:5173

---

## 🎫 Available Discount Codes

Use these codes for testing:

| Code | Type | Discount | Status |
|------|------|----------|--------|
| **FIRST10** | Percentage + Flat | 10% + ₹100 | ✅ Active |
| **MYFASHION1** | Percentage + Flat | 20% + ₹200 | ✅ Active |
| **SAVE20** | Percentage + Flat | 10% + ₹100 | ✅ Active |
| ~~SAVE10~~ | Percentage + Flat | 10% + ₹100 | ❌ Inactive |

**Recommended for testing:** Use `FIRST10` or `MYFASHION1`

---

## 📋 Test Scenarios

### ✅ TEST 1: Product Detail Page (No Discount Input)

**Steps:**
1. Open http://localhost:5173
2. Click on any product (e.g., "Women Navratri Ghagara")
3. Scroll through the product page

**Expected Result:**
- ✅ Product images, name, price visible
- ✅ Color and size selectors visible
- ✅ Add to Cart button visible
- ✅ **NO discount code input field anywhere**
- ✅ Clean, professional product page

**Pass Criteria:** No discount input visible on product page

---

### ✅ TEST 2: Add to Cart Flow

**Steps:**
1. On product detail page
2. Select a color (click on color circle)
3. Select a size (click on size button)
4. Click "Add to Cart"
5. Click on cart icon in header

**Expected Result:**
- ✅ Product added to cart successfully
- ✅ Cart page opens
- ✅ Product visible in cart with correct details

**Pass Criteria:** Product successfully added to cart

---

### ✅ TEST 3: Apply Discount in Cart (Success)

**Steps:**
1. Go to Cart page (http://localhost:5173/cart)
2. Ensure you have at least one item in cart
3. Scroll to "Price Details" section on the right
4. Find "Coupon Code" input field
5. Enter: `FIRST10`
6. Click "Apply" button

**Expected Result:**
- ✅ Green success message: "✓ Coupon applied!"
- ✅ Discount line appears in price breakdown
- ✅ Shows: "Discount (FIRST10)" with amount
- ✅ Total price reduced by discount amount
- ✅ "You save ₹X on this order!" message appears

**Pass Criteria:** Discount successfully applied and visible in cart

---

### ✅ TEST 4: Invalid Discount Code

**Steps:**
1. In Cart page
2. Enter: `INVALID123`
3. Click "Apply"

**Expected Result:**
- ❌ Red error message appears
- ❌ No discount applied
- ❌ Total price unchanged

**Pass Criteria:** Error message shown for invalid code

---

### ✅ TEST 5: Discount Carried to Checkout (CRITICAL TEST)

**Steps:**
1. In Cart page with discount applied (from TEST 3)
2. Note the discount code and amount (e.g., FIRST10, ₹100)
3. Note the total amount (e.g., ₹1698)
4. Click "Proceed to Checkout" button

**Expected Result:**
- ✅ Checkout page opens
- ✅ **Green box appears** with heading "Discount Applied"
- ✅ Shows: "Code: FIRST10 — You save ₹100"
- ✅ Shows message: "💡 To change discount code, go back to cart"
- ✅ **NO discount input field** on checkout page
- ✅ Price breakdown shows discount amount
- ✅ Total matches cart total exactly

**Pass Criteria:** Discount from cart is visible in checkout (read-only)

---

### ✅ TEST 6: Checkout Without Discount

**Steps:**
1. Go to Cart page
2. Do NOT apply any discount code
3. Click "Proceed to Checkout"

**Expected Result:**
- ✅ Checkout page opens
- ✅ **NO green discount box** appears
- ✅ **NO discount input field** appears
- ✅ Price breakdown shows no discount
- ✅ Total is full price (no discount)

**Pass Criteria:** Checkout works fine without discount

---

### ✅ TEST 7: Complete Order with Discount

**Steps:**
1. In Checkout page with discount applied
2. Fill in all required fields:
   - Full Name: `Test User`
   - Email: `test@example.com`
   - Phone: `9876543210`
   - Address Line 1: `123 Test Street`
   - City: `Mumbai`
   - State: `Maharashtra`
   - Pincode: `400001`
3. Click "Place Order"

**Expected Result:**
- ✅ Order placed successfully
- ✅ Redirected to Order Success page
- ✅ Order confirmation shown
- ✅ Order includes discount code

**Pass Criteria:** Order placed with discount successfully

---

### ✅ TEST 8: Mobile Responsive (Bonus)

**Steps:**
1. Open browser DevTools (F12)
2. Toggle device toolbar (Ctrl+Shift+M)
3. Select "iPhone 12 Pro" or similar
4. Repeat TEST 3, 5, and 6

**Expected Result:**
- ✅ Cart page responsive on mobile
- ✅ Discount input works on mobile
- ✅ Checkout page responsive
- ✅ Discount box visible on mobile

**Pass Criteria:** All features work on mobile view

---

## 🎯 Success Criteria Summary

| Test | Feature | Status |
|------|---------|--------|
| 1 | Product page has NO discount input | ⬜ |
| 2 | Add to cart works | ⬜ |
| 3 | Apply discount in cart works | ⬜ |
| 4 | Invalid code shows error | ⬜ |
| 5 | Discount carried to checkout | ⬜ |
| 6 | Checkout without discount works | ⬜ |
| 7 | Order placement with discount | ⬜ |
| 8 | Mobile responsive | ⬜ |

**Phase 1 is successful if ALL tests pass ✅**

---

## 🐛 Troubleshooting

### Issue: Discount not showing in checkout
**Solution:** Make sure you clicked "Proceed to Checkout" from cart page (not direct URL)

### Issue: Discount code not working
**Solution:** Use active codes: `FIRST10`, `MYFASHION1`, or `SAVE20`

### Issue: Cart is empty
**Solution:** Add products to cart first from product detail page

### Issue: Server not running
**Solution:** 
```bash
# Backend
cd backend
python app.py

# Frontend (in new terminal)
npm run dev
```

---

## 📸 Expected Screenshots

### Cart Page (with discount)
```
┌─────────────────────────────────────┐
│ Your Cart                           │
│                                     │
│ [Product Image] Product Name        │
│ Color: Pink · Size: M               │
│ Qty: 1                    ₹1000     │
│                                     │
│ ┌─────────────────────────────┐     │
│ │ Price Details               │     │
│ │ Price (1 item)      ₹1000   │     │
│ │ Discount (FIRST10)  -₹100 ✅│     │
│ │ Delivery            FREE     │     │
│ │ ─────────────────────────   │     │
│ │ Total               ₹900     │     │
│ │                             │     │
│ │ 🏷️ COUPON CODE              │     │
│ │ [FIRST10___] [Apply]        │     │
│ │ ✓ Coupon applied!           │     │
│ │                             │     │
│ │ [Proceed to Checkout →]     │     │
│ └─────────────────────────────┘     │
└─────────────────────────────────────┘
```

### Checkout Page (with discount)
```
┌─────────────────────────────────────┐
│ Checkout                            │
│                                     │
│ Contact Details                     │
│ [Name] [Email] [Phone]              │
│                                     │
│ Shipping Address                    │
│ [Address fields...]                 │
│                                     │
│ ┌─────────────────────────────┐     │
│ │ ✅ Discount Applied          │     │
│ │ Code: FIRST10               │     │
│ │ You save ₹100               │     │
│ │ 💡 To change, go back to cart│     │
│ └─────────────────────────────┘     │
│                                     │
│ ┌─────────────────────────────┐     │
│ │ Order Summary               │     │
│ │ Subtotal          ₹1000     │     │
│ │ Discount          -₹100     │     │
│ │ Shipping          Free      │     │
│ │ ─────────────────────────   │     │
│ │ Total             ₹900      │     │
│ │                             │     │
│ │ [Place Order]               │     │
│ └─────────────────────────────┘     │
└─────────────────────────────────────┘
```

---

## ✅ Final Checklist

Before marking Phase 1 as complete:

- [ ] All 8 tests passed
- [ ] No console errors in browser
- [ ] No errors in backend terminal
- [ ] Discount flow works end-to-end
- [ ] User experience is smooth
- [ ] Mobile view works correctly

---

**Ready to test!** 🚀

Start at: http://localhost:5173
