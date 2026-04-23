# 🧪 PHASE 2 TESTING GUIDE

## ✅ What Phase 2 Fixed

**Problem:** Cart quantity changes were NOT saved to database  
**Solution:** Added API endpoint + database sync  
**Result:** Quantity changes now persist across page refreshes  

---

## 🎯 Quick Test (2 Minutes)

### Step 1: Add Item to Cart
1. Open http://localhost:5173
2. Click on any product
3. Select color and size
4. Click "Add to Cart"
5. Go to Cart page

### Step 2: Change Quantity
1. Find the quantity controls (+ and - buttons)
2. Click "+" button 3 times
3. **VERIFY:** Quantity increases to 4
4. **VERIFY:** Price updates accordingly

### Step 3: Refresh Page (CRITICAL TEST)
1. Press F5 to refresh the page
2. **VERIFY:** Quantity is still 4 (not reset to 1)
3. **SUCCESS!** ✅ Quantity persisted to database

---

## 🔬 Detailed Testing

### Test 1: Increase Quantity ✅

**Steps:**
1. Go to Cart: http://localhost:5173/cart
2. Open DevTools (F12) → Network tab
3. Click "+" button on any item
4. Watch Network tab

**Expected Results:**
- ✅ Quantity increases immediately in UI
- ✅ See PUT request to `http://localhost:5000/api/cart/update`
- ✅ Request payload shows: `{whatsapp_number, variant_id, quantity}`
- ✅ Response status: 200 OK
- ✅ Response body: `{message: "Cart updated successfully", ...}`

**Pass Criteria:** API call made and succeeded

---

### Test 2: Decrease Quantity ✅

**Steps:**
1. In Cart page
2. Click "-" button on any item
3. Watch Network tab

**Expected Results:**
- ✅ Quantity decreases immediately
- ✅ PUT request sent to `/api/cart/update`
- ✅ Response status: 200 OK

**Pass Criteria:** Decrease also syncs to database

---

### Test 3: Persistence After Refresh ✅

**Steps:**
1. Change quantity to 5
2. Wait 1 second (ensure API call completes)
3. Press F5 to refresh page
4. Check quantity

**Expected Results:**
- ✅ Quantity remains 5 after refresh
- ✅ No reset to 1
- ✅ Data loaded from database

**Pass Criteria:** Quantity survives page refresh

---

### Test 4: Multiple Items ✅

**Steps:**
1. Add 3 different products to cart
2. Set quantities:
   - Item 1: 2
   - Item 2: 3
   - Item 3: 1
3. Refresh page

**Expected Results:**
- ✅ All quantities persist correctly
- ✅ Item 1 still shows 2
- ✅ Item 2 still shows 3
- ✅ Item 3 still shows 1

**Pass Criteria:** Multiple items sync independently

---

### Test 5: Stock Validation ✅

**Steps:**
1. Find a product with low stock (check "Only X left" message)
2. Add to cart
3. Try to increase quantity beyond available stock
4. Keep clicking "+" button

**Expected Results:**
- ✅ Quantity stops at available stock
- ✅ Cannot exceed stock limit
- ✅ Console shows error: "Only X items available in stock"

**Pass Criteria:** Stock validation prevents over-ordering

---

### Test 6: Network Error Handling ✅

**Steps:**
1. Open DevTools → Network tab
2. Set throttling to "Offline"
3. Try to change quantity
4. Check Console tab

**Expected Results:**
- ✅ UI still updates (optimistic)
- ✅ Console shows error: "Network error updating cart quantity"
- ✅ No crash or freeze
5. Set back to "Online"
6. Refresh page
7. ✅ Quantity reverts to last saved state

**Pass Criteria:** Graceful degradation when offline

---

## 📊 Visual Verification

### Before Phase 2 (Broken)
```
1. Add item to cart (Qty: 1)
2. Click "+" 3 times (Qty: 4)
3. Refresh page
4. ❌ Quantity resets to 1
5. ❌ Data lost!
```

### After Phase 2 (Fixed)
```
1. Add item to cart (Qty: 1)
2. Click "+" 3 times (Qty: 4)
3. Refresh page
4. ✅ Quantity remains 4
5. ✅ Data persisted!
```

---

## 🔍 Database Verification (Advanced)

### Check Database Directly

**Option 1: Using Python**
```bash
cd backend
python -c "from app import app, db; from models import CartItem; app.app_context().push(); items = CartItem.query.all(); print([(i.id, i.variant_id, i.quantity) for i in items])"
```

**Expected Output:**
```
[(1, 123, 4), (2, 456, 2), (3, 789, 3)]
```

**Option 2: Using SQLite Browser**
1. Open `backend/ecommerce.db` in DB Browser for SQLite
2. Go to "Browse Data" tab
3. Select table: `cartitem`
4. Check `quantity` column
5. Verify quantities match what you see in UI

---

## 🐛 Troubleshooting

### Issue: Quantity resets after refresh
**Cause:** API call failed or user not logged in  
**Solution:**
1. Check if you're logged in (localStorage has `whatsapp_number`)
2. Check Network tab for failed API calls
3. Check Console for errors
4. Verify backend is running on port 5000

### Issue: No API call in Network tab
**Cause:** User not logged in (guest cart)  
**Solution:**
1. Log in via WhatsApp (use any 10-digit number)
2. Guest carts are local-only (not persisted)

### Issue: "User not found" error
**Cause:** WhatsApp number not in database  
**Solution:**
1. Log in again via WhatsApp login page
2. This creates user in database

### Issue: "Insufficient stock" error
**Cause:** Trying to add more items than available  
**Solution:**
1. This is expected behavior (stock validation working)
2. Reduce quantity to available stock

---

## ✅ Success Checklist

Before marking Phase 2 as complete:

- [ ] Test 1: Increase quantity works
- [ ] Test 2: Decrease quantity works
- [ ] Test 3: Quantity persists after refresh
- [ ] Test 4: Multiple items sync correctly
- [ ] Test 5: Stock validation prevents over-ordering
- [ ] Test 6: Graceful error handling
- [ ] No console errors (except expected offline errors)
- [ ] Backend running without errors
- [ ] Database contains correct quantities

---

## 🎊 Expected Outcome

After Phase 2:
- ✅ Cart quantities saved to database in real-time
- ✅ No data loss on page refresh
- ✅ Stock validation prevents over-ordering
- ✅ Smooth user experience (optimistic updates)
- ✅ Professional e-commerce behavior

---

## 📈 Performance Check

### API Response Time
1. Open Network tab
2. Change quantity
3. Click on PUT request to `/api/cart/update`
4. Check "Timing" tab

**Expected:** < 100ms response time  
**Acceptable:** < 500ms  
**Slow:** > 1000ms (investigate if this happens)

---

## 🚀 Ready to Test!

**Start here:** http://localhost:5173/cart

**Quick verification:**
1. Change quantity
2. Refresh page
3. Quantity should remain the same

**If it works:** Phase 2 is successful! ✅  
**If it doesn't:** Check troubleshooting section above

---

*Phase 2 Testing Guide - M&M Fashion B2C Flow Improvement*
