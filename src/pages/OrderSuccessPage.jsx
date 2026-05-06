import { useEffect, useState } from "react";
import { useNavigate, useLocation, Link } from "react-router-dom";
import { CheckCircle, ShoppingBag, Truck, Home, Loader2, AlertCircle, Package } from "lucide-react";
import PaymentInstructions from "../components/PaymentInstructions";

const OrderSuccessPage = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const order_id = location.state?.order_id;
  const paymentMethod = location.state?.paymentMethod || "UPI";
  const totalFromNav = location.state?.total;

  const [order, setOrder] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);


  // Extracted so it can be called again after payment proof upload
  const fetchOrder = async () => {
    try {
      const res = await fetch(`${import.meta.env.VITE_API_URL}/api/orders/track/${order_id}`, {
        headers: {
          'Cache-Control': 'no-cache, no-store, must-revalidate',
          'Pragma': 'no-cache',
          'Expires': '0'
        }
      });
      if (!res.ok) throw new Error("Order not found");
      const data = await res.json();
      

      setOrder(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (!order_id) {
      navigate("/");
      return;
    }
    fetchOrder();
  }, [order_id, navigate]);

  // ── Poll every 5 s while payment is not yet confirmed ─────────────────────
  useEffect(() => {
    if (!order_id) return;

    const interval = setInterval(async () => {
      // Stop polling if order is in a terminal status for this page
      if (order?.status === 'PLACED' || order?.status === 'CONFIRMED' || order?.status === 'CANCELLED' || order?.status === 'REJECTED' || order?.payment_status === 'VERIFIED') {
        clearInterval(interval);
        return;
      }
      try {
        const res = await fetch(`${import.meta.env.VITE_API_URL}/api/orders/track/${order_id}`, {
          headers: {
            'Cache-Control': 'no-cache, no-store, must-revalidate',
            'Pragma': 'no-cache',
            'Expires': '0'
          }
        });
        if (!res.ok) return;
        const data = await res.json();
        

        setOrder(data);

        // Stop polling once confirmed or rejected
        if (data.status === 'PLACED' || data.status === 'CONFIRMED' || data.status === 'CANCELLED' || data.status === 'REJECTED' || data.payment_status === 'VERIFIED') {
          clearInterval(interval);
        }
      } catch {
        // silent — keep polling
      }
    }, 5000);

    return () => clearInterval(interval);
  }, [order_id, order?.status]);

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
    <div className="min-h-screen bg-gray-50 py-6 px-4 md:px-6 relative overflow-hidden">
      

      <div className="max-w-4xl mx-auto">

        {/* Status-based Header */}
        {(() => {
          const isConfirmed = order.status === 'PLACED' || order.status === 'CONFIRMED' || order.payment_status === 'VERIFIED';
          const isRejected  = order.status === 'CANCELLED' || order.status === 'REJECTED' || order.payment_status === 'FAILED';
          const isPaid      = order.status === 'PAID' || (order.payment_proof && !isConfirmed && !isRejected);

          if (isConfirmed) {
            return (
              <div className="bg-white rounded-2xl shadow-sm p-6 text-center mb-4">
                <div className="flex justify-center mb-4">
                  <div className="w-16 h-16 bg-green-50 rounded-full flex items-center justify-center">
                    <CheckCircle size={32} className="text-green-500" />
                  </div>
                </div>
                <h1 className="text-2xl font-black text-gray-900 mb-1">Order Confirmed!</h1>
                <p className="text-gray-500 text-sm mb-4">Payment verified. Confirmation sent.</p>
                <div className="inline-block bg-gray-100 rounded-full px-4 py-1.5">
                  <span className="text-[10px] font-bold text-gray-500 uppercase tracking-wider">Order ID</span>
                  <span className="ml-2 text-base font-black text-gray-900">#{order.order_id}</span>
                </div>
              </div>
            );
          }

          if (isRejected) {
            return (
              <div className="bg-white rounded-2xl shadow-sm p-6 text-center mb-4">
                <div className="flex justify-center mb-4">
                  <div className="w-16 h-16 bg-red-50 rounded-full flex items-center justify-center">
                    <AlertCircle size={32} className="text-red-500" />
                  </div>
                </div>
                <h1 className="text-2xl font-black text-gray-900 mb-1">Payment Rejected</h1>
                <p className="text-red-500 text-sm mb-4">Verification failed. Please upload valid screenshot again.</p>
                <div className="inline-block bg-gray-100 rounded-full px-4 py-1.5">
                  <span className="text-[10px] font-bold text-gray-500 uppercase tracking-wider">Order ID</span>
                  <span className="ml-2 text-base font-black text-gray-900">#{order.order_id}</span>
                </div>
              </div>
            );
          }

          if (isPaid) {
            return (
              <div className="bg-white rounded-2xl shadow-sm p-6 text-center mb-4">
                <div className="flex justify-center mb-4">
                  <div className="w-16 h-16 bg-blue-50 rounded-full flex items-center justify-center">
                    <Loader2 size={32} className="text-blue-500 animate-spin" />
                  </div>
                </div>
                <h1 className="text-2xl font-black text-gray-900 mb-1">Proof Uploaded</h1>
                <p className="text-gray-500 text-sm mb-4">Waiting for verification. Confirmed once approved.</p>
                <div className="inline-block bg-gray-100 rounded-full px-4 py-1.5">
                  <span className="text-[10px] font-bold text-gray-500 uppercase tracking-wider">Order ID</span>
                  <span className="ml-2 text-base font-black text-gray-900">#{order.order_id}</span>
                </div>
              </div>
            );
          }

          return (
            <div className="bg-white rounded-2xl shadow-sm p-6 text-center mb-4">
              <div className="flex justify-center mb-4">
                <div className="w-16 h-16 bg-amber-50 rounded-full flex items-center justify-center">
                  <ShoppingBag size={32} className="text-amber-500" />
                </div>
              </div>
              <h1 className="text-2xl font-black text-gray-900 mb-1">Order Placed!</h1>
              <p className="text-amber-600 text-sm mb-4">Upload UPI screenshot below to confirm.</p>
              <div className="inline-block bg-gray-100 rounded-full px-4 py-1.5">
                <span className="text-[10px] font-bold text-gray-500 uppercase tracking-wider">Order ID</span>
                <span className="ml-2 text-base font-black text-gray-900">#{order.order_id}</span>
              </div>
            </div>
          );
        })()}

        <div className="grid lg:grid-cols-3 gap-4">

          {/* Left: Order Details */}
          <div className="lg:col-span-2 space-y-4">

            {/* Order Items */}
            <div className="bg-white rounded-2xl shadow-sm p-4">
              <h2 className="font-black text-sm text-gray-900 mb-3 uppercase tracking-wider">Items</h2>
              <div className="space-y-3">
                {order.items.map((item, i) => (
                  <div key={i} className="flex gap-3 items-center pb-3 border-b last:border-b-0">
                    <img
                      src={item.image_url || "https://via.placeholder.com/60"}
                      className="w-14 h-14 rounded-lg object-cover border border-gray-100"
                      alt={item.product_name}
                    />
                    <div className="flex-1 min-w-0">
                      <p className="font-bold text-xs text-gray-900 truncate">{item.product_name}</p>
                      <p className="text-[10px] text-gray-500">
                        {item.color} · {item.size} · Qty: {item.quantity}
                      </p>
                    </div>
                    <p className="font-black text-xs text-gray-900">
                      ₹{(item.price_at_purchase * item.quantity).toLocaleString()}
                    </p>
                  </div>
                ))}
              </div>
            </div>

            {/* Shipping Address */}
            <div className="bg-white rounded-2xl shadow-sm p-4">
              <h2 className="font-black text-sm text-gray-900 mb-3 flex items-center gap-2 uppercase tracking-wider">
                <Truck size={16} className="text-pink-600" /> Shipping
              </h2>
              <div className="text-xs text-gray-700 space-y-0.5">
                <p className="font-bold">{order.customer_name}</p>
                <p>{order.address.line1}, {order.address.city}</p>
                <p>{order.address.state} - {order.address.pincode}</p>
                <p className="pt-1 text-gray-400 font-medium">Phone: {order.customer_phone}</p>
              </div>
            </div>

          </div>

          {/* Right: Order Summary */}
          <div className="space-y-6">

            {/* Price Summary */}
            <div className="bg-white rounded-2xl shadow-sm p-4 sticky top-24 border border-gray-100">
              <h2 className="font-black text-sm text-gray-900 mb-3 uppercase tracking-wider">Order Summary</h2>

              <div className="space-y-1.5 text-xs border-b pb-3">
                <div className="flex justify-between text-gray-500">
                  <span>Subtotal</span>
                  <span className="font-bold text-gray-900">₹{order.subtotal.toLocaleString()}</span>
                </div>
                {order.discount_amount > 0 && (
                  <div className="flex justify-between text-green-600 font-bold">
                    <span>Discount {order.discount_code && `(${order.discount_code})`}</span>
                    <span>−₹{order.discount_amount.toLocaleString()}</span>
                  </div>
                )}
                <div className="flex justify-between text-gray-500">
                  <span>Shipping</span>
                  <span className="font-bold text-gray-900">{order.shipping_charge === 0 ? "Free" : `₹${order.shipping_charge}`}</span>
                </div>
                <div className="flex justify-between font-black text-sm text-gray-900 pt-1">
                  <span>Total</span>
                  <span className="text-pink-600">₹{order.total_amount.toLocaleString()}</span>
                </div>
              </div>

              {/* Order Info */}
              <div className="mt-3 space-y-1.5 text-[10px] uppercase tracking-tighter">
                <div className="flex justify-between">
                  <span className="text-gray-400 font-bold">Order Date</span>
                  <span className="font-black text-gray-700">{orderDate}</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-gray-400 font-bold">Status</span>
                  <span className={`font-black px-2 py-0.5 rounded-full ${
                    (order.status === 'CONFIRMED' || order.status === 'PLACED' || order.payment_status === 'VERIFIED')
                      ? 'bg-green-100 text-green-700'
                      : order.status === 'PAID'
                      ? 'bg-blue-100 text-blue-700'
                      : (order.status === 'REJECTED' || order.status === 'CANCELLED')
                      ? 'bg-red-100 text-red-700'
                      : 'bg-amber-100 text-amber-700'
                  }`}>
                    {(order.status === 'CONFIRMED' || order.status === 'PLACED' || order.payment_status === 'VERIFIED')
                      ? 'Confirmed'
                      : order.status === 'PAID'
                      ? 'Paid'
                      : (order.status === 'REJECTED' || order.status === 'CANCELLED')
                      ? 'Rejected'
                      : 'Pending'}
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-400 font-bold">Tracking</span>
                  <span className={`font-black ${order.tracking_number ? 'text-blue-600' : 'text-gray-400'}`}>
                    {order.tracking_number || 'TBA'}
                  </span>
                </div>
              </div>

              {/* UPI payment instructions — hidden if confirmed or rejected */}
              {!(order.status === 'PLACED' || order.status === 'CONFIRMED' || order.payment_status === 'VERIFIED' || order.status === 'CANCELLED' || order.status === 'REJECTED' || order.payment_status === 'FAILED') && (
                <PaymentInstructions
                  orderId={order.order_id}
                  totalAmount={order.total_amount || totalFromNav}
                  alreadyUploaded={!!order.payment_proof}
                  onPaymentMarked={fetchOrder}
                  paymentMethod={paymentMethod}
                />
              )}

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
