import { useState, useContext } from "react";
import { useNavigate } from "react-router-dom";
import { CartContext } from "../context/CartContext";

const CartPage = () => {
  const navigate = useNavigate();
  const { cartItems, removeFromCart, updateQuantity } = useContext(CartContext);
  const [coupon, setCoupon] = useState("");
  const [discountAmount, setDiscountAmount] = useState(0);

  // Remove Item
  const removeItem = (item) => {
    removeFromCart(item.id, item.activeVariant?.id);
  };

  // Quantity Increase
  const increaseQty = (item) => {
    updateQuantity(item.id, item.activeVariant?.id, (item.cartQuantity || 1) + 1);
  };

  // Quantity Decrease
  const decreaseQty = (item) => {
    if ((item.cartQuantity || 1) > 1) {
      updateQuantity(item.id, item.activeVariant?.id, (item.cartQuantity || 1) - 1);
    }
  };

  // Price Calculations
  const totalMRP = cartItems.reduce(
    (total, item) => total + (item.price || 0) * (item.cartQuantity || 1),
    0
  );

  const deliveryCharge = totalMRP > 999 ? 0 : 99;
  const finalTotal = totalMRP - discountAmount + deliveryCharge;

  // Apply Coupon
  const applyCoupon = () => {
    if (coupon === "SAVE10") {
      setDiscountAmount(200);
      alert("Coupon Applied! ₹200 Discount");
    } else {
      alert("Invalid Coupon Code");
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-6 py-10">
      <h1 className="text-3xl font-bold mb-8">🛒 Your Cart</h1>

      {cartItems.length === 0 ? (
        <p>Your cart is empty.</p>
      ) : (
        <div className="grid md:grid-cols-3 gap-8">

          {/* LEFT SIDE - CART ITEMS */}
          <div className="md:col-span-2 space-y-6">
            {cartItems.map((item, index) => (
              <div key={index} className="border p-5 rounded-lg shadow-sm">

                <div className="flex gap-5 flex-col md:flex-row">

                  {/* Image */}
                  <img
                    src={item.image || (item.images && item.images[0]) || "https://via.placeholder.com/150"}
                    alt={item.name}
                    className="w-32 h-32 object-cover rounded"
                  />

                  {/* Info */}
                  <div className="flex-1">
                    <h2 className="text-lg font-semibold">
                      {item.name}
                    </h2>
                    <p className="text-sm text-gray-500">
                      Product ID: {item.id}
                    </p>
                    <p>Color: {item.activeVariant?.color || item.color}</p>
                    <p>Size: {item.activeVariant?.size || item.size}</p>

                    {/* Stock Warning */}
                    <p className="text-red-500 text-sm mt-1">
                      {item.activeVariant && item.activeVariant.quantity < 5 ? `Only ${item.activeVariant.quantity} left in stock!` : ""}
                    </p>

                    {/* Quantity Selector */}
                    <div className="flex items-center gap-3 mt-3">
                      <button
                        onClick={() => decreaseQty(item)}
                        className="border px-3 py-1"
                      >
                        −
                      </button>
                      <span>{item.cartQuantity || 1}</span>
                      <button
                        onClick={() => increaseQty(item)}
                        className="border px-3 py-1"
                      >
                        +
                      </button>
                    </div>

                    <p className="font-bold mt-3">
                      ₹{item.price} × {item.cartQuantity || 1}
                    </p>

                    {/* Actions */}
                    <div className="flex gap-4 mt-3 text-sm">
                      <button
                        onClick={() => removeItem(item)}
                        className="text-red-600"
                      >
                        ❌ Remove
                      </button>
                      <button className="text-blue-600">
                        ❤️ Move to Wishlist
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            ))}

            {/* Continue Shopping */}
            <button
              onClick={() => navigate("/")}
              className="text-blue-600 underline"
            >
              🛍 Continue Shopping
            </button>
          </div>

          {/* RIGHT SIDE - PRICE DETAILS */}
          <div className="border p-6 rounded-lg shadow-sm h-fit">

            <h2 className="text-xl font-semibold mb-4">
              💰 Price Details
            </h2>

            <div className="space-y-2 text-sm">
              <p>Price ({cartItems.length} items): ₹{totalMRP}</p>
              <p className="text-green-600">
                Discount: -₹{discountAmount}
              </p>
              <p>
                Delivery:{" "}
                {deliveryCharge === 0 ? "Free" : `₹${deliveryCharge}`}
              </p>
              <p>Platform Fee: ₹0</p>
            </div>

            <hr className="my-4" />

            <p className="text-lg font-bold">
              Total Amount: ₹{finalTotal}
            </p>

            {/* Coupon Section */}
            <div className="mt-6">
              <input
                type="text"
                placeholder="Enter Coupon Code"
                value={coupon}
                onChange={(e) => setCoupon(e.target.value)}
                className="border p-2 w-full mb-2"
              />
              <button
                onClick={applyCoupon}
                className="bg-black text-white px-4 py-2 w-full"
              >
                Apply Coupon
              </button>
            </div>

            {/* Delivery Preview */}
            <div className="mt-6 text-sm">
              <p className="font-semibold">🚚 Deliver To:</p>
              <p>John Doe</p>
              <p>Mumbai, Maharashtra - 400001</p>
              <p className="text-green-600 mt-2">
                Estimated Delivery: 3 March
              </p>
            </div>

            {/* Checkout Button */}
            <button className="bg-yellow-500 text-black font-bold w-full py-3 mt-6 rounded">
              ⚡ Proceed to Checkout
            </button>

            {/* Security Message */}
            <div className="text-xs text-gray-500 mt-6 space-y-1">
              <p>🔐 Safe & Secure Payments</p>
              <p>🔄 7 Days Return Policy</p>
              <p>✅ 100% Original Products</p>
            </div>
          </div>
        </div>
      )}

      {/* Sticky Mobile Checkout */}
      {cartItems.length > 0 && (
        <div className="fixed bottom-0 left-0 w-full bg-white shadow-md p-4 md:hidden">
          <button className="bg-yellow-500 w-full py-3 font-bold">
            ⚡ Proceed to Checkout ₹{finalTotal}
          </button>
        </div>
      )}
    </div>
  );
};

export default CartPage;