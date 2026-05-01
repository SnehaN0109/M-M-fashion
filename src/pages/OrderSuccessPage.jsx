import { useEffect, useState } from "react";
import { useNavigate, useLocation, Link } from "react-router-dom";
import { CheckCircle, ShoppingBag, Truck, Home, Loader2, AlertCircle, Package } from "lucide-react";

const OrderSuccessPage = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const order_id = location.state?.order_id;

  const [order, setOrder] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    // If no order_id, redirect to home
    if (!order_id) {
      navigate("/");
      return;
    }

    // Fetch order details from API
    const fetchOrder = async () => {
      try {
        const res = await fetch(`${import.meta.env.VITE_API_URL}/api/orders/track/${order_id}`);
        if (!res.ok) {
          throw new Error("Order not found");
        }
        const data = await res.json();
        setOrder(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchOrder();
  }, [order_id, navigate]);

  // Loading state
  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex flex-col items-center justify-center px-6">
        <Loader2 className="w-12 h-12 text-pink-600 animate-spin mb-4" />
        <p className="text-gray-600 font-medium">Loading order details...</p>
      </div>
    );
  }

  // Error state
  if (error || !order) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center px-6">
        <div className="max-w-md w-full bg-white rounded-3xl shadow-xl p-10 text-center">
          <div className="flex justify-center mb-6">
            <div className="w-20 h-20 bg-red-50 rounded-full flex items-center justify-center">
              <AlertCircle size={48} className="text-red-500" />
            </div>
          </div>
          <h1 className="text-2xl font-black text-gray-900 mb-2">Order Not Found</h1>
          <p className="text-gray-500 mb-8">
            We couldn't find this order. Please check your email for order confirmation or view your orders.
          </p>
          <div className="flex flex-col gap-3">
            <Link
              to="/my-orders"
              className="flex items-center justify-center gap-2 bg-gray-900 text-white font-bold py-3 rounded-2xl hover:bg-black transition"
            >
              <Package size={18} /> View My Orders
            </Link>
            <Link
              to="/"
              className="flex items-center justify-center gap-2 bg-pink-600 text-white font-bold py-3 rounded-2xl hover:bg-pink-700 transition"
            >
              <Home size={18} /> Go to Home
            </Link>
          </div>
        </div>
      </div>
    );
  }

  // Calculate estimated delivery (5 days from order date)
  const estimatedDelivery = new Date(order.created_at);
  estimatedDelivery.setDate(estimatedDelivery.getDate() + 5);

  const orderDate = new Date(order.created_at).toLocaleDateString('en-IN', {
    day: 'numeric',
    month: 'long',
    year: 'numeric'
  });

  return (
    <div className="min-h-screen bg-gray-50 py-10 px-6">
      <div className="max-w-4xl mx-auto">

        {/* Success Header */}
        <div className="bg-white rounded-3xl shadow-xl p-10 text-center mb-6">
          <div className="flex justify-center mb-6">
            <div className="w-20 h-20 bg-green-50 rounded-full flex items-center justify-center">
              <CheckCircle size={48} className="text-green-500" />
            </div>
          </div>

          <h1 className="text-3xl font-black text-gray-900 tracking-tight mb-2">
            Order Placed Successfully!
          </h1>
          <p className="text-gray-500 font-medium mb-6">
            Thank you for your order. We'll send you a confirmation email shortly.
          </p>

          {/* Order ID Badge */}
          <div className="inline-block bg-gray-100 rounded-full px-6 py-2">
            <span className="text-xs font-bold text-gray-500 uppercase tracking-wider">Order ID</span>
            <span className="ml-2 text-lg font-black text-gray-900">#{order.order_id}</span>
          </div>
        </div>

        <div className="grid lg:grid-cols-3 gap-6">

          {/* Left: Order Details */}
          <div className="lg:col-span-2 space-y-6">

            {/* Order Items */}
            <div className="bg-white rounded-2xl shadow-sm p-6">
              <h2 className="font-black text-lg text-gray-900 mb-4">Order Items</h2>
              <div className="space-y-4">
                {order.items.map((item, i) => (
                  <div key={i} className="flex gap-4 items-center pb-4 border-b last:border-b-0">
                    <img
                      src={item.image_url || "https://via.placeholder.com/80"}
                      className="w-20 h-20 rounded-xl object-cover border border-gray-100"
                      alt={item.product_name}
                    />
                    <div className="flex-1 min-w-0">
                      <p className="font-bold text-gray-900 truncate">{item.product_name}</p>
                      <p className="text-sm text-gray-500">
                        {item.color} · {item.size} · Qty: {item.quantity}
                      </p>
                    </div>
                    <p className="font-black text-gray-900">
                      ₹{(item.price_at_purchase * item.quantity).toLocaleString()}
                    </p>
                  </div>
                ))}
              </div>
            </div>

            {/* Shipping Address */}
            <div className="bg-white rounded-2xl shadow-sm p-6">
              <h2 className="font-black text-lg text-gray-900 mb-4 flex items-center gap-2">
                <Truck size={20} className="text-pink-600" /> Shipping Address
              </h2>
              <div className="text-sm text-gray-700 space-y-1">
                <p className="font-bold">{order.customer_name}</p>
                <p>{order.address.line1}</p>
                {order.address.line2 && <p>{order.address.line2}</p>}
                <p>{order.address.city}, {order.address.state} - {order.address.pincode}</p>
                <p className="pt-2 text-gray-500">Phone: {order.customer_phone}</p>
                <p className="text-gray-500">Email: {order.customer_email}</p>
              </div>
            </div>

          </div>

          {/* Right: Order Summary */}
          <div className="space-y-6">

            {/* Price Summary */}
            <div className="bg-white rounded-2xl shadow-sm p-6 sticky top-24">
              <h2 className="font-black text-lg text-gray-900 mb-4">Order Summary</h2>

              <div className="space-y-2 text-sm">
                <div className="flex justify-between text-gray-600">
                  <span>Subtotal</span>
                  <span>₹{order.subtotal.toLocaleString()}</span>
                </div>
                {order.discount_amount > 0 && (
                  <div className="flex justify-between text-green-600 font-bold">
                    <span>Discount {order.discount_code && `(${order.discount_code})`}</span>
                    <span>−₹{order.discount_amount.toLocaleString()}</span>
                  </div>
                )}
                <div className="flex justify-between text-gray-600">
                  <span>Shipping</span>
                  <span>{order.shipping_charge === 0 ? "Free" : `₹${order.shipping_charge}`}</span>
                </div>
                <div className="flex justify-between font-black text-lg text-gray-900 border-t pt-3 mt-2">
                  <span>Total</span>
                  <span>₹{order.total_amount.toLocaleString()}</span>
                </div>
              </div>

              {/* Order Info */}
              <div className="mt-6 pt-6 border-t space-y-2 text-sm">
                <div className="flex justify-between">
                  <span className="text-gray-500">Order Date</span>
                  <span className="font-bold text-gray-900">{orderDate}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-500">Payment</span>
                  <span className="font-bold text-gray-900">Cash on Delivery</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-500">Estimated Delivery</span>
                  <span className="font-bold text-green-600">
                    {estimatedDelivery.toLocaleDateString('en-IN', { day: 'numeric', month: 'long' })}
                  </span>
                </div>
              </div>

              {/* COD Note */}
              <div className="mt-6 bg-yellow-50 border border-yellow-100 rounded-xl p-3 text-xs text-yellow-800 font-medium">
                💵 Cash on Delivery: Please keep the exact amount ready at delivery.
              </div>

              {/* Actions */}
              <div className="mt-6 space-y-3">
                <Link
                  to={`/trackorder/${order.order_id}`}
                  className="w-full flex items-center justify-center gap-2 bg-gray-900 text-white font-bold py-3 rounded-2xl hover:bg-black transition"
                >
                  <Truck size={18} /> Track Order
                </Link>
                <Link
                  to="/"
                  className="w-full flex items-center justify-center gap-2 bg-pink-600 text-white font-bold py-3 rounded-2xl hover:bg-pink-700 transition"
                >
                  <Home size={18} /> Continue Shopping
                </Link>
              </div>

              <p className="text-center text-xs text-gray-400 mt-4">
                🔐 Safe & Secure · 7 Day Returns
              </p>
            </div>

          </div>

        </div>
      </div>
    </div>
  );
};

export default OrderSuccessPage;
