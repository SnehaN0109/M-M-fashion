import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

const CheckoutPage = () => {
  const navigate = useNavigate();
  const [product, setProduct] = useState(null);

  useEffect(() => {
    const item = JSON.parse(localStorage.getItem("buyNowItem"));
    if (!item) navigate("/");
    else setProduct(item);
  }, [navigate]);

  if (!product) return null;

  const mrp = product.originalPrice * product.quantity;
  const sellingPrice = product.price * product.quantity;
  const discount = mrp - sellingPrice;
  const platformFee = 7;
  const totalAmount = sellingPrice + platformFee;

  // ✅ UPDATED FUNCTION
  const handleContinue = () => {
    const orderId = "OD" + Date.now();

    const orderData = {
      ...product,
      orderId,
      totalAmount,
      date: new Date().toLocaleDateString(),
    };

    // Save as pending order (not final yet)
    localStorage.setItem("pendingOrder", JSON.stringify(orderData));

    // Navigate to Payment Page
    navigate("/payment");
  };

  return (
    <div className="bg-gray-100 min-h-screen pb-28">

      {/* HEADER */}
      <div className="bg-white shadow-sm">
        <div className="max-w-5xl mx-auto p-4">
          <h1 className="text-2xl font-bold">Order Summary</h1>

          <div className="flex justify-between mt-4 text-sm">
            <span className="text-gray-500">1 Address</span>
            <span className="font-bold text-blue-600">
              2 Order Summary
            </span>
            <span className="text-gray-500">3 Payment</span>
          </div>
        </div>
      </div>

      <div className="max-w-5xl mx-auto mt-5 space-y-4">

        {/* ADDRESS CARD */}
        <div className="bg-white p-5 rounded shadow-sm">
          <div className="flex justify-between items-center">
            <h2 className="font-semibold text-lg">Deliver to</h2>
            <button className="text-blue-600 text-sm font-medium">
              Change
            </button>
          </div>

          <div className="mt-3 text-sm text-gray-700">
            <p className="font-semibold">John Doe</p>
            <p>Andheri West, Mumbai - 400001</p>
            <p>9876543210</p>
          </div>
        </div>

        {/* PRODUCT CARD */}
        <div className="bg-white p-5 rounded shadow-sm">
          <div className="flex gap-5">
            <img
              src={product.image}
              alt={product.name}
              className="w-28 h-28 object-cover rounded border"
            />

            <div className="flex-1">
              <p className="font-semibold text-lg">{product.name}</p>
              <p className="text-sm text-gray-500 mt-1">
                Size: {product.size} | Color: {product.color}
              </p>

              <div className="flex items-center gap-3 mt-3">
                <span className="text-green-600 text-xl font-bold">
                  ₹{product.price}
                </span>
                <span className="line-through text-gray-400">
                  ₹{product.originalPrice}
                </span>
                <span className="text-green-600 text-sm font-medium">
                  {Math.round((discount / mrp) * 100)}% off
                </span>
              </div>

              <p className="text-sm text-gray-500 mt-2">
                Quantity: {product.quantity}
              </p>

              <p className="text-sm text-gray-500 mt-1">
                Delivery within 5 days
              </p>
            </div>
          </div>
        </div>

        {/* PRICE DETAILS */}
        <div className="bg-white p-5 rounded shadow-sm">
          <h2 className="font-semibold text-lg mb-4">Price Details</h2>

          <div className="space-y-2 text-sm">
            <div className="flex justify-between">
              <span>MRP</span>
              <span>₹{mrp}</span>
            </div>

            <div className="flex justify-between">
              <span>Selling Price</span>
              <span>₹{sellingPrice}</span>
            </div>

            <div className="flex justify-between">
              <span>Platform Fee</span>
              <span>₹{platformFee}</span>
            </div>

            <div className="flex justify-between text-green-600">
              <span>Discount</span>
              <span>-₹{discount}</span>
            </div>

            <hr className="my-3" />

            <div className="flex justify-between font-bold text-lg">
              <span>Total Amount</span>
              <span>₹{totalAmount}</span>
            </div>
          </div>

          <p className="text-green-600 text-sm mt-3">
            🎉 You save ₹{discount} on this order!
          </p>
        </div>
      </div>

      {/* STICKY BOTTOM BAR */}
      <div className="fixed bottom-0 left-0 w-full bg-white border-t shadow-lg">
        <div className="max-w-5xl mx-auto p-4 flex justify-between items-center">
          <div>
            <p className="text-sm text-gray-400 line-through">
              ₹{mrp}
            </p>
            <p className="text-xl font-bold">
              ₹{totalAmount}
            </p>
          </div>

          <button
            onClick={handleContinue}
            className="bg-yellow-500 hover:bg-yellow-600 px-10 py-3 rounded font-semibold transition"
          >
            Continue
          </button>
        </div>
      </div>

    </div>
  );
};

export default CheckoutPage;