import { useState, useEffect } from "react";
import {
  Package, ShoppingBag, Tag, Image, Plus, Trash2, Pencil,
  CheckCircle, XCircle, Loader2, ChevronDown, RefreshCw, Settings
} from "lucide-react";
import PaymentActions from "../components/admin/PaymentActions";

const API = `${import.meta.env.VITE_API_URL}/api/admin`;

/** Authenticated fetch wrapper — injects admin JWT and handles 401 */
const adminFetch = async (url, options = {}) => {
  const token = localStorage.getItem("admin_token");
  const isFormData = options.body instanceof FormData;
  const headers = {
    ...(options.headers || {}),
    Authorization: `Bearer ${token}`,
  };
  if (!isFormData && !headers["Content-Type"]) {
    headers["Content-Type"] = "application/json";
  }
  const res = await fetch(url, {
    ...options,
    headers,
  });
  if (res.status === 401 || res.status === 403) {
    localStorage.removeItem("admin_token");
    window.location.href = "/admin-login";
    return res;
  }
  return res;
};

const STATUS_OPTIONS = ["PENDING_PAYMENT", "PLACED", "PACKED", "SHIPPED", "OUT_FOR_DELIVERY", "DELIVERED", "CANCELLED"];
const PAYMENT_STATUS_OPTIONS = ["PENDING", "VERIFIED", "FAILED"];
const STATUS_COLORS = {
  PENDING_PAYMENT: "bg-yellow-100 text-yellow-700",
  PLACED: "bg-blue-100 text-blue-700",
  PACKED: "bg-indigo-100 text-indigo-700",
  SHIPPED: "bg-purple-100 text-purple-700",
  OUT_FOR_DELIVERY: "bg-blue-100 text-blue-700",
  DELIVERED: "bg-green-100 text-green-700",
  CANCELLED: "bg-red-100 text-red-700",
};
const PAYMENT_COLORS = {
  PENDING: "bg-yellow-100 text-yellow-700",
  VERIFIED: "bg-green-100 text-green-700",
  FAILED: "bg-red-100 text-red-700",
};

// ─── Reusable ────────────────────────────────────────────────────────────────
const Badge = ({ status }) => {
  const normStatus = (status || "PENDING_PAYMENT").toUpperCase();
  return (
    <span className={`text-xs font-black px-2 py-0.5 rounded-full capitalize ${STATUS_COLORS[normStatus] || "bg-gray-100 text-gray-600"}`}>
      {normStatus.replace(/_/g, " ")}
    </span>
  );
};

const PaymentBadge = ({ status }) => {
  const normStatus = (status || "PENDING").toUpperCase();
  return (
    <span className={`text-xs font-black px-2 py-0.5 rounded-full capitalize ${PAYMENT_COLORS[normStatus] || "bg-gray-100 text-gray-600"}`}>
      {normStatus}
    </span>
  );
};

const EMPTY_FORM = {
  name: "", description: "", category: "", fabric: "",
  occasion: "", pattern: "", gender: "", image_url: "", video_url: "",
  // combo fields — admin types comma-separated values
  colors: "",       // e.g. "Pink,Black,Yellow"
  sizes: "",        // e.g. "S,M,XL"
  quantity: 10,
  price_b2c: 0,
  price_b2b_ttd: 0,
  price_b2b_maharashtra: 0,
};

/** Resolve image src — handles both old external URLs and new /uploads/... paths */
const resolveImageSrc = (url) => {
  if (!url) return null;
  if (url.startsWith('http')) return url;           // old external URL
  return `${import.meta.env.VITE_API_URL}${url}`;  // local upload path
};

/** Expand colours × sizes into individual variant rows */
const buildVariants = (form) => {
  const colors = form.colors.split(",").map(c => c.trim()).filter(Boolean);
  const sizes  = form.sizes.split(",").map(s => s.trim()).filter(Boolean);
  if (!colors.length || !sizes.length) return [];
  const variants = [];
  for (const color of colors) {
    for (const size of sizes) {
      variants.push({
        color,
        size,
        quantity: Number(form.quantity) || 0,
        price_b2c: Number(form.price_b2c) || 0,
        price_b2b_ttd: Number(form.price_b2b_ttd) || 0,
        price_b2b_maharashtra: Number(form.price_b2b_maharashtra) || 0,
      });
    }
  }
  return variants;
};

