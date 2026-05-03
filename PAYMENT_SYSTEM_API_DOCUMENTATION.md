# 💳 PAYMENT SYSTEM API DOCUMENTATION

## ✅ IMPLEMENTATION COMPLETE

**Status:** All payment routes implemented and tested  
**File:** `backend/routes/payment.py`  
**Tests Passed:** 5/5  
**Date:** 2026-05-02

---

## 📁 FILE STRUCTURE

```
backend/
├── routes/
│   └── payment.py          ✅ NEW - Payment system routes
├── uploads/
│   └── payment_proofs/     ✅ NEW - Payment proof storage
└── app.py                  ✅ UPDATED - Blueprint registered
```

---

## 🔌 API ENDPOINTS

### 1. USER API - Upload Payment Proof

**Endpoint:** `POST /api/orders/<order_id>/mark-paid`

**Purpose:** User uploads payment proof for their order

**Authentication:** Optional (WhatsApp number verification)

**Request:**
- **Content-Type:** `multipart/form-data`
- **Form Fields:**
  - `payment_proof` (file, optional): Image/PDF file
  - `whatsapp_number` (string, optional): For ownership verification

**Allowed File Types:** jpg, jpeg, png, pdf, webp

**Example Request (cURL):**
```bash
curl -X POST http://localhost:5000/api/orders/44/mark-paid \
  -F "payment_proof=@payment_screenshot.jpg" \
  -F "whatsapp_number=9876543210"
```

**Response (200 OK):**
```json
{
  "message": "Payment proof uploaded successfully. Awaiting admin verification.",
  "order_id": 44,
  "payment_proof": "/uploads/payment_proofs/f9490f9b838449609b64e1831701b5d3.jpg",
  "payment_status": "PENDING",
  "status": "PENDING_PAYMENT"
}
```

**Behavior:**
- ✅ Saves file to `uploads/payment_proofs/`
- ✅ Updates `order.payment_proof` with file path
- ✅ Keeps `payment_status = 'PENDING'` (awaiting admin verification)
- ✅ Does NOT change order status
- ✅ Verifies user ownership if WhatsApp number provided

