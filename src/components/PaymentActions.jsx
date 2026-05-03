import { useState } from "react";
import { CheckCircle, XCircle, Image, Loader2, ExternalLink } from "lucide-react";

const API_BASE = import.meta.env.VITE_API_URL || "http://localhost:5001";

// ─── Payment status badge ──────────────────────────────────────────────────
const PaymentBadge = ({ status }) => {
  const s = (status || "PENDING").toUpperCase();
  const styles = {
    PENDING: "bg-amber-100 text-amber-700 border border-amber-200",
    VERIFIED: "bg-green-100 text-green-700 border border-green-200",
    FAILED: "bg-red-100 text-red-700 border border-red-200",
  };
  const labels = { PENDING: "⏳ Pending", VERIFIED: "✅ Verified", FAILED: "❌ Rejected" };
  return (
    <span className={`text-xs font-black px-2.5 py-1 rounded-full ${styles[s] || styles.PENDING}`}>
      {labels[s] || s}
    </span>
  );
};

// ─── Main PaymentActions component ────────────────────────────────────────
const PaymentActions = ({ order, adminToken, onStatusChange }) => {
  const [loading, setLoading] = useState(null); // 'verify' | 'reject' | 'proof'
  const [proofUrl, setProofUrl] = useState(null);
  const [proofError, setProofError] = useState("");
  const [actionError, setActionError] = useState("");
  const [currentPaymentStatus, setCurrentPaymentStatus] = useState(
    order.payment_status || "PENDING"
  );

  const paymentMethod = order.payment_method || "COD";
  const isUPI = paymentMethod === "UPI";
  const isPending = currentPaymentStatus === "PENDING";

  const authHeaders = {
    Authorization: `Bearer ${adminToken}`,
    "Content-Type": "application/json",
  };

  const handleAction = async (action) => {
    setLoading(action);
    setActionError("");
    try {
      const res = await fetch(
        `${API_BASE}/api/payment/admin/orders/${order.id}/payment-action`,
        {
          method: "POST",
          headers: authHeaders,
          body: JSON.stringify({ action }),
        }
      );
      const data = await res.json();
      if (!res.ok) {
        setActionError(data.error || "Action failed.");
        return;
      }
      setCurrentPaymentStatus(data.payment_status);
      if (onStatusChange) onStatusChange(order.id, data.payment_status, data.order_status);
    } catch {
      setActionError("Network error.");
    } finally {
      setLoading(null);
    }
  };

  const handleViewProof = async () => {
    if (proofUrl) {
      // Toggle off
      setProofUrl(null);
      return;
    }
    setLoading("proof");
    setProofError("");
    try {
      const res = await fetch(
        `${API_BASE}/api/payment/admin/payment-proof/${order.id}`,
        { headers: { Authorization: `Bearer ${adminToken}` } }
      );
      const data = await res.json();
      if (!res.ok) {
        setProofError(data.error || "Could not load proof.");
        return;
      }
      if (!data.proof_url) {
        setProofError("No screenshot uploaded by customer.");
        return;
      }
      setProofUrl(`${API_BASE}${data.proof_url}`);
    } catch {
      setProofError("Network error loading proof.");
    } finally {
      setLoading(null);
    }
  };

  return (
    <div className="mt-3 pt-3 border-t border-gray-100">
      {/* Payment method + status row */}
      <div className="flex items-center gap-2 mb-2 flex-wrap">
        <span className="text-xs font-black text-gray-400 uppercase tracking-wider">Payment:</span>
        <span className="text-xs font-bold text-gray-700">{paymentMethod}</span>
        <PaymentBadge status={currentPaymentStatus} />
      </div>

      {/* Action buttons — only show for UPI orders with PENDING status */}
      {isUPI && isPending && (
        <div className="flex gap-2 flex-wrap mb-2">
          {/* Verify */}
          <button
            onClick={() => handleAction("verify")}
            disabled={!!loading}
            className="flex items-center gap-1.5 bg-green-500 hover:bg-green-600 text-white font-black text-xs px-3 py-1.5 rounded-xl transition-all active:scale-95 disabled:opacity-50"
          >
            {loading === "verify" ? (
              <Loader2 size={13} className="animate-spin" />
            ) : (
              <CheckCircle size={13} />
            )}
            Verify Payment
          </button>

          {/* Reject */}
          <button
            onClick={() => handleAction("reject")}
            disabled={!!loading}
            className="flex items-center gap-1.5 bg-red-500 hover:bg-red-600 text-white font-black text-xs px-3 py-1.5 rounded-xl transition-all active:scale-95 disabled:opacity-50"
          >
            {loading === "reject" ? (
              <Loader2 size={13} className="animate-spin" />
            ) : (
              <XCircle size={13} />
            )}
            Reject Payment
          </button>

          {/* View Screenshot */}
          <button
            onClick={handleViewProof}
            disabled={!!loading}
            className="flex items-center gap-1.5 bg-blue-500 hover:bg-blue-600 text-white font-black text-xs px-3 py-1.5 rounded-xl transition-all active:scale-95 disabled:opacity-50"
          >
            {loading === "proof" ? (
              <Loader2 size={13} className="animate-spin" />
            ) : (
              <Image size={13} />
            )}
            {proofUrl ? "Hide Screenshot" : "View Screenshot"}
          </button>
        </div>
      )}

      {/* Also allow viewing screenshot for non-pending UPI orders */}
      {isUPI && !isPending && (
        <button
          onClick={handleViewProof}
          disabled={!!loading}
          className="flex items-center gap-1.5 bg-blue-100 hover:bg-blue-200 text-blue-700 font-black text-xs px-3 py-1.5 rounded-xl transition-all active:scale-95 disabled:opacity-50 mb-2"
        >
          {loading === "proof" ? (
            <Loader2 size={13} className="animate-spin" />
          ) : (
            <Image size={13} />
          )}
          {proofUrl ? "Hide Screenshot" : "View Screenshot"}
        </button>
      )}

      {/* Error messages */}
      {actionError && (
        <p className="text-xs text-red-600 font-bold mb-2">{actionError}</p>
      )}
      {proofError && (
        <p className="text-xs text-blue-600 font-bold mb-2">{proofError}</p>
      )}

      {/* Inline proof image */}
      {proofUrl && (
        <div className="mt-2 border border-blue-200 rounded-2xl overflow-hidden bg-blue-50 p-2">
          <div className="flex items-center justify-between mb-1">
            <span className="text-xs font-black text-blue-600 uppercase tracking-wide">
              Payment Screenshot
            </span>
            <a
              href={proofUrl}
              target="_blank"
              rel="noreferrer"
              className="text-xs text-blue-500 hover:text-blue-700 flex items-center gap-1"
            >
              Open <ExternalLink size={11} />
            </a>
          </div>
          <img
            src={proofUrl}
            alt="Payment proof"
            className="w-full max-h-48 object-contain rounded-xl"
            onError={() => setProofError("Could not load image.")}
          />
        </div>
      )}
    </div>
  );
};

export default PaymentActions;
