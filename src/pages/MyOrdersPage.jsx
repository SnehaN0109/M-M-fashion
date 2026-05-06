import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { Package, Loader2, ShoppingBag, ChevronRight, Calendar, CreditCard, MapPin, Phone, Mail } from "lucide-react";

const STATUS_COLORS = {
  pending_payment: "bg-yellow-100 text-yellow-700",
  confirmed: "bg-blue-100 text-blue-700",
  packed: "bg-indigo-100 text-indigo-700",
  shipped: "bg-purple-100 text-purple-700",
  delivered: "bg-green-100 text-green-700",
  cancelled: "bg-red-100 text-red-700",
};

const MyOrdersPage = () => {
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [expandedOrder, setExpandedOrder] = useState(null);

  // Get whatsapp number from localStorage (set during WhatsApp login)
  const whatsapp = localStorage.getItem("whatsapp_number");

  useEffect(() => {
    if (!whatsapp) { setLoading(false); return; }
    
    // Fetch orders with full details
    fetch(`${import.meta.env.VITE_API_URL}/api/orders/my-orders?whatsapp_number=${encodeURIComponent(whatsapp)}`, {
      headers: {
        'Cache-Control': 'no-cache, no-store, must-revalidate',
        'Pragma': 'no-cache',
        'Expires': '0'
      }
    })
      .then((r) => r.json())
      .then(async (data) => {
        if (Array.isArray(data)) {
          // Fetch full details for each order
          const ordersWithDetails = await Promise.all(
            data.map(async (order) => {
              try {
                const detailRes = await fetch(`${import.meta.env.VITE_API_URL}/api/orders/track/${order.order_id}`, {
                  headers: {
                    'Cache-Control': 'no-cache, no-store, must-revalidate',
                    'Pragma': 'no-cache',
                    'Expires': '0'
                  }
                });
                const detailData = await detailRes.json();
                return detailData;
              } catch {
                return order; // Fallback to basic data if detail fetch fails
              }
            })
          );
          setOrders(ordersWithDetails);
        } else {
          setError(data.error || "Failed to load orders.");
        }
      })
      .catch(() => setError("Could not connect to server."))
      .finally(() => setLoading(false));
  }, [phoneNumber]);

  if (loading) return (
    <div className="min-h-screen flex items-center justify-center">
      <Loader2 className="w-10 h-10 text-pink-600 animate-spin" />
    </div>
  );

  if (!phoneNumber) return (
    <div className="min-h-screen flex flex-col items-center justify-center gap-6 px-6">
      <Package size={56} className="text-gray-200" />
      <p className="text-xl font-black text-gray-500 text-center">Login with Phone to view your orders</p>
      <Link to="/login" className="px-8 py-3 bg-blue-600 text-white font-bold rounded-2xl">
        Login with Phone
      </Link>
    </div>
  );

  if (error) return (
    <div className="min-h-screen flex flex-col items-center justify-center gap-4 px-6">
      <p className="text-red-500 font-bold">{error}</p>
      <button onClick={() => window.location.reload()} className="px-6 py-2 bg-gray-900 text-white rounded-xl text-sm">
        Retry
      </button>
    </div>
  );

  if (orders.length === 0) return (
    <div className="min-h-screen flex flex-col items-center justify-center gap-6 px-6">
      <ShoppingBag size={56} className="text-gray-200" />
      <p className="text-xl font-black text-gray-400">No orders yet</p>
      <Link to="/products" className="px-8 py-3 bg-pink-600 text-white font-bold rounded-2xl">
        Start Shopping
      </Link>
    </div>
  );

  return (
    <div className="max-w-5xl mx-auto px-6 py-10">
      <div className="flex items-center gap-3 mb-8">
        <Package size={32} className="text-pink-600" />
        <h1 className="text-3xl font-black">My Orders</h1>
      </div>

      <div className="space-y-6">
        {orders.map((order) => {
          const isExpanded = expandedOrder === order.order_id;
          
          return (
            <div key={order.order_id} className="border rounded-2xl shadow-sm overflow-hidden bg-white">
              {/* Order Header */}
              <div className="p-5 bg-gray-50 border-b">
                <div className="flex items-start justify-between gap-4 flex-wrap">
                  <div className="flex-1">
                    <div className="flex items-center gap-3 mb-2">
                      <p className="font-black text-gray-900 text-lg">Order #{order.order_id}</p>
                      <span className={`text-xs font-black px-3 py-1 rounded-full capitalize ${STATUS_COLORS[order.status] || "bg-gray-100 text-gray-600"}`}>
                        {order.status.replace(/_/g, " ")}
                      </span>
                    </div>
                    
                    <div className="flex flex-wrap gap-4 text-sm text-gray-600">
                      <div className="flex items-center gap-1.5">
                        <Calendar size={14} />
                        <span>
                          {new Date(order.created_at).toLocaleDateString("en-IN", {
                            day: "numeric", month: "short", year: "numeric", hour: "2-digit", minute: "2-digit"
                          })}
                        </span>
                      </div>
                      <div className="flex items-center gap-1.5">
                        <CreditCard size={14} />
                        <span>{order.payment_method}</span>
                      </div>
                      {order.tracking_number ? (
                        <div className="flex items-center gap-1.5 text-blue-600 font-bold">
                          <Package size={14} />
                          <span>Tracking: {order.tracking_number}</span>
                        </div>
                      ) : (
                        <div className="flex items-center gap-1.5 text-gray-400">
                          <Package size={14} />
                          <span>Tracking: {(order.payment_status || '').toUpperCase() === 'PENDING' ? 'Awaiting payment...' : 'Processing...'}</span>
                        </div>
                      )}
                    </div>
                  </div>
                  
                  <div className="text-right">
                    <p className="text-2xl font-black text-gray-900">₹{order.total_amount?.toLocaleString()}</p>
                    <p className="text-xs text-gray-500">{order.items?.length || 0} item{(order.items?.length || 0) > 1 ? "s" : ""}</p>
                  </div>
                </div>
              </div>

              {/* Order Items */}
              <div className="p-5">
                <h3 className="font-black text-sm text-gray-700 mb-3 uppercase tracking-wider">Order Items</h3>
                <div className="space-y-3">
                  {order.items?.map((item, idx) => (
                    <div key={idx} className="flex gap-4 items-center p-3 bg-gray-50 rounded-xl">
                      <img
                        src={item.image_url || "https://via.placeholder.com/80"}
                        className="w-20 h-20 rounded-lg object-cover border border-gray-200"
                        alt={item.product_name}
                      />
                      <div className="flex-1 min-w-0">
                        <p className="font-bold text-gray-900 mb-1">{item.product_name}</p>
                        <div className="flex flex-wrap gap-3 text-xs text-gray-500">
                          <span className="bg-white px-2 py-1 rounded border">Color: {item.color}</span>
                          <span className="bg-white px-2 py-1 rounded border">Size: {item.size}</span>
                          <span className="bg-white px-2 py-1 rounded border">Qty: {item.quantity}</span>
                        </div>
                      </div>
                      <div className="text-right">
                        <p className="font-black text-gray-900">₹{(item.price_at_purchase * item.quantity).toLocaleString()}</p>
                        <p className="text-xs text-gray-500">₹{item.price_at_purchase} each</p>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Expandable Details */}
              {isExpanded && (
                <div className="px-5 pb-5 space-y-4 border-t pt-4">
                  {/* Price Breakdown */}
                  <div className="bg-gray-50 rounded-xl p-4">
                    <h3 className="font-black text-sm text-gray-700 mb-3 uppercase tracking-wider">Price Details</h3>
                    <div className="space-y-2 text-sm">
                      <div className="flex justify-between text-gray-600">
                        <span>Subtotal</span>
                        <span>₹{order.subtotal?.toLocaleString()}</span>
                      </div>
                      {order.discount_amount > 0 && (
                        <div className="flex justify-between text-green-600 font-bold">
                          <span>Discount {order.discount_code && `(${order.discount_code})`}</span>
                          <span>−₹{order.discount_amount?.toLocaleString()}</span>
                        </div>
                      )}
                      <div className="flex justify-between text-gray-600">
                        <span>Shipping</span>
                        <span>{order.shipping_charge === 0 ? "Free" : `₹${order.shipping_charge}`}</span>
                      </div>
                      <div className="flex justify-between font-black text-lg text-gray-900 border-t pt-2 mt-2">
                        <span>Total</span>
                        <span>₹{order.total_amount?.toLocaleString()}</span>
                      </div>
                    </div>
                  </div>

                  {/* Shipping Address */}
                  <div className="bg-gray-50 rounded-xl p-4">
                    <h3 className="font-black text-sm text-gray-700 mb-3 uppercase tracking-wider flex items-center gap-2">
                      <MapPin size={14} /> Shipping Address
                    </h3>
                    <div className="text-sm text-gray-700 space-y-1">
                      <p className="font-bold">{order.customer_name}</p>
                      <p>{order.address?.line1}</p>
                      {order.address?.line2 && <p>{order.address.line2}</p>}
                      <p>{order.address?.city}, {order.address?.state} - {order.address?.pincode}</p>
                    </div>
                  </div>

                  {/* Contact Info */}
                  <div className="bg-gray-50 rounded-xl p-4">
                    <h3 className="font-black text-sm text-gray-700 mb-3 uppercase tracking-wider">Contact Details</h3>
                    <div className="space-y-2 text-sm text-gray-700">
                      <div className="flex items-center gap-2">
                        <Phone size={14} className="text-gray-400" />
                        <span>{order.customer_phone}</span>
                      </div>
                      <div className="flex items-center gap-2">
                        <Mail size={14} className="text-gray-400" />
                        <span>{order.customer_email}</span>
                      </div>
                    </div>
                  </div>
                </div>
              )}

              {/* Action Buttons */}
              <div className="px-5 pb-5 flex gap-3 flex-wrap">
                <button
                  onClick={() => setExpandedOrder(isExpanded ? null : order.order_id)}
                  className="flex items-center gap-1 text-xs font-black text-gray-600 border border-gray-300 px-4 py-2 rounded-xl hover:bg-gray-50 transition"
                >
                  {isExpanded ? "Hide Details" : "View Full Details"}
                  <ChevronRight size={13} className={`transition-transform ${isExpanded ? "rotate-90" : ""}`} />
                </button>
                
                <Link
                  to={`/trackorder/${order.order_id}`}
                  className="flex items-center gap-1 text-xs font-black text-pink-600 border border-pink-200 px-4 py-2 rounded-xl hover:bg-pink-50 transition"
                >
                  Track Order <ChevronRight size={13} />
                </Link>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default MyOrdersPage;