// ─── Products Tab ─────────────────────────────────────────────────────────────
const ProductsTab = () => {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [editId, setEditId] = useState(null);
  const [saving, setSaving] = useState(false);
  const [form, setForm] = useState(EMPTY_FORM);
  const [imageFile, setImageFile] = useState(null);   // File object for upload
  const [imagePreview, setImagePreview] = useState(null); // data URL preview

  const load = () => {
    setLoading(true);
    adminFetch(`${API}/products`).then(r => r.json()).then(setProducts).finally(() => setLoading(false));
  };
  useEffect(load, []);

  const handleDelete = async (id) => {
    if (!confirm("Delete this product?")) return;
    const res = await adminFetch(`${API}/products/${id}`, { method: "DELETE" });
    if (!res.ok) { alert("Failed to delete product."); return; }
    load();
  };

  const handleEdit = (p) => {
    setEditId(p.id);
    setForm({
      name: p.name || "",
      description: p.description || "",
      category: p.category || "",
      fabric: p.fabric || "",
      occasion: p.occasion || "",
      pattern: p.pattern || "",
      gender: p.gender || "",
      image_url: p.image_url || "",
      video_url: p.video_url || "",
      colors: "", sizes: "", quantity: 10,
      price_b2c: 0, price_b2b_ttd: 0, price_b2b_maharashtra: 0,
    });
    setImageFile(null);
    setImagePreview(p.image_url ? resolveImageSrc(p.image_url) : null);
    setShowForm(true);
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  const handleAddNew = () => {
    setEditId(null);
    setForm(EMPTY_FORM);
    setImageFile(null);
    setImagePreview(null);
    setShowForm(true);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSaving(true);
    try {
      const url    = editId ? `${API}/products/${editId}` : `${API}/products/add`;
      const method = editId ? "PUT" : "POST";
      // Always use FormData so we can attach the image file if selected
      const fd = new FormData();

      // Append all text fields
      const textFields = ["name","description","category","fabric","occasion","pattern","gender","video_url","image_url"];
      textFields.forEach(k => fd.append(k, form[k] ?? ""));

      // Append image file if one was selected
      if (imageFile) fd.append("image", imageFile);

      // For new products, append variants as JSON string
      if (!editId) {
        fd.append("variants", JSON.stringify(buildVariants(form)));
        fd.append("images", JSON.stringify([]));
      }

      const res = await adminFetch(url, { method, body: fd });
      if (res.ok) {
        setShowForm(false);
        setEditId(null);
        setForm(EMPTY_FORM);
        setImageFile(null);
        setImagePreview(null);
        load();
      }
    } finally { setSaving(false); }
  };

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-xl font-black">Products ({products.length})</h2>
        <button onClick={handleAddNew}
          className="flex items-center gap-2 bg-pink-600 text-white px-4 py-2 rounded-xl text-sm font-bold">
          <Plus size={16} /> Add Product
        </button>
      </div>

      {showForm && (
        <form onSubmit={handleSubmit} className="border rounded-2xl p-6 mb-8 space-y-4 bg-gray-50">
          <h3 className="font-black text-lg">{editId ? `Edit Product #${editId}` : "New Product"}</h3>
          <div className="grid grid-cols-2 gap-4">
            {["name", "category", "fabric", "occasion", "pattern", "gender", "video_url"].map(field => (
              <div key={field}>
                <label className="text-xs font-black text-gray-400 uppercase tracking-widest block mb-1">{field.replace(/_/g, " ")}</label>
                <input value={form[field]} onChange={e => setForm(f => ({ ...f, [field]: e.target.value }))}
                  className="w-full border rounded-xl px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-pink-500"
                  required={field === "name"} />
              </div>
            ))}

            {/* ── Image Upload ── */}
            <div className="col-span-2">
              <label className="text-xs font-black text-gray-400 uppercase tracking-widest block mb-1">Product Image</label>
              <div className="flex items-start gap-4">
                {/* File picker */}
                <label className="flex-1 flex flex-col items-center justify-center border-2 border-dashed border-gray-200 rounded-xl p-4 cursor-pointer hover:border-pink-400 hover:bg-pink-50 transition">
                  <input
                    id="product-image-input"
                    type="file"
                    accept="image/jpeg,image/png,image/webp"
                    className="hidden"
                    onChange={e => {
                      const file = e.target.files?.[0];
                      if (!file) return;
                      setImageFile(file);
                      setImagePreview(URL.createObjectURL(file));
                    }}
                  />
                  <span className="text-xs font-bold text-gray-500 text-center">
                    {imageFile ? imageFile.name : "Click to upload JPG / PNG / WEBP"}
                  </span>
                  {!imageFile && (
                    <span className="text-[10px] text-gray-400 mt-1">Or leave blank to use URL below</span>
                  )}
                </label>

                {/* Live preview */}
                {imagePreview && (
                  <div className="relative w-24 h-24 rounded-xl overflow-hidden border flex-shrink-0">
                    <img src={imagePreview} alt="preview" className="w-full h-full object-cover" />
                    <button
                      type="button"
                      onClick={() => { setImageFile(null); setImagePreview(form.image_url ? resolveImageSrc(form.image_url) : null); }}
                      className="absolute top-1 right-1 bg-red-500 text-white rounded-full w-5 h-5 flex items-center justify-center text-xs font-black"
                    >×</button>
                  </div>
                )}
              </div>

              {/* Fallback URL input (backward compat) */}
              {!imageFile && (
                <div className="mt-2">
                  <label className="text-[10px] font-bold text-gray-400 uppercase tracking-widest block mb-1">Or paste image URL (old products)</label>
                  <input
                    value={form.image_url}
                    onChange={e => { setForm(f => ({ ...f, image_url: e.target.value })); setImagePreview(e.target.value || null); }}
                    placeholder="https://..."
                    className="w-full border rounded-xl px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-pink-500"
                  />
                </div>
              )}
            </div>
          </div>
          <div>
            <label className="text-xs font-black text-gray-400 uppercase tracking-widest block mb-1">Description</label>
            <textarea value={form.description} onChange={e => setForm(f => ({ ...f, description: e.target.value }))}
              rows={2} className="w-full border rounded-xl px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-pink-500 resize-none" />
          </div>

          {!editId && (
            <div className="space-y-4 border rounded-xl p-4 bg-white">
              <p className="text-xs font-black text-gray-400 uppercase tracking-widest">
                Variants — enter comma-separated values, all combinations will be created automatically
              </p>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="text-xs font-black text-gray-400 uppercase tracking-widest block mb-1">
                    Colours <span className="normal-case font-normal text-gray-400">(e.g. Pink, Black, Yellow)</span>
                  </label>
                  <input
                    value={form.colors}
                    onChange={e => setForm(f => ({ ...f, colors: e.target.value }))}
                    placeholder="Pink, Black, Yellow"
                    className="w-full border rounded-xl px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-pink-500"
                  />
                </div>
                <div>
                  <label className="text-xs font-black text-gray-400 uppercase tracking-widest block mb-1">
                    Sizes <span className="normal-case font-normal text-gray-400">(e.g. S, M, L, XL)</span>
                  </label>
                  <input
                    value={form.sizes}
                    onChange={e => setForm(f => ({ ...f, sizes: e.target.value }))}
                    placeholder="S, M, L, XL"
                    className="w-full border rounded-xl px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-pink-500"
                  />
                </div>
                <div>
                  <label className="text-xs font-black text-gray-400 uppercase tracking-widest block mb-1">Qty per variant</label>
                  <input type="number" value={form.quantity}
                    onChange={e => setForm(f => ({ ...f, quantity: e.target.value }))}
                    className="w-full border rounded-xl px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-pink-500" />
                </div>
                <div>
                  <label className="text-xs font-black text-gray-400 uppercase tracking-widest block mb-1">B2C Price (₹)</label>
                  <input type="number" value={form.price_b2c}
                    onChange={e => setForm(f => ({ ...f, price_b2c: e.target.value }))}
                    className="w-full border rounded-xl px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-pink-500" />
                </div>
                <div>
                  <label className="text-xs font-black text-gray-400 uppercase tracking-widest block mb-1">TTD Price (₹)</label>
                  <input type="number" value={form.price_b2b_ttd}
                    onChange={e => setForm(f => ({ ...f, price_b2b_ttd: e.target.value }))}
                    className="w-full border rounded-xl px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-pink-500" />
                </div>
                <div>
                  <label className="text-xs font-black text-gray-400 uppercase tracking-widest block mb-1">MH Price (₹)</label>
                  <input type="number" value={form.price_b2b_maharashtra}
                    onChange={e => setForm(f => ({ ...f, price_b2b_maharashtra: e.target.value }))}
                    className="w-full border rounded-xl px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-pink-500" />
                </div>
              </div>

              {/* Live preview of combinations */}
              {form.colors && form.sizes && (() => {
                const variants = buildVariants(form);
                return variants.length > 0 ? (
                  <div className="bg-gray-50 rounded-xl p-3">
                    <p className="text-xs font-black text-gray-400 mb-2">{variants.length} variants will be created:</p>
                    <div className="flex flex-wrap gap-1.5">
                      {variants.map((v, i) => (
                        <span key={i} className="text-xs bg-white border rounded-lg px-2 py-1 font-bold text-gray-700">
                          {v.color} / {v.size}
                        </span>
                      ))}
                    </div>
                  </div>
                ) : null;
              })()}
            </div>
          )}

          <div className="flex gap-3">
            <button type="submit" disabled={saving}
              className="px-6 py-2 bg-pink-600 text-white font-bold rounded-xl text-sm disabled:opacity-50 flex items-center gap-2">
              {saving && <Loader2 size={14} className="animate-spin" />}
              {editId ? "Save Changes" : "Save Product"}
            </button>
            <button type="button" onClick={() => { setShowForm(false); setEditId(null); setForm(EMPTY_FORM); }}
              className="px-6 py-2 border rounded-xl text-sm font-bold">Cancel</button>
          </div>
        </form>
      )}

      {loading ? (
        <div className="flex justify-center py-16"><Loader2 className="w-8 h-8 text-pink-600 animate-spin" /></div>
      ) : (
        <div className="overflow-x-auto">
          <table className="w-full text-sm border-collapse">
            <thead>
              <tr className="bg-gray-50 border-b">
                <th className="px-4 py-3 text-left font-black text-gray-500 text-xs uppercase">Product</th>
                <th className="px-4 py-3 text-left font-black text-gray-500 text-xs uppercase">Category</th>
                <th className="px-4 py-3 text-left font-black text-gray-500 text-xs uppercase">Variants</th>
                <th className="px-4 py-3 text-left font-black text-gray-500 text-xs uppercase">Actions</th>
              </tr>
            </thead>
            <tbody>
              {products.map(p => (
                <tr key={p.id} className="border-b hover:bg-gray-50">
                  <td className="px-4 py-3">
                    <div className="flex items-center gap-3">
                      {p.image_url && (
                        <img
                          src={resolveImageSrc(p.image_url)}
                          alt=""
                          className="w-10 h-10 rounded-lg object-cover"
                        />
                      )}
                      <div>
                        <p className="font-bold text-gray-900">{p.name}</p>
                        <p className="text-xs text-gray-400">ID: {p.id}</p>
                      </div>
                    </div>
                  </td>
                  <td className="px-4 py-3 text-gray-600">{p.category}</td>
                  <td className="px-4 py-3 text-gray-600">{p.variant_count}</td>
                  <td className="px-4 py-3">
                    <div className="flex items-center gap-3">
                      <button onClick={() => handleEdit(p)}
                        className="text-blue-500 hover:text-blue-700 flex items-center gap-1 text-xs font-bold">
                        <Pencil size={13} /> Edit
                      </button>
                      <button onClick={() => handleDelete(p.id)}
                        className="text-red-500 hover:text-red-700 flex items-center gap-1 text-xs font-bold">
                        <Trash2 size={13} /> Delete
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};

// ─── Orders Tab ───────────────────────────────────────────────────────────────
const OrdersTab = () => {
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);
  const [statusFilter, setStatusFilter] = useState("");
  const [updating, setUpdating] = useState(null);

  const load = () => {
    setLoading(true);
    const url = statusFilter ? `${API}/orders?status=${statusFilter}` : `${API}/orders`;
    adminFetch(url).then(r => r.json()).then(setOrders).finally(() => setLoading(false));
  };
  useEffect(load, [statusFilter]);

  // Save order/tracking status — updates list in-place, no full reload
  const updateStatus = async (orderId, status, paymentStatus, tracking) => {
    setUpdating(orderId);
    const res = await adminFetch(`${API}/orders/${orderId}/status`, {
      method: "PUT",
      body: JSON.stringify({ status, payment_status: paymentStatus, tracking_number: tracking || undefined })
    });
    if (res.ok) {
      setOrders(prev => prev.map(o =>
        o.id === orderId
          ? { ...o, status, payment_status: paymentStatus, tracking_number: tracking || o.tracking_number }
          : o
      ));
    }
    setUpdating(null);
  };

  // Called by PaymentActions after verify — update payment_status + order status in-place
  const handlePaymentVerified = (orderId, newPaymentStatus, newOrderStatus) => {
    setOrders(prev => prev.map(o =>
      o.id === orderId
        ? { ...o, payment_status: newPaymentStatus || 'VERIFIED', status: newOrderStatus || 'PLACED' }
        : o
    ));
  };

  // Called by PaymentActions after reject — update payment_status in-place
  const handlePaymentRejected = (orderId, newPaymentStatus) => {
    setOrders(prev => prev.map(o =>
      o.id === orderId
        ? { ...o, payment_status: newPaymentStatus || 'FAILED' }
        : o
    ));
  };

  return (
    <div>
      <div className="flex items-center justify-between mb-6 flex-wrap gap-3">
        <h2 className="text-xl font-black">Orders ({orders.length})</h2>
        <div className="flex items-center gap-3">
          <select value={statusFilter} onChange={e => setStatusFilter(e.target.value)}
            className="border rounded-xl px-3 py-2 text-sm focus:outline-none">
            <option value="">All Statuses</option>
            {STATUS_OPTIONS.map(s => <option key={s} value={s}>{s.replace(/_/g, " ")}</option>)}
          </select>
          <button onClick={load} className="p-2 border rounded-xl hover:bg-gray-50"><RefreshCw size={16} /></button>
        </div>
      </div>

      {loading ? (
        <div className="flex justify-center py-16"><Loader2 className="w-8 h-8 text-pink-600 animate-spin" /></div>
      ) : (
        <div className="space-y-4">
          {orders.map(o => (
            <OrderRow
              key={o.id}
              order={o}
              updating={updating}
              onUpdate={updateStatus}
              onPaymentVerified={handlePaymentVerified}
              onPaymentRejected={handlePaymentRejected}
            />
          ))}
          {orders.length === 0 && <p className="text-center text-gray-400 py-10">No orders found.</p>}
        </div>
      )}
    </div>
  );
};

const OrderRow = ({ order, updating, onUpdate, onPaymentVerified, onPaymentRejected }) => {
  const [open, setOpen] = useState(false);
  const [newStatus, setNewStatus] = useState((order.status || "PENDING_PAYMENT").toUpperCase());
  const [newPaymentStatus, setNewPaymentStatus] = useState((order.payment_status || "PENDING").toUpperCase());
  const [tracking, setTracking] = useState(order.tracking_number || "");

  // Keep local selects in sync when parent updates the order object
  // (e.g. after PaymentActions verify/reject)
  const currentStatus = (order.status || "PENDING_PAYMENT").toUpperCase();
  const currentPaymentStatus = (order.payment_status || "PENDING").toUpperCase();

  return (
    <div className="border rounded-2xl overflow-hidden">
      {/* ── Collapsed header ── */}
      <div className="flex items-center justify-between px-5 py-4 cursor-pointer hover:bg-gray-50" onClick={() => setOpen(!open)}>
        <div className="flex items-center gap-4 flex-wrap">
          <span className="font-black text-gray-900">#{order.id}</span>
          <span className="text-sm text-gray-600">{order.customer_name}</span>
          <span className="text-sm text-gray-400">{order.customer_phone}</span>
          {/* Badges always reflect the live order object from parent */}
          <Badge status={currentStatus} />
          <PaymentBadge status={currentPaymentStatus} />
        </div>
        <div className="flex items-center gap-4">
          <span className="font-black text-gray-900">₹{order.total_amount?.toLocaleString()}</span>
          <ChevronDown size={16} className={`text-gray-400 transition-transform ${open ? "rotate-180" : ""}`} />
        </div>
      </div>

      {/* ── Expanded detail ── */}
      {open && (
        <div className="border-t px-5 py-4 bg-gray-50 space-y-4">

          {/* Order meta */}
          <div className="grid grid-cols-2 md:grid-cols-3 gap-3 text-sm">
            <div><p className="text-xs text-gray-400 font-black uppercase">Email</p><p>{order.customer_email}</p></div>
            <div><p className="text-xs text-gray-400 font-black uppercase">Payment Method</p><p>{order.payment_method}</p></div>
            <div><p className="text-xs text-gray-400 font-black uppercase">Domain</p><p>{order.domain_origin}</p></div>
            <div><p className="text-xs text-gray-400 font-black uppercase">Date</p><p>{new Date(order.created_at).toLocaleDateString("en-IN")}</p></div>
            <div><p className="text-xs text-gray-400 font-black uppercase">Items</p><p>{order.items?.length} item(s)</p></div>
            <div><p className="text-xs text-gray-400 font-black uppercase">Total</p><p className="font-black">₹{order.total_amount?.toLocaleString()}</p></div>
          </div>

          {/* ── Payment Actions panel ── */}
          <PaymentActions
            order={order}
            onVerify={onPaymentVerified}
            onReject={onPaymentRejected}
          />

          {/* ── Manual status override ── */}
          <details className="group">
            <summary className="text-xs font-black text-gray-400 uppercase tracking-widest cursor-pointer select-none list-none flex items-center gap-1 hover:text-gray-600">
              <ChevronDown size={13} className="transition-transform group-open:rotate-180" />
              Manual Status Override
            </summary>
            <div className="mt-3 flex gap-3 flex-wrap items-end">
              <div>
                <label className="text-xs font-black text-gray-400 uppercase tracking-widest block mb-1">Order Status</label>
                <select value={newStatus} onChange={e => setNewStatus(e.target.value)}
                  className="border rounded-xl px-3 py-2 text-sm focus:outline-none">
                  {STATUS_OPTIONS.map(s => <option key={s} value={s}>{s.replace(/_/g, " ")}</option>)}
                </select>
              </div>
              <div>
                <label className="text-xs font-black text-gray-400 uppercase tracking-widest block mb-1">Payment Status</label>
                <select value={newPaymentStatus} onChange={e => setNewPaymentStatus(e.target.value)}
                  className="border rounded-xl px-3 py-2 text-sm focus:outline-none">
                  {PAYMENT_STATUS_OPTIONS.map(s => <option key={s} value={s}>{s}</option>)}
                </select>
              </div>
              <div>
                <label className="text-xs font-black text-gray-400 uppercase tracking-widest block mb-1">Tracking Number</label>
                <input value={tracking} onChange={e => setTracking(e.target.value)}
                  placeholder="e.g. DTDC123456"
                  className="border rounded-xl px-3 py-2 text-sm focus:outline-none w-48" />
              </div>
              <button
                onClick={() => onUpdate(order.id, newStatus, newPaymentStatus, tracking)}
                disabled={updating === order.id}
                className="px-5 py-2 bg-gray-900 text-white font-bold rounded-xl text-sm disabled:opacity-50 flex items-center gap-2"
              >
                {updating === order.id && <Loader2 size={13} className="animate-spin" />} Save
              </button>
            </div>
          </details>

        </div>
      )}
    </div>
  );
};

// ─── Discount Codes Tab ───────────────────────────────────────────────────────
const DiscountsTab = () => {
  const [codes, setCodes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [form, setForm] = useState({ code: "", discount_percentage: "", discount_flat: "", min_cart_value: "" });
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");

  const load = () => {
    setLoading(true);
    adminFetch(`${API}/discount-codes`).then(r => r.json()).then(setCodes).finally(() => setLoading(false));
  };
  useEffect(load, []);

  const handleCreate = async (e) => {
    e.preventDefault();
    setSaving(true); setError("");
    const res = await adminFetch(`${API}/discount-codes`, {
      method: "POST",
      body: JSON.stringify({
        code: form.code,
        discount_percentage: form.discount_percentage ? parseFloat(form.discount_percentage) : null,
        discount_flat: form.discount_flat ? parseFloat(form.discount_flat) : null,
        min_cart_value: form.min_cart_value ? parseFloat(form.min_cart_value) : 0
      })
    });
    const data = await res.json();
    if (!res.ok) { setError(data.error); setSaving(false); return; }
    setForm({ code: "", discount_percentage: "", discount_flat: "", min_cart_value: "" });
    setSaving(false);
    load();
  };

  const toggle = async (id) => {
    await adminFetch(`${API}/discount-codes/${id}`, { method: "PUT" });
    load();
  };

  const del = async (id) => {
    if (!confirm("Delete this code?")) return;
    await adminFetch(`${API}/discount-codes/${id}`, { method: "DELETE" });
    load();
  };

  return (
    <div>
      <h2 className="text-xl font-black mb-6">Discount Codes</h2>

      <form onSubmit={handleCreate} className="border rounded-2xl p-5 mb-8 bg-gray-50 space-y-4">
        <h3 className="font-black">Create New Code</h3>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {[
            { key: "code", label: "Code", placeholder: "SAVE20" },
            { key: "discount_percentage", label: "% Off", placeholder: "10" },
            { key: "discount_flat", label: "Flat ₹ Off", placeholder: "200" },
            { key: "min_cart_value", label: "Min Cart ₹", placeholder: "999" },
          ].map(({ key, label, placeholder }) => (
            <div key={key}>
              <label className="text-xs font-black text-gray-400 uppercase tracking-widest block mb-1">{label}</label>
              <input value={form[key]} onChange={e => setForm(f => ({ ...f, [key]: e.target.value }))}
                placeholder={placeholder}
                className="w-full border rounded-xl px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-pink-500"
                required={key === "code"} />
            </div>
          ))}
        </div>
        {error && <p className="text-red-500 text-sm font-bold">{error}</p>}
        <button type="submit" disabled={saving}
          className="px-6 py-2 bg-pink-600 text-white font-bold rounded-xl text-sm disabled:opacity-50 flex items-center gap-2">
          {saving && <Loader2 size={14} className="animate-spin" />} Create Code
        </button>
      </form>

      {loading ? (
        <div className="flex justify-center py-10"><Loader2 className="w-8 h-8 text-pink-600 animate-spin" /></div>
      ) : (
        <div className="overflow-x-auto">
          <table className="w-full text-sm border-collapse">
            <thead>
              <tr className="bg-gray-50 border-b">
                {["Code", "% Off", "Flat Off", "Min Cart", "Status", "Actions"].map(h => (
                  <th key={h} className="px-4 py-3 text-left font-black text-gray-500 text-xs uppercase">{h}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {codes.map(c => (
                <tr key={c.id} className="border-b hover:bg-gray-50">
                  <td className="px-4 py-3 font-black">{c.code}</td>
                  <td className="px-4 py-3">{c.discount_percentage ? `${c.discount_percentage}%` : "—"}</td>
                  <td className="px-4 py-3">{c.discount_flat ? `₹${c.discount_flat}` : "—"}</td>
                  <td className="px-4 py-3">{c.min_cart_value ? `₹${c.min_cart_value}` : "—"}</td>
                  <td className="px-4 py-3">
                    <span className={`text-xs font-black px-2 py-0.5 rounded-full ${c.is_active ? "bg-green-100 text-green-700" : "bg-gray-100 text-gray-500"}`}>
                      {c.is_active ? "Active" : "Inactive"}
                    </span>
                  </td>
                  <td className="px-4 py-3">
                    <div className="flex gap-3">
                      <button onClick={() => toggle(c.id)} className="text-xs font-bold text-blue-600 hover:text-blue-800">
                        {c.is_active ? "Disable" : "Enable"}
                      </button>
                      <button onClick={() => del(c.id)} className="text-xs font-bold text-red-500 hover:text-red-700">Delete</button>
                    </div>
                  </td>
                </tr>
              ))}
              {codes.length === 0 && (
                <tr><td colSpan={6} className="text-center py-8 text-gray-400">No discount codes yet.</td></tr>
              )}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};

// ─── Photos Moderation Tab ────────────────────────────────────────────────────
const PhotosTab = () => {
  const [photos, setPhotos] = useState([]);
  const [loading, setLoading] = useState(true);
  const [acting, setActing] = useState(null);

  const load = () => {
    setLoading(true);
    adminFetch(`${API}/photos/pending`).then(r => r.json()).then(setPhotos).finally(() => setLoading(false));
  };
  useEffect(load, []);

  const approve = async (id) => {
    setActing(id);
    await adminFetch(`${API}/photos/${id}/approve`, { method: "POST" });
    setActing(null);
    load();
  };

  const reject = async (id) => {
    setActing(id);
    await adminFetch(`${API}/photos/${id}/reject`, { method: "DELETE" });
    setActing(null);
    load();
  };

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-xl font-black">Pending Photos ({photos.length})</h2>
        <button onClick={load} className="p-2 border rounded-xl hover:bg-gray-50"><RefreshCw size={16} /></button>
      </div>

      {loading ? (
        <div className="flex justify-center py-16"><Loader2 className="w-8 h-8 text-pink-600 animate-spin" /></div>
      ) : photos.length === 0 ? (
        <div className="text-center py-16 text-gray-400">
          <Image size={48} className="mx-auto mb-3 text-gray-200" />
          <p>No photos pending approval.</p>
        </div>
      ) : (
        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-4">
          {photos.map(p => (
            <div key={p.id} className="border rounded-2xl overflow-hidden">
              <div className="aspect-square bg-gray-100">
                <img
                  src={`${import.meta.env.VITE_API_URL}${p.photo_url}`}
                  alt="User photo"
                  className="w-full h-full object-cover"
                />
              </div>
              <div className="p-3 space-y-2">
                <p className="text-xs text-gray-400">Product #{p.product_id}</p>
                <p className="text-xs text-gray-400">{new Date(p.created_at).toLocaleDateString("en-IN")}</p>
                <div className="flex gap-2">
                  <button
                    onClick={() => approve(p.id)}
                    disabled={acting === p.id}
                    className="flex-1 flex items-center justify-center gap-1 bg-green-500 text-white text-xs font-bold py-1.5 rounded-lg disabled:opacity-50"
                  >
                    {acting === p.id ? <Loader2 size={12} className="animate-spin" /> : <CheckCircle size={12} />}
                    Approve
                  </button>
                  <button
                    onClick={() => reject(p.id)}
                    disabled={acting === p.id}
                    className="flex-1 flex items-center justify-center gap-1 bg-red-500 text-white text-xs font-bold py-1.5 rounded-lg disabled:opacity-50"
                  >
                    <XCircle size={12} /> Reject
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

// ─── Settings Tab ─────────────────────────────────────────────────────────────
const SettingsTab = () => {
  const [msg, setMsg] = useState("");
  const [active, setActive] = useState(false);
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    adminFetch(`${API}/settings/popup`).then(r => r.json()).then(data => {
      setMsg(data.message || "");
      setActive(data.is_active || false);
    });
  }, []);

  const handleSave = async () => {
    setSaving(true);
    await adminFetch(`${API}/settings/popup`, {
      method: "POST",
      body: JSON.stringify({ message: msg, is_active: active })
    });
    setSaving(false);
  };

  return (
    <div>
      <h2 className="text-xl font-black mb-6">Store Settings</h2>
      <div className="border rounded-2xl p-6 bg-gray-50 max-w-lg">
        <h3 className="font-black mb-4">Welcome Popup (garba.shop)</h3>
        <div className="space-y-4">
          <div>
            <label className="text-xs font-black text-gray-400 uppercase tracking-widest block mb-1">Popup Message</label>
            <input value={msg} onChange={e => setMsg(e.target.value)} placeholder="e.g. 10% OFF with code FIRST10" className="w-full border rounded-xl px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-pink-500" />
          </div>
          <div className="flex items-center gap-2">
            <input type="checkbox" id="popupActive" checked={active} onChange={e => setActive(e.target.checked)} className="w-4 h-4 rounded border-gray-300 text-pink-600 focus:ring-pink-500" />
            <label htmlFor="popupActive" className="text-sm font-bold text-gray-700">Enable Popup</label>
          </div>
          <button onClick={handleSave} disabled={saving} className="px-6 py-2 bg-gray-900 text-white font-bold rounded-xl text-sm flex items-center gap-2">
            {saving ? "Saving..." : "Save Settings"}
          </button>
        </div>
      </div>
    </div>
  );
};

// ─── Main Dashboard ───────────────────────────────────────────────────────────
const TABS = [
  { id: "products", label: "Products", icon: Package },
  { id: "orders", label: "Orders", icon: ShoppingBag },
  { id: "discounts", label: "Discounts", icon: Tag },
  { id: "photos", label: "Photos", icon: Image },
  { id: "settings", label: "Settings", icon: Settings },
];

const AdminDashboardPage = () => {
  const [activeTab, setActiveTab] = useState("products");

  return (
    <div className="max-w-7xl mx-auto px-6 py-10">
      <h1 className="text-3xl font-black mb-8">Admin Dashboard</h1>

      {/* Tab Nav */}
      <div className="flex gap-2 border-b mb-8 overflow-x-auto">
        {TABS.map(({ id, label, icon: Icon }) => (
          <button
            key={id}
            onClick={() => setActiveTab(id)}
            className={`flex items-center gap-2 px-5 py-3 text-sm font-black whitespace-nowrap border-b-2 transition-colors ${
              activeTab === id
                ? "border-pink-600 text-pink-600"
                : "border-transparent text-gray-400 hover:text-gray-700"
            }`}
          >
            <Icon size={16} /> {label}
          </button>
        ))}
      </div>

      {/* Tab Content */}
      {activeTab === "products" && <ProductsTab />}
      {activeTab === "orders" && <OrdersTab />}
      {activeTab === "discounts" && <DiscountsTab />}
      {activeTab === "photos" && <PhotosTab />}
      {activeTab === "settings" && <SettingsTab />}
    </div>
  );
};

export default AdminDashboardPage;
