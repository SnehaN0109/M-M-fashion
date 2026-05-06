import { useState, useContext, useEffect } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import { CartContext } from "../context/CartContext";
import { useDomain } from "../context/DomainContext";
import { Loader2, ShoppingBag, Truck } from "lucide-react";
const CheckoutPage = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const { removeOrderedItems } = useContext(CartContext);
  const { domain, priceKey } = useDomain();

  // Receive selected items + discount from CartPage via navigation state
  const discountApplied = location.state?.discountApplied || null;
  // selectedItems: only the items the user checked in CartPage
  // Guard: ensure it's always an array with valid items
  const selectedItems = (location.state?.selectedItems || []).filter(
    item => item?.activeVariant?.id && item?.cartQuantity >= 1
  );

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [fieldErrors, setFieldErrors] = useState({});
  // UPI is the only payment method — hardcoded, no selector needed
  const paymentMethod = "UPI";

  const [form, setForm] = useState({
    customer_name: "",
    customer_email: "",
    customer_phone: "",
    address_line1: "",
    address_line2: "",
    city: "",
    state: "",
    pincode: "",
    whatsapp_number: ""
  });

  // Auto-fill WhatsApp number from localStorage on mount
  useEffect(() => {
    const savedWhatsApp = localStorage.getItem("whatsapp_number");
    if (savedWhatsApp) {
      setForm(prev => ({
        ...prev,
        whatsapp_number: savedWhatsApp
      }));
    }
  }, []);

  // Redirect if no items were selected (direct URL access)
  if (selectedItems.length === 0) {
    return (
      <div className="min-h-screen flex flex-col items-center justify-center gap-6">
        <ShoppingBag size={48} className="text-gray-300" />
        <p className="text-xl font-bold text-gray-500">No items selected</p>
        <button
          onClick={() => navigate("/cart")}
          className="px-8 py-3 bg-pink-600 text-white font-bold rounded-2xl"
        >
          Back to Cart
        </button>
      </div>
    );
  }

  // Price calculations — based on selectedItems only
  const subtotal = selectedItems.reduce(
    (sum, item) => sum + (item.price || 0) * (item.cartQuantity || 1), 0
  );
  const discountAmount = discountApplied?.amount || 0;
  const shippingCharge = subtotal >= 999 ? 0 : 99;
  const total = subtotal - discountAmount + shippingCharge;

  const handleChange = (e) => {
    const { name, value } = e.target;
    setForm({ ...form, [name]: value });
    
    // Clear field error when user starts typing
    if (fieldErrors[name]) {
      setFieldErrors(prev => ({ ...prev, [name]: "" }));
    }
    
    // Clear general error
    if (error) setError("");
  };

  // Validation functions
  const validateEmail = (email) => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
  };

  const validatePhone = (phone) => {
    const phoneRegex = /^[6-9]\d{9}$/; // Indian mobile number: starts with 6-9, total 10 digits
    return phoneRegex.test(phone);
  };

  const validatePincode = (pincode) => {
    const pincodeRegex = /^\d{6}$/; // Exactly 6 digits
    return pincodeRegex.test(pincode);
  };

  const validateForm = () => {
    const errors = {};
    
    // Required field validation
    if (!form.customer_name.trim()) {
      errors.customer_name = "Full name is required";
    } else if (form.customer_name.trim().length < 3) {
      errors.customer_name = "Name must be at least 3 characters";
    }
    
    if (!form.customer_email.trim()) {
      errors.customer_email = "Email is required";
    } else if (!validateEmail(form.customer_email)) {
      errors.customer_email = "Please enter a valid email address";
    }
    
    if (!form.customer_phone.trim()) {
      errors.customer_phone = "Phone number is required";
    } else if (!validatePhone(form.customer_phone)) {
      errors.customer_phone = "Please enter a valid 10-digit mobile number";
    }
    
    if (!form.address_line1.trim()) {
      errors.address_line1 = "Address is required";
    }
    
    if (!form.city.trim()) {
      errors.city = "City is required";
    }
    
    if (!form.state.trim()) {
      errors.state = "State is required";
    }
    
    if (!form.pincode.trim()) {
      errors.pincode = "Pincode is required";
    } else if (!validatePincode(form.pincode)) {
      errors.pincode = "Pincode must be exactly 6 digits";
    }
    
    setFieldErrors(errors);
    return Object.keys(errors).length === 0;
  };

  const handlePlaceOrder = async () => {
    // Validate form fields first
    if (!validateForm()) {
      setError("Please fix the errors above before placing your order");
      return;
    }

    // ── Step 1: Strip malformed items silently ────────────────────────────
    // Keep only items that have a valid variant id, quantity > 0, and a price
    const validItems = selectedItems.filter(
      item =>
        item?.activeVariant?.id &&
        item?.cartQuantity > 0 &&
        item?.price != null &&
        item.price > 0
    );

    // ── Step 2: Validate at least one item remains after stripping ────────
    if (validItems.length === 0) {
      setError("No valid items selected. Please go back to cart and select items.");
      return;
    }

    setLoading(true);
    setError("");

    try {
      // ── Step 3: Build payload using ONLY validItems ───────────────────
      const payload = {
        ...form,
        domain: domain || window.location.hostname,
        price_key: priceKey || "price_b2c",
        discount_code: discountApplied?.code || "",
        payment_method: paymentMethod,
        items: validItems.map(item => ({
          variant_id: item.activeVariant.id,
          quantity: item.cartQuantity,
        })),
      };

      const res = await fetch(`${import.meta.env.VITE_API_URL}/api/orders/checkout`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      const data = await res.json();

      if (!res.ok) {
        setError(data.error || "Failed to place order. Please try again.");
        return;
      }

      // ── Step 4: Remove ONLY the ordered items — keep the rest ─────────
      const orderedVariantIds = validItems
        .map(i => i.activeVariant?.id)
        .filter(Boolean);
      await removeOrderedItems(orderedVariantIds);

      // ── Step 5: Navigate away (selectedItems resets naturally) ────────
      // Note: WhatsApp confirmation is sent automatically by the backend
      // inside the checkout API — no need to call it again from frontend.
      navigate("/order-success", {
        state: { order_id: data.order_id, paymentMethod, total },
      });
    } catch {
      setError("Network error. Please check your connection.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-gray-50 min-h-screen py-10">
      <div className="max-w-6xl mx-auto px-6">

        <h1 className="text-3xl font-black text-gray-900 mb-8 tracking-tight">Checkout</h1>

        <div className="grid lg:grid-cols-3 gap-8">

          {/* ── LEFT: Form ── */}
          <div className="lg:col-span-2 space-y-6">

            {/* Contact */}
            <div className="bg-white rounded-2xl p-6 shadow-sm">
              <h2 className="font-black text-lg text-gray-900 mb-4">Contact Details</h2>
              <div className="grid sm:grid-cols-2 gap-4">
                <div>
                  <label className="text-xs font-bold text-gray-500 uppercase tracking-wider">Full Name *</label>
                  <input name="customer_name" value={form.customer_name} onChange={handleChange}
                    className={`mt-1 w-full border rounded-xl px-4 py-3 text-sm focus:outline-none focus:ring-2 ${
                      fieldErrors.customer_name 
                        ? 'border-red-300 focus:ring-red-500' 
                        : 'border-gray-200 focus:ring-pink-500'
                    }`}
                    placeholder="Your full name" />
                  {fieldErrors.customer_name && (
                    <p className="mt-1 text-xs text-red-600 font-bold">{fieldErrors.customer_name}</p>
                  )}
                </div>
                <div>
                  <label className="text-xs font-bold text-gray-500 uppercase tracking-wider">Email *</label>
                  <input name="customer_email" type="email" value={form.customer_email} onChange={handleChange}
                    className={`mt-1 w-full border rounded-xl px-4 py-3 text-sm focus:outline-none focus:ring-2 ${
                      fieldErrors.customer_email 
                        ? 'border-red-300 focus:ring-red-500' 
                        : 'border-gray-200 focus:ring-pink-500'
                    }`}
                    placeholder="email@example.com" />
                  {fieldErrors.customer_email && (
                    <p className="mt-1 text-xs text-red-600 font-bold">{fieldErrors.customer_email}</p>
                  )}
                </div>
                <div>
                  <label className="text-xs font-bold text-gray-500 uppercase tracking-wider">Phone *</label>
                  <input name="customer_phone" value={form.customer_phone} onChange={handleChange}
                    maxLength="10"
                    className={`mt-1 w-full border rounded-xl px-4 py-3 text-sm focus:outline-none focus:ring-2 ${
                      fieldErrors.customer_phone 
                        ? 'border-red-300 focus:ring-red-500' 
                        : 'border-gray-200 focus:ring-pink-500'
                    }`}
                    placeholder="10-digit mobile number" />
                  {fieldErrors.customer_phone && (
                    <p className="mt-1 text-xs text-red-600 font-bold">{fieldErrors.customer_phone}</p>
                  )}
                </div>
                <div>
                  <label className="text-xs font-bold text-gray-500 uppercase tracking-wider">
                    Notification Number {form.phone_number && <span className="text-blue-600">✓</span>}
                  </label>
                  <input name="phone_number" value={form.phone_number} onChange={handleChange}
                    maxLength="10"
                    className="mt-1 w-full border border-gray-200 rounded-xl px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-pink-500 bg-gray-50"
                    placeholder="Auto-filled from login" 
                    readOnly={!!form.phone_number} />
                  {form.phone_number && (
                    <p className="mt-1 text-xs text-blue-600 font-bold">✓ Auto-filled from your login</p>
                  )}
                </div>
              </div>
            </div>

            {/* Shipping Address */}
            <div className="bg-white rounded-2xl p-6 shadow-sm">
              <h2 className="font-black text-lg text-gray-900 mb-4 flex items-center gap-2">
                <Truck size={20} className="text-pink-600" /> Shipping Address
              </h2>
              <div className="space-y-4">
                <div>
                  <label className="text-xs font-bold text-gray-500 uppercase tracking-wider">Address Line 1 *</label>
                  <input name="address_line1" value={form.address_line1} onChange={handleChange}
                    className={`mt-1 w-full border rounded-xl px-4 py-3 text-sm focus:outline-none focus:ring-2 ${
                      fieldErrors.address_line1 
                        ? 'border-red-300 focus:ring-red-500' 
                        : 'border-gray-200 focus:ring-pink-500'
                    }`}
                    placeholder="House/Flat no, Street name" />
                  {fieldErrors.address_line1 && (
                    <p className="mt-1 text-xs text-red-600 font-bold">{fieldErrors.address_line1}</p>
                  )}
                </div>
                <div>
                  <label className="text-xs font-bold text-gray-500 uppercase tracking-wider">Address Line 2</label>
                  <input name="address_line2" value={form.address_line2} onChange={handleChange}
                    className="mt-1 w-full border border-gray-200 rounded-xl px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-pink-500"
                    placeholder="Landmark, Area (optional)" />
                </div>
                <div className="grid sm:grid-cols-3 gap-4">
                  <div>
                    <label className="text-xs font-bold text-gray-500 uppercase tracking-wider">City *</label>
                    <input name="city" value={form.city} onChange={handleChange}
                      className={`mt-1 w-full border rounded-xl px-4 py-3 text-sm focus:outline-none focus:ring-2 ${
                        fieldErrors.city 
                          ? 'border-red-300 focus:ring-red-500' 
                          : 'border-gray-200 focus:ring-pink-500'
                      }`}
                      placeholder="City" />
                    {fieldErrors.city && (
                      <p className="mt-1 text-xs text-red-600 font-bold">{fieldErrors.city}</p>
                    )}
                  </div>
                  <div>
                    <label className="text-xs font-bold text-gray-500 uppercase tracking-wider">State *</label>
                    <input name="state" value={form.state} onChange={handleChange}
                      className={`mt-1 w-full border rounded-xl px-4 py-3 text-sm focus:outline-none focus:ring-2 ${
                        fieldErrors.state 
                          ? 'border-red-300 focus:ring-red-500' 
                          : 'border-gray-200 focus:ring-pink-500'
                      }`}
                      placeholder="State" />
                    {fieldErrors.state && (
                      <p className="mt-1 text-xs text-red-600 font-bold">{fieldErrors.state}</p>
                    )}
                  </div>
                  <div>
                    <label className="text-xs font-bold text-gray-500 uppercase tracking-wider">Pincode *</label>
                    <input name="pincode" value={form.pincode} onChange={handleChange}
                      maxLength="6"
                      className={`mt-1 w-full border rounded-xl px-4 py-3 text-sm focus:outline-none focus:ring-2 ${
                        fieldErrors.pincode 
                          ? 'border-red-300 focus:ring-red-500' 
                          : 'border-gray-200 focus:ring-pink-500'
                      }`}
                      placeholder="6-digit pincode" />
                    {fieldErrors.pincode && (
                      <p className="mt-1 text-xs text-red-600 font-bold">{fieldErrors.pincode}</p>
                    )}
                  </div>
                </div>
              </div>
            </div>

            {/* Discount Applied (Read-only from Cart) */}
            {discountApplied && (
              <div className="bg-green-50 border border-green-200 rounded-2xl p-6 shadow-sm">
                <div className="flex items-center justify-between">
                  <div>
                    <h2 className="font-black text-lg text-green-700 mb-1">Discount Applied</h2>
                    <p className="text-sm text-green-600 font-bold">
                      Code: {discountApplied.code} — You save ₹{discountApplied.amount}
                    </p>
                  </div>
                  <div className="text-3xl">✓</div>
                </div>
                <p className="text-xs text-green-600 mt-2">
                  💡 To change discount code, go back to cart
                </p>
              </div>
            )}

          </div>

          {/* ── RIGHT: Order Summary ── */}
          <div className="space-y-6">
            <div className="bg-white rounded-2xl p-6 shadow-sm sticky top-24">
              <h2 className="font-black text-lg text-gray-900 mb-4">Order Summary</h2>

              {/* Items */}
              <div className="space-y-3 mb-6 max-h-60 overflow-y-auto">
                {selectedItems.map((item, i) => (
                  <div key={i} className="flex gap-3 items-center">
                    <img
                      src={item.image_url || "https://via.placeholder.com/60"}
                      className="w-14 h-14 rounded-xl object-cover border border-gray-100"
                      alt={item.name}
                    />
                    <div className="flex-1 min-w-0">
                      <p className="text-sm font-bold text-gray-900 truncate">{item.name}</p>
                      <p className="text-xs text-gray-400">
                        {item.activeVariant?.color} · {item.activeVariant?.size} · Qty {item.cartQuantity}
                      </p>
                    </div>
                    <p className="text-sm font-black text-gray-900">
                      ₹{((item.price || 0) * (item.cartQuantity || 1)).toLocaleString()}
                    </p>
                  </div>
                ))}
              </div>

              {/* Price breakdown */}
              <div className="space-y-2 text-sm border-t pt-4">
                <div className="flex justify-between text-gray-600">
                  <span>Subtotal</span>
                  <span>₹{subtotal.toLocaleString()}</span>
                </div>
                {discountAmount > 0 && (
                  <div className="flex justify-between text-green-600 font-bold">
                    <span>Discount</span>
                    <span>−₹{discountAmount}</span>
                  </div>
                )}
                <div className="flex justify-between text-gray-600">
                  <span>Shipping</span>
                  <span>{shippingCharge === 0 ? "Free" : `₹${shippingCharge}`}</span>
                </div>
                <div className="flex justify-between font-black text-lg text-gray-900 border-t pt-3 mt-2">
                  <span>Total</span>
                  <span>₹{total.toLocaleString()}</span>
                </div>
              </div>

              {/* Payment method — UPI only */}
              <div className="mt-4 bg-amber-50 border border-amber-200 rounded-xl px-4 py-3 flex items-center gap-3">
                <span className="text-xl">📱</span>
                <div>
                  <p className="text-xs font-black text-amber-800 uppercase tracking-wider">Payment Method</p>
                  <p className="text-sm font-bold text-amber-700">UPI / QR Code</p>
                </div>
                <span className="ml-auto text-xs font-black text-amber-600 bg-amber-100 px-2 py-1 rounded-lg">Only option</span>
              </div>
              <p className="mt-2 text-xs text-amber-700 font-medium bg-amber-50 rounded-lg px-3 py-2">
                💡 UPI payment instructions will appear after placing the order.
              </p>

              {/* Error */}
              {error && (
                <div className="mt-3 bg-red-50 border border-red-100 text-red-600 text-xs font-bold p-3 rounded-xl">
                  {error}
                </div>
              )}

              {/* Place Order */}
              <button
                onClick={handlePlaceOrder}
                disabled={loading}
                className="mt-6 w-full bg-pink-600 hover:bg-pink-700 text-white font-black py-4 rounded-2xl text-lg shadow-lg active:scale-95 transition-all flex items-center justify-center gap-3 disabled:opacity-60"
              >
                {loading ? <Loader2 size={22} className="animate-spin" /> : null}
                {loading ? "Placing Order..." : "Place Order"}
              </button>

              <p className="text-center text-xs text-gray-400 mt-3">
                🔐 Safe & Secure · 7 Day Returns
              </p>
            </div>
          </div>

        </div>
      </div>
    </div>
  );
};

export default CheckoutPage;