**Error Responses:**
- `400` - Invalid file type
- `403` - Unauthorized (order doesn't belong to user)
- `404` - Order not found
- `500` - File save error

---

### 2. ADMIN API - Verify or Reject Payment

**Endpoint:** `POST /api/admin/orders/<order_id>/payment-action`

**Purpose:** Admin verifies or rejects payment after reviewing proof

**Authentication:** Required (Admin JWT token)

**Request:**
- **Content-Type:** `application/json`
- **Headers:** `Authorization: Bearer <admin_token>`
- **Body:**
```json
{
  "action": "verify",
  "reason": "Optional rejection reason"
}
```

**Actions:**
- `verify` - Approve payment
- `reject` - Reject payment

**Example Request (Verify):**
```bash
curl -X POST http://localhost:5000/api/admin/orders/44/payment-action \
  -H "Authorization: Bearer <admin_token>" \
  -H "Content-Type: application/json" \
  -d '{"action": "verify"}'
```

**Response - Verify (200 OK):**
```json
{
  "message": "Payment verified successfully",
  "order_id": 44,
  "payment_status": "VERIFIED",
  "status": "PLACED"
}
```

**Behavior (Verify):**
- ✅ Sets `payment_status = 'VERIFIED'`
- ✅ Changes `status = 'PLACED'` (if currently PENDING_PAYMENT)
- ✅ Order ready for fulfillment

**Example Request (Reject):**
```bash
curl -X POST http://localhost:5000/api/admin/orders/44/payment-action \
  -H "Authorization: Bearer <admin_token>" \
  -H "Content-Type: application/json" \
  -d '{"action": "reject", "reason": "Invalid payment proof"}'
```

**Response - Reject (200 OK):**
```json
{
  "message": "Payment rejected",
  "order_id": 44,
  "payment_status": "FAILED",
  "status": "PENDING_PAYMENT",
  "reason": "Invalid payment proof"
}
```

**Behavior (Reject):**
- ✅ Sets `payment_status = 'FAILED'`
- ✅ Keeps order status unchanged
- ✅ Returns rejection reason

**Error Responses:**
- `400` - Invalid action
- `401` - Missing/invalid token
- `403` - Not admin
- `404` - Order not found

---

### 3. ADMIN API - Get Payment Proof

**Endpoint:** `GET /api/admin/payment-proof/<order_id>`

**Purpose:** Admin retrieves payment proof details for review

**Authentication:** Required (Admin JWT token)

**Request:**
- **Headers:** `Authorization: Bearer <admin_token>`

**Example Request:**
```bash
curl -X GET http://localhost:5000/api/admin/payment-proof/44 \
  -H "Authorization: Bearer <admin_token>"
```

**Response (200 OK):**
```json
{
  "order_id": 44,
  "payment_proof": "/uploads/payment_proofs/f9490f9b838449609b64e1831701b5d3.jpg",
  "payment_status": "PENDING",
  "payment_method": "UPI",
  "customer_name": "Payment Test User",
  "customer_email": "payment@test.com",
  "customer_phone": "9876543210",
  "total_amount": 899.0,
  "created_at": "2026-05-02T19:19:49"
}
```

**Behavior:**
- ✅ Returns payment proof URL
- ✅ Returns order details for context
- ✅ Admin can view/download proof image

**Error Responses:**
- `401` - Missing/invalid token
- `403` - Not admin
- `404` - Order not found

---

### 4. PUBLIC API - Get Payment Status

**Endpoint:** `GET /api/orders/<order_id>/payment-status`

**Purpose:** Check payment status of an order

**Authentication:** Optional (WhatsApp number verification)

**Query Parameters:**
- `whatsapp_number` (optional): For ownership verification

**Example Request:**
```bash
curl -X GET "http://localhost:5000/api/orders/44/payment-status?whatsapp_number=9876543210"
```

**Response (200 OK):**
```json
{
  "order_id": 44,
  "payment_status": "PENDING",
  "payment_method": "UPI",
  "has_payment_proof": true,
  "status": "PENDING_PAYMENT"
}
```

**Behavior:**
- ✅ Returns current payment status
- ✅ Indicates if payment proof uploaded
- ✅ Verifies ownership if WhatsApp provided

**Error Responses:**
- `403` - Unauthorized (order doesn't belong to user)
- `404` - Order not found

---

## 🔄 PAYMENT WORKFLOW

### Complete Flow:

```
1. User places order
   ↓
   payment_status = 'PENDING'
   status = 'PENDING_PAYMENT'

2. User uploads payment proof
   POST /api/orders/<id>/mark-paid
   ↓
   payment_proof = '/uploads/payment_proofs/xxx.jpg'
   payment_status = 'PENDING' (unchanged)
   status = 'PENDING_PAYMENT' (unchanged)

3. Admin reviews payment proof
   GET /api/admin/payment-proof/<id>
   ↓
   Admin views proof image

4a. Admin VERIFIES payment
    POST /api/admin/orders/<id>/payment-action
    {"action": "verify"}
    ↓
    payment_status = 'VERIFIED'
    status = 'PLACED'
    ↓
    Order ready for fulfillment

4b. Admin REJECTS payment
    POST /api/admin/orders/<id>/payment-action
    {"action": "reject"}
    ↓
    payment_status = 'FAILED'
    status = 'PENDING_PAYMENT' (unchanged)
    ↓
    User notified to retry payment
```

---

## 🔐 SECURITY FEATURES

### User Endpoints:
- ✅ Optional WhatsApp number verification
- ✅ Checks order ownership before allowing upload
- ✅ File type validation (jpg, jpeg, png, pdf, webp)
- ✅ Unique filename generation (UUID)

### Admin Endpoints:
- ✅ JWT token authentication required
- ✅ Role verification (must be admin)
- ✅ Token expiry handling
- ✅ Protected routes with decorator

### File Handling:
- ✅ Secure filename generation
- ✅ File extension validation
- ✅ Separate upload directory
- ✅ Error handling for file operations

---

## 📂 FILE STORAGE

### Upload Directory:
```
backend/uploads/payment_proofs/
```

### File Naming:
- Format: `<uuid>.{extension}`
- Example: `f9490f9b838449609b64e1831701b5d3.jpg`

### File Access:
- URL: `/uploads/payment_proofs/<filename>`
- Served by Flask static file handler
- Configured in `app.py`

---

## 🧪 TEST RESULTS

### All Tests Passed: 5/5

| Test | Status | Description |
|------|--------|-------------|
| 1. User Upload Payment Proof | ✅ PASS | File uploaded, status remains PENDING |
| 2. Get Payment Status | ✅ PASS | Status retrieved, proof detected |
| 3. Admin Get Payment Proof | ✅ PASS | Admin retrieved proof URL |
| 4. Admin Verify Payment | ✅ PASS | Status set to VERIFIED, order PLACED |
| 5. Admin Reject Payment | ✅ PASS | Status set to FAILED |

---

## 📊 DATABASE FIELDS USED

### Order Model Fields:
- `payment_method` - Payment method chosen (COD, UPI, etc.)
- `payment_status` - Payment verification status (PENDING, VERIFIED, FAILED)
- `payment_proof` - File path to uploaded proof
- `status` - Order fulfillment status

### Status Values:

**payment_status:**
- `PENDING` - Awaiting verification
- `VERIFIED` - Payment confirmed by admin
- `FAILED` - Payment rejected by admin

**status:**
- `PENDING_PAYMENT` - Awaiting payment/verification
- `PLACED` - Payment verified, ready for fulfillment
- `PACKED` - Order packed
- `SHIPPED` - Order shipped
- `OUT_FOR_DELIVERY` - Out for delivery
- `DELIVERED` - Delivered to customer

---

## 🔧 INTEGRATION WITH EXISTING SYSTEM

### Blueprint Registration:
```python
# backend/app.py
from routes.payment import payment_bp
app.register_blueprint(payment_bp)
```

### Static File Serving:
```python
# backend/app.py
@app.route('/uploads/payment_proofs/<filename>')
def serve_payment_proof(filename):
    folder = os.path.join(os.path.dirname(__file__), 'uploads', 'payment_proofs')
    return send_from_directory(folder, filename)
```

### CORS Configuration:
- Already configured in `app.py`
- Allows all API routes including payment endpoints

---

## 📝 USAGE EXAMPLES

### Frontend Integration Example:

```javascript
// User uploads payment proof
const uploadPaymentProof = async (orderId, file, whatsappNumber) => {
  const formData = new FormData();
  formData.append('payment_proof', file);
  formData.append('whatsapp_number', whatsappNumber);
  
  const response = await fetch(`/api/orders/${orderId}/mark-paid`, {
    method: 'POST',
    body: formData
  });
  
  return response.json();
};

// Admin verifies payment
const verifyPayment = async (orderId, adminToken) => {
  const response = await fetch(`/api/admin/orders/${orderId}/payment-action`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${adminToken}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ action: 'verify' })
  });
  
  return response.json();
};

// Get payment proof for admin review
const getPaymentProof = async (orderId, adminToken) => {
  const response = await fetch(`/api/admin/payment-proof/${orderId}`, {
    headers: {
      'Authorization': `Bearer ${adminToken}`
    }
  });
  
  return response.json();
};
```

---

## ✅ IMPLEMENTATION CHECKLIST

- ✅ Created `backend/routes/payment.py`
- ✅ Registered blueprint in `app.py`
- ✅ Implemented user upload endpoint
- ✅ Implemented admin verify/reject endpoint
- ✅ Implemented admin get proof endpoint
- ✅ Implemented public status check endpoint
- ✅ Added file upload handling
- ✅ Added admin authentication
- ✅ Added error handling
- ✅ Created upload directory structure
- ✅ Configured static file serving
- ✅ Tested all endpoints
- ✅ All tests passing (5/5)

---

## 🎯 READY FOR PRODUCTION

**Status:** ✅ **FULLY FUNCTIONAL**

The payment system is complete and ready for integration with the frontend. All endpoints are tested and working correctly.

**Next Steps:**
1. Integrate with frontend UI
2. Add email notifications for payment status changes
3. Add admin dashboard UI for payment review
4. Consider adding payment gateway integration (Razorpay, Stripe)

---

**Documentation Complete** ✅

