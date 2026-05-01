# Implement Order Tracking System with Manual Payment Verification

This plan outlines the steps to build a complete order tracking lifecycle where admins manually verify payments and control the order statuses (`PENDING_PAYMENT` -> `PLACED` -> `PACKED` -> `SHIPPED` -> `OUT_FOR_DELIVERY` -> `DELIVERED`).

## Proposed Changes

### Database Updates

#### [MODIFY] `backend/models.py`
- Add `payment_status` column to the `Order` model (`db.Column(db.String(50), default='PENDING')`).
- Ensure the default for the `status` column in the `Order` model is `'PENDING_PAYMENT'`.

### Backend Updates

#### [MODIFY] `backend/routes/orders.py`
- In the `/checkout` route, ensure new orders explicitly set `status='PENDING_PAYMENT'` and `payment_status='PENDING'` when creating the `Order` record.
- In the `/my-orders` and `/track/<id>` routes, ensure `payment_status` is returned in the JSON response so the frontend can display the payment verification banner.

#### [MODIFY] `backend/routes/admin_dashboard.py`
- Update the `/orders/<int:order_id>/status` route to allow updating both `status` and `payment_status`.
- Add validation to ensure `status` is one of `['PENDING_PAYMENT', 'PLACED', 'PACKED', 'SHIPPED', 'OUT_FOR_DELIVERY', 'DELIVERED', 'CANCELLED']`.
- Add validation to ensure `payment_status` is one of `['PENDING', 'VERIFIED', 'FAILED']`.

---

### Frontend Admin Updates

#### [MODIFY] `src/pages/AdminDashboardPage.jsx`
- Update `STATUS_OPTIONS` array to `["PENDING_PAYMENT", "PLACED", "PACKED", "SHIPPED", "OUT_FOR_DELIVERY", "DELIVERED", "CANCELLED"]`.
- Add `PAYMENT_STATUS_OPTIONS` array `["PENDING", "VERIFIED", "FAILED"]`.
- Update the `OrderRow` component to include a dropdown for updating the `payment_status` alongside the existing `status` dropdown.
- Update the `adminFetch` call in `updateStatus` to pass the new `payment_status` to the backend.

---

### Frontend User Updates

#### [MODIFY] `src/pages/TrackOrderPage.jsx`
- Update the `STATUS_STEPS` array to include the new keys: `PENDING_PAYMENT`, `PLACED`, `PACKED`, `SHIPPED`, `OUT_FOR_DELIVERY`, `DELIVERED`.
- If `payment_status === "PENDING"`, show an alert banner stating: *"Waiting for payment verification"*.
- Update the UI logic to display the "Shipped via Speed Post" and Tracking ID block only if the current step is `SHIPPED` or higher.
- Add backward compatibility mappings so old lowercase statuses (like `pending_payment`) are safely mapped to `PENDING_PAYMENT` to prevent UI breakage.

## Verification Plan

### Manual Verification
1. Place a new order on the frontend.
2. Go to the "Track Order" page and verify the status is `PENDING_PAYMENT` and the "Waiting for payment verification" banner is visible.
3. Open the Admin Dashboard (`/admin`), locate the order, and use the new dropdowns to set `payment_status = VERIFIED`.
4. Check the "Track Order" page to ensure the payment banner disappears.
5. In the Admin Dashboard, set `status = PLACED`, then `PACKED`, then `SHIPPED` (while entering a tracking ID).
6. Check the "Track Order" page to verify the timeline updates correctly and the "Shipped via Speed Post" message appears.
