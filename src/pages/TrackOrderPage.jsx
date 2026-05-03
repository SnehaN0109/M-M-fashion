import { useState, useEffect } from "react";
import { useParams, Link } from "react-router-dom";
import { Loader2, Package, CheckCircle, Truck, MapPin, Box, Home } from "lucide-react";

const STATUS_STEPS = [
  { key: "PENDING_PAYMENT", label: "Pending Payment", icon: Package },
  { key: "PLACED",          label: "Order Placed",    icon: CheckCircle },
  { key: "PACKED",          label: "Packed",          icon: Box },
  { key: "SHIPPED",         label: "Shipped",         icon: Truck },
  { key: "OUT_FOR_DELIVERY",label: "Out For Delivery",icon: MapPin },
  { key: "DELIVERED",       label: "Delivered",       icon: Home },
];

const STATUS_INDEX = {
  PENDING_PAYMENT: 0,
  PLACED: 1,
  PACKED: 2,
  SHIPPED: 3,
  OUT_FOR_DELIVERY: 4,
  DELIVERED: 5,
  CANCELLED: -1,
};

const TrackOrderPage = () => {
  const { orderId } = useParams();
  const [order, setOrder] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!orderId) return;
    fetch(`${import.meta.env.VITE_API_URL}/api/orders/track/${orderId}`)
      .then((r) => {
        if (!r.ok) throw new Error("Order not found.");
        return r.json();
      })
      .then(setOrder)
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, [orderId]);

  if (loading) return (
    <div className="min-h-screen flex items-center justify-center">
      <Loader2 className="w-10 h-10 text-pink-600 animate-spin" />
    </div>
  );

  if (error) return (
    <div className="min-h-screen flex flex-col items-center justify-center gap-4 px-6">
      <Package size={48} className="text-gray-200" />
      <p className="text-xl font-black text-gray-500">{error}</p>
      <Link to="/my-orders" className="px-6 py-3 bg-pink-600 text-white font-bold rounded-2xl text-sm">
        My Orders
      </Link>
    </div>
  );

  if (!order) return null;

  const normStatus = (order.status || "PENDING_PAYMENT").toUpperCase();
  const currentStep = STATUS_INDEX[normStatus] ?? 0;
  const isCancelled = normStatus === "CANCELLED";

  return (
    <div className="max-w-2xl mx-auto px-6 py-10">

      {/* Header */}
      <div className="mb-8">
        <p className="text-xs font-black text-pink-600 uppercase tracking-widest mb-1">Order Tracking</p>
        <h1 className="text-3xl font-black text-gray-900">Order #{order.order_id}</h1>
        <p className="text-sm text-gray-400 mt-1">
          Placed on {new Date(order.created_at).toLocaleDateString("en-IN", { day: "numeric", month: "long", year: "numeric" })}
        </p>
      </div>

      {(order.payment_status || "PENDING").toUpperCase() === "PENDING" && !isCancelled && (
        <div className="bg-yellow-50 border border-yellow-200 rounded-2xl p-4 mb-6 flex items-center justify-center">
          <p className="text-sm font-black text-yellow-700">Waiting for payment verification</p>
        </div>
      )}

      {/* Status Timeline */}
      <div className="bg-white border rounded-2xl p-6 mb-6">
        <h2 className="text-sm font-black text-gray-400 uppercase tracking-widest mb-6">Status</h2>

        {isCancelled ? (
          <div className="bg-red-50 border border-red-100 rounded-xl p-4 text-center">
            <p className="font-black text-red-600 text-lg">Order Cancelled</p>
            <p className="text-sm text-red-400 mt-1">This order has been cancelled.</p>
          </div>
        ) : (
          <div className="relative">
            {/* Progress line */}
            <div className="absolute top-5 left-5 right-5 h-0.5 bg-gray-100" />
            <div
              className="absolute top-5 left-5 h-0.5 bg-pink-500 transition-all duration-700"
              style={{ width: `${(currentStep / (STATUS_STEPS.length - 1)) * 100}%` }}
            />

            <div className="relative flex justify-between">
              {STATUS_STEPS.map((step, i) => {
                const Icon = step.icon;
                const done = i <= currentStep;
                const active = i === currentStep;
                return (
                  <div key={step.key} className="flex flex-col items-center gap-2 w-16">
                    <div className={`w-10 h-10 rounded-full flex items-center justify-center z-10 transition-all ${
                      done ? "bg-pink-600 text-white shadow-lg" : "bg-gray-100 text-gray-300"
                    } ${active ? "ring-4 ring-pink-100 scale-110" : ""}`}>
                      <Icon size={18} />
                    </div>
                    <p className={`text-[10px] font-black text-center leading-tight ${done ? "text-gray-900" : "text-gray-300"}`}>
                      {step.label}
                    </p>
                  </div>
                );
              })}
            </div>
          </div>
        )}
      </div>

      {/* Tracking Number */}
      {order.tracking_number ? (
        <div className="bg-blue-50 border border-blue-100 rounded-2xl p-5 mb-6 flex items-center gap-3">
          <Truck size={20} className="text-blue-500 flex-shrink-0" />
          <div>
            <p className="text-xs font-black text-blue-400 uppercase tracking-widest">Tracking Number</p>
            <p className="font-black text-blue-700 text-lg">{order.tracking_number}</p>
          </div>
        </div>
      ) : (
        <div className="bg-gray-50 border border-gray-200 rounded-2xl p-5 mb-6 flex items-center gap-3">
          <Package size={20} className="text-gray-400 flex-shrink-0" />
          <div>
            <p className="text-xs font-black text-gray-400 uppercase tracking-widest">Tracking Number</p>
            <p className="font-bold text-gray-500">
              {(order.payment_status || '').toUpperCase() === 'PENDING'
                ? 'Awaiting payment verification...'
                : 'Processing...'}
            </p>
          </div>
        </div>
      )}

      {/* Order Info */}
      <div className="bg-white border rounded-2xl p-6 mb-6 space-y-4">
        <h2 className="text-sm font-black text-gray-400 uppercase tracking-widest">Order Info</h2>
        <div className="grid grid-cols-2 gap-4 text-sm">
          <div>
            <p className="text-xs text-gray-400 font-black uppercase tracking-widest">Customer</p>
            <p className="font-bold text-gray-900 mt-0.5">{order.customer_name}</p>
          </div>
          <div>
            <p className="text-xs text-gray-400 font-black uppercase tracking-widest">Payment</p>
            <p className="font-bold text-gray-900 mt-0.5">{order.payment_method || "UPI"}</p>
          </div>
          <div>
            <p className="text-xs text-gray-400 font-black uppercase tracking-widest">Items</p>
            <p className="font-bold text-gray-900 mt-0.5">{order.items?.length} item{order.items?.length !== 1 ? "s" : ""}</p>
          </div>
          <div>
            <p className="text-xs text-gray-400 font-black uppercase tracking-widest">Total</p>
            <p className="font-bold text-gray-900 mt-0.5">
              ₹{order.items?.reduce((s, i) => s + i.price_at_purchase * i.quantity, 0).toLocaleString()}
            </p>
          </div>
        </div>

        {/* Delivery address */}
        {order.city && (
          <div className="border-t pt-4 flex gap-2">
            <MapPin size={16} className="text-gray-400 flex-shrink-0 mt-0.5" />
            <p className="text-sm text-gray-600">
              {order.city}, {order.state} — {order.pincode}
            </p>
          </div>
        )}
      </div>

      {/* Actions */}
      <div className="flex gap-3 flex-wrap">
        <Link to="/my-orders"
          className="px-6 py-3 bg-gray-900 text-white font-bold rounded-2xl text-sm hover:bg-black transition">
          ← My Orders
        </Link>
        <Link to="/contact-us"
          className="px-6 py-3 border border-gray-200 text-gray-700 font-bold rounded-2xl text-sm hover:bg-gray-50 transition">
          Contact Support
        </Link>
      </div>
    </div>
  );
};

export default TrackOrderPage;
