# 💳 PAYMENT API - QUICK REFERENCE

## 🚀 ENDPOINTS

### 1. User Upload Payment Proof
```
POST /api/orders/<order_id>/mark-paid
Content-Type: multipart/form-data

Form Data:
  - payment_proof: <file>
  - whatsapp_number: <string>

Response: 200 OK
{
  "message": "Payment proof uploaded successfully...",
  "order_id": 44,
  "payment_proof": "/uploads/payment_proofs/xxx.jpg",
  "payment_status": "PENDING",
  "status": "PENDING_PAYMENT"
}
```

### 2. Admin Verify Payment
```
POST /api/admin/orders/<order_id>/payment-action
Authorization: Bearer <admin_token>
Content-Type: application/json

Body:
{
  "action": "verify"
}

Response: 200 OK
{
  "message": "Payment verified successfully",
  "order_id": 44,
  "payment_status": "VERIFIED",
  "status": "PLACED"
}
```

### 3. Admin Reject Payment
```
POST /api/admin/orders/<order_id>/payment-action
Authorization: Bearer <admin_token>
Content-Type: application/json

Body:
{
  "action": "reject",
  "reason": "Invalid payment proof"
}

Response: 200 OK
{
  "message": "Payment rejected",
  "order_id": 44,
  "payment_status": "FAILED",
  "status": "PENDING_PAYMENT"
}
```

### 4. Admin Get Payment Proof
```
GET /api/admin/payment-proof/<order_id>
Authorization: Bearer <admin_token>

Response: 200 OK
{
  "order_id": 44,
  "payment_proof": "/uploads/payment_proofs/xxx.jpg",
  "payment_status": "PENDING",
  "payment_method": "UPI",
  "customer_name": "John Doe",
  "total_amount": 899.0
}
```

### 5. Check Payment Status
```
GET /api/orders/<order_id>/payment-status?whatsapp_number=<number>

Response: 200 OK
{
  "order_id": 44,
  "payment_status": "PENDING",
  "payment_method": "UPI",
  "has_payment_proof": true,
  "status": "PENDING_PAYMENT"
}
```

---

## 📊 PAYMENT STATUS FLOW

```
PENDING → VERIFIED (admin approves)
        → FAILED (admin rejects)
```

## 📊 ORDER STATUS FLOW

```
PENDING_PAYMENT → PLACED (after payment verified)
                → PACKED
                → SHIPPED
                → OUT_FOR_DELIVERY
                → DELIVERED
```

---

## ✅ TEST RESULTS

All 5 tests passed:
- ✅ User upload payment proof
- ✅ Get payment status
- ✅ Admin get payment proof
- ✅ Admin verify payment
- ✅ Admin reject payment

---

## 📁 FILES

- **Routes:** `backend/routes/payment.py`
- **Upload Dir:** `backend/uploads/payment_proofs/`
- **Blueprint:** Registered in `backend/app.py`

---

**Status:** ✅ Ready for use
