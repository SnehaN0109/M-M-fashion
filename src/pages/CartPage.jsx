import { useState, useContext, useEffect, useRef } from "react";
import { useNavigate, Link } from "react-router-dom";
import { CartContext } from "../context/CartContext";
import { WishlistContext } from "../context/WishlistContext";
import { Loader2, Tag, ShoppingBag, Trash2, Heart, CheckSquare, Square } from "lucide-react";

const CartPage = () => {
  const navigate = useNavigate();
  const { cartItems, cartLoading, removeFromCart, updateQuantity } = useContext(CartContext);
  const { addToWishlist } = useContext(WishlistContext);

  // ── Selection state — keyed by activeVariant.id ───────────────────────────
  // Starts empty; synced to all items once cart loads (see useEffect below)
  const [selectedVariantIds, setSelectedVariantIds] = useState(new Set());
  const initializedRef = useRef(false); // track whether we've done the first-load select-all

  // Auto-select all items when cart first loads from DB
  useEffect(() => {
    if (!cartLoading && cartItems.length > 0 && !initializedRef.current) {
      initializedRef.current = true;
      setSelectedVariantIds(new Set(cartItems.map(i => i.activeVariant?.id).filter(Boolean)));
    }
  }, [cartItems, cartLoading]);
  const [selectionError, setSelectionError] = useState("");
  const [stockToast, setStockToast] = useState(""); // stock limit message

  const [coupon, setCoupon] = useState("");
  const [discountApplied, setDiscountApplied] = useState(null);
  const [couponError, setCouponError] = useState("");
  const [couponLoading, setCouponLoading] = useState(false);

  // ── Helpers ───────────────────────────────────────────────────────────────
  const removeItem = (item) => {
    removeFromCart(item.id, item.activeVariant?.id);
    setSelectedVariantIds(prev => {
      const next = new Set(prev);
      next.delete(item.activeVariant?.id);
      return next;
    });
  };

  const increaseQty = (item) => {
    const stock = item.activeVariant?.quantity ?? Infinity;
    const current = item.cartQuantity || 1;
    if (current >= stock) {
      setStockToast(`Only ${stock} item${stock !== 1 ? "s" : ""} available in stock`);
      setTimeout(() => setStockToast(""), 3000);
      return;
    }
    updateQuantity(item.id, item.activeVariant?.id, current + 1);
  };
  const decreaseQty = (item) => {
    if ((item.cartQuantity || 1) > 1)
      updateQuantity(item.id, item.activeVariant?.id, (item.cartQuantity || 1) - 1);
  };

  const moveToWishlist = (item) => {
    addToWishlist(item);
    removeFromCart(item.id, item.activeVariant?.id);
    setSelectedVariantIds(prev => {
      const next = new Set(prev);
      next.delete(item.activeVariant?.id);
      return next;
    });
  };

  // ── Toggle single item selection ──────────────────────────────────────────
  const toggleItem = (variantId) => {
    setSelectionError("");
    setSelectedVariantIds(prev => {
      const next = new Set(prev);
      if (next.has(variantId)) next.delete(variantId);
      else next.add(variantId);
      return next;
    });
  };

  // ── Select / deselect all ─────────────────────────────────────────────────
  const allSelected = cartItems.length > 0 && cartItems.every(i => selectedVariantIds.has(i.activeVariant?.id));
  const toggleAll = () => {
    setSelectionError("");
    if (allSelected) {
      setSelectedVariantIds(new Set());
    } else {
      setSelectedVariantIds(new Set(cartItems.map(i => i.activeVariant?.id).filter(Boolean)));
    }
  };

  // ── Selected items list ───────────────────────────────────────────────────
  const selectedItems = cartItems.filter(i => selectedVariantIds.has(i.activeVariant?.id));

  // ── Price calculations (based on selected items only) ─────────────────────
  const subtotal = selectedItems.reduce((sum, item) => sum + (item.price || 0) * (item.cartQuantity || 1), 0);
  const discountAmount = discountApplied?.amount || 0;
  const deliveryCharge = subtotal > 0 ? (subtotal >= 999 ? 0 : 99) : 0;
  const finalTotal = subtotal - discountAmount + deliveryCharge;

  const applyCoupon = async () => {
    if (!coupon.trim()) return;
    setCouponLoading(true);
    setCouponError("");
    try {
      const res = await fetch(`${import.meta.env.VITE_API_URL}/api/cart/apply_discount`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ code: coupon.trim().toUpperCase(), cart_total: subtotal }),
      });
      const data = await res.json();
      if (!res.ok) { setCouponError(data.error || "Invalid coupon code"); setDiscountApplied(null); return; }
      let amount = 0;
      if (data.discount_flat) amount = parseFloat(data.discount_flat);
      else if (data.discount_percentage) amount = Math.round(subtotal * data.discount_percentage / 100);
      setDiscountApplied({ amount, code: coupon.trim().toUpperCase() });
      setCouponError("");
    } catch {
      setCouponError("Could not apply coupon. Try again.");
    } finally {
      setCouponLoading(false);
    }
  };

  // ── Proceed to checkout — validate selection first ────────────────────────
  const handleProceedToCheckout = () => {
    if (cartLoading) return; // don't proceed while cart is still loading
    if (selectedItems.length === 0) {
      setSelectionError("Please select at least one item to proceed.");
      // Scroll to top so user sees the error
      window.scrollTo({ top: 0, behavior: "smooth" });
      return;
    }
    navigate("/checkout", {
      state: {
        discountApplied,
        selectedItems,   // only selected items go to checkout
      }
    });
  };

  // ── Loading / empty states ────────────────────────────────────────────────
  if (cartLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <Loader2 className="w-10 h-10 text-pink-600 animate-spin" />
      </div>
    );
  }

  if (cartItems.length === 0) {
    return (
      <div className="min-h-screen flex flex-col items-center justify-center gap-6">
        <ShoppingBag size={56} className="text-gray-200" />
        <p className="text-2xl font-black text-gray-400">Your cart is empty</p>
        <Link to="/products" className="px-8 py-3 bg-pink-600 text-white font-bold rounded-2xl">
          Continue Shopping
        </Link>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-6 py-10 pb-32 md:pb-10">
      <h1 className="text-3xl font-black mb-2">Your Cart</h1>
      <p className="text-sm text-gray-400 mb-6">
        {selectedItems.length} of {cartItems.length} item{cartItems.length !== 1 ? "s" : ""} selected
      </p>

      <div className="grid md:grid-cols-3 gap-8">

        {/* ── Cart Items ── */}
        <div className="md:col-span-2 space-y-4">

          {/* Select All row */}
          <div className="flex items-center gap-3 px-1 pb-2 border-b">
            <button
              onClick={toggleAll}
              className="flex items-center gap-2 text-sm font-bold text-gray-700 hover:text-pink-600 transition-colors"
            >
              {allSelected
                ? <CheckSquare size={20} className="text-pink-600" />
                : <Square size={20} className="text-gray-400" />
              }
              {allSelected ? "Deselect All" : "Select All"}
            </button>
            {selectedItems.length > 0 && (
              <span className="text-xs text-gray-400 font-medium">
                ({selectedItems.length} selected · ₹{subtotal.toLocaleString()})
              </span>
            )}
          </div>

          {cartItems.map((item) => {
            const variantId = item.activeVariant?.id;
            const isSelected = selectedVariantIds.has(variantId);

            return (
              <div
                key={variantId || item.cartId}
                className={`border rounded-2xl p-5 shadow-sm flex gap-4 flex-col sm:flex-row transition-all ${
                  isSelected ? "border-pink-300 bg-pink-50/30" : "border-gray-200 bg-white opacity-70"
                }`}
              >
                {/* Checkbox */}
                <button
                  onClick={() => toggleItem(variantId)}
                  className="flex-shrink-0 self-start mt-1"
                  aria-label={isSelected ? "Deselect item" : "Select item"}
                >
                  {isSelected
                    ? <CheckSquare size={22} className="text-pink-600" />
                    : <Square size={22} className="text-gray-300 hover:text-gray-500" />
                  }
                </button>

                {/* Image */}
                <img
                  src={item.image_url || item.image || "https://via.placeholder.com/150"}
                  alt={item.name}
                  className="w-24 h-28 object-cover rounded-xl flex-shrink-0"
                />

                {/* Details */}
                <div className="flex-1 min-w-0">
                  <h2 className="text-base font-black text-gray-900 truncate">{item.name}</h2>
                  <p className="text-xs text-gray-400 mt-0.5">
                    {item.activeVariant?.color && `Color: ${item.activeVariant.color}`}
                    {item.activeVariant?.size && ` · Size: ${item.activeVariant.size}`}
                  </p>
                  {item.activeVariant?.quantity < 5 && item.activeVariant?.quantity > 0 && (
                    <p className="text-xs text-red-500 font-bold mt-1">Only {item.activeVariant.quantity} left!</p>
                  )}

                  {/* Qty controls */}
                  <div className="flex items-center gap-3 mt-3">
                    <button
                      onClick={() => decreaseQty(item)}
                      className="w-8 h-8 border rounded-lg font-bold flex items-center justify-center hover:bg-gray-100"
                    >−</button>
                    <span className="font-black w-6 text-center">{item.cartQuantity || 1}</span>
                    <button
                      onClick={() => increaseQty(item)}
                      className="w-8 h-8 border rounded-lg font-bold flex items-center justify-center hover:bg-gray-100"
                    >+</button>
                    <span className="ml-2 font-black text-gray-900">
                      ₹{((item.price || 0) * (item.cartQuantity || 1)).toLocaleString()}
                    </span>
                  </div>

                  {/* Actions */}
                  <div className="flex gap-4 mt-3 text-xs font-bold">
                    <button onClick={() => removeItem(item)} className="flex items-center gap-1 text-red-500 hover:text-red-700">
                      <Trash2 size={13} /> Remove
                    </button>
                    <button onClick={() => moveToWishlist(item)} className="flex items-center gap-1 text-pink-500 hover:text-pink-700">
                      <Heart size={13} /> Move to Wishlist
                    </button>
                  </div>
                </div>
              </div>
            );
          })}

          <Link to="/products" className="text-sm text-blue-600 underline">← Continue Shopping</Link>
        </div>

        {/* ── Price Summary ── */}
        <div className="border rounded-2xl p-6 shadow-sm h-fit space-y-4">
          <h2 className="text-lg font-black">Price Details</h2>

          {selectedItems.length === 0 ? (
            <p className="text-sm text-gray-400 py-4 text-center">Select items to see price</p>
          ) : (
            <div className="space-y-2 text-sm text-gray-600">
              <div className="flex justify-between">
                <span>Price ({selectedItems.length} item{selectedItems.length > 1 ? "s" : ""})</span>
                <span>₹{subtotal.toLocaleString()}</span>
              </div>
              {discountAmount > 0 && (
                <div className="flex justify-between text-green-600 font-bold">
                  <span>Discount ({discountApplied.code})</span>
                  <span>−₹{discountAmount.toLocaleString()}</span>
                </div>
              )}
              <div className="flex justify-between">
                <span>Delivery</span>
                <span className={deliveryCharge === 0 ? "text-green-600 font-bold" : ""}>
                  {deliveryCharge === 0 ? "FREE" : `₹${deliveryCharge}`}
                </span>
              </div>
            </div>
          )}

          {selectedItems.length > 0 && (
            <>
              <hr />
              <div className="flex justify-between font-black text-lg">
                <span>Total</span>
                <span>₹{finalTotal.toLocaleString()}</span>
              </div>
              {discountAmount > 0 && (
                <p className="text-green-600 text-xs font-bold">You save ₹{discountAmount.toLocaleString()} on this order!</p>
              )}
            </>
          )}

          {/* Coupon */}
          <div className="space-y-2 pt-2">
            <div className="flex items-center gap-1 text-xs font-black text-gray-400 uppercase tracking-widest">
              <Tag size={12} /> Coupon Code
            </div>
            <div className="flex gap-2">
              <input
                type="text"
                placeholder="Enter code"
                value={coupon}
                onChange={(e) => { setCoupon(e.target.value.toUpperCase()); setCouponError(""); }}
                className="flex-1 border rounded-xl px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-pink-500 uppercase"
              />
              <button
                onClick={applyCoupon}
                disabled={couponLoading || selectedItems.length === 0}
                className="px-4 py-2 bg-gray-900 text-white text-sm font-bold rounded-xl disabled:opacity-50 flex items-center gap-1"
              >
                {couponLoading ? <Loader2 size={14} className="animate-spin" /> : "Apply"}
              </button>
            </div>
            {couponError && <p className="text-red-500 text-xs font-bold">{couponError}</p>}
            {discountApplied && <p className="text-green-600 text-xs font-bold">✓ Coupon applied!</p>}
          </div>

          {/* Selection error */}
          {selectionError && (
            <p className="text-red-500 text-xs font-bold bg-red-50 border border-red-100 rounded-xl px-3 py-2">
              {selectionError}
            </p>
          )}

          <button
            onClick={handleProceedToCheckout}
            className="w-full bg-pink-600 hover:bg-pink-700 text-white font-black py-4 rounded-2xl text-base shadow-lg active:scale-95 transition-all mt-2 disabled:opacity-50"
          >
            {selectedItems.length > 0
              ? `Checkout ${selectedItems.length} Item${selectedItems.length > 1 ? "s" : ""} →`
              : "Select Items to Checkout"
            }
          </button>

          <div className="text-xs text-gray-400 space-y-1 pt-2">
            <p>🔐 Safe & Secure Payments</p>
            <p>🔄 7 Days Return Policy</p>
            <p>✅ 100% Original Products</p>
          </div>
        </div>
      </div>

      {/* Mobile sticky checkout */}
      <div className="fixed bottom-0 left-0 w-full bg-white border-t shadow-lg p-4 md:hidden z-50">
        {selectionError && (
          <p className="text-red-500 text-xs font-bold text-center mb-2">{selectionError}</p>
        )}
        <button
          onClick={handleProceedToCheckout}
          className="w-full bg-pink-600 text-white font-black py-3 rounded-2xl"
        >
          {selectedItems.length > 0
            ? `Checkout ${selectedItems.length} Item${selectedItems.length > 1 ? "s" : ""} · ₹${finalTotal.toLocaleString()}`
            : "Select Items to Checkout"
          }
        </button>
      </div>

      {/* Stock limit toast */}
      {stockToast && (
        <div className="fixed top-6 left-1/2 -translate-x-1/2 z-[70] animate-bounce pointer-events-none">
          <div className="bg-orange-600 text-white px-6 py-3 rounded-2xl shadow-2xl text-sm font-bold flex items-center gap-2">
            <span>⚠️</span>
            <span>{stockToast}</span>
          </div>
        </div>
      )}
    </div>
  );
};

export default CartPage;
