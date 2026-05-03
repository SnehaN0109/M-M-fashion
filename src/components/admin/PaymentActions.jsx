import { useState } from 'react'
import { CheckCircle, XCircle, ImageIcon, Loader2, ExternalLink } from 'lucide-react'

const API = import.meta.env.VITE_API_URL || 'http://localhost:5000'

const BADGE = {
  PENDING:  'bg-yellow-100 text-yellow-700 border-yellow-200',
  VERIFIED: 'bg-green-100  text-green-700  border-green-200',
  FAILED:   'bg-red-100    text-red-700    border-red-200',
}

/**
 * PaymentActions — shown inside each OrderRow in the admin dashboard.
 *
 * Props:
 *   order        — order object (.id, .payment_status, .payment_proof, .payment_method)
 *   onVerify(id) — called after successful verify
 *   onReject(id) — called after successful reject
 *
 * All orders use UPI. Shows status badge, verify/reject buttons,
 * and "View Screenshot" only when payment_proof exists.
 */
export default function PaymentActions({ order, onVerify, onReject }) {
  const [status, setStatus] = useState((order.payment_status || 'PENDING').toUpperCase())
  const [acting, setActing]           = useState(null)   // 'verify' | 'reject' | null
  const [feedback, setFeedback]       = useState(null)   // { ok: bool, msg: string }
  const [proofOpen, setProofOpen]     = useState(false)
  const [proofUrl, setProofUrl]       = useState(null)
  const [proofLoading, setProofLoading] = useState(false)

  const token  = localStorage.getItem('admin_token')
  // All orders use UPI — screenshot button shown only when a real image was uploaded
  // "submitted" is a sentinel value meaning paid without file — no image to show
  const hasProof = !!order.payment_proof && order.payment_proof !== 'submitted'

  // ── Payment action (verify / reject) ─────────────────────────────────────
  const handleAction = async (action) => {
    setActing(action)
    setFeedback(null)
    try {
      const res = await fetch(`${API}/api/admin/orders/${order.id}/payment-action`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify({ action }),
      })
      const data = await res.json()
      if (res.ok) {
        const newStatus = data.payment_status?.toUpperCase() || (action === 'verify' ? 'VERIFIED' : 'FAILED')
        setStatus(newStatus)
        setFeedback({
          ok: true,
          msg: action === 'verify'
            ? 'Payment verified — order moved to PLACED.'
            : 'Payment rejected.',
        })
        if (action === 'verify' && onVerify) onVerify(order.id, data.payment_status, data.status)
        if (action === 'reject' && onReject) onReject(order.id, data.payment_status)
      } else {
        setFeedback({ ok: false, msg: data.error || 'Action failed. Try again.' })
      }
    } catch {
      setFeedback({ ok: false, msg: 'Network error. Check your connection.' })
    } finally {
      setActing(null)
    }
  }

  // ── Load payment proof screenshot ─────────────────────────────────────────
  const handleViewProof = async () => {
    // Toggle if already loaded
    if (proofUrl) { setProofOpen(v => !v); return }

    setProofLoading(true)
    setFeedback(null)
    try {
      const res = await fetch(`${API}/api/admin/payment-proof/${order.id}`, {
        headers: { 'Authorization': `Bearer ${token}` },
      })
      const data = await res.json()
      if (res.ok && data.payment_proof) {
        setProofUrl(`${API}${data.payment_proof}`)
        setProofOpen(true)
      } else {
        setFeedback({ ok: false, msg: 'Screenshot not found on server.' })
      }
    } catch {
      setFeedback({ ok: false, msg: 'Could not load screenshot.' })
    } finally {
      setProofLoading(false)
    }
  }

  // ── UPI orders ────────────────────────────────────────────────────────────
  return (
    <div className="rounded-xl border border-gray-200 bg-white p-4 space-y-3">

      {/* Header: status badge + method + screenshot button (UPI + proof exists only) */}
      <div className="flex items-center justify-between flex-wrap gap-2">
        <div className="flex items-center gap-2">
          <span className="text-xs font-black text-gray-400 uppercase tracking-wider">UPI Payment</span>
          <span className={`text-xs font-black px-2.5 py-0.5 rounded-full border ${BADGE[status] || BADGE.PENDING}`}>
            {status}
          </span>
        </div>

        {/* View Screenshot — ONLY when payment_proof exists */}
        {hasProof && (
          <button
            onClick={handleViewProof}
            disabled={proofLoading}
            className="flex items-center gap-1.5 text-xs font-bold text-blue-600 hover:text-blue-800 border border-blue-200 hover:border-blue-400 rounded-lg px-3 py-1.5 transition-colors disabled:opacity-50"
          >
            {proofLoading
              ? <Loader2 size={13} className="animate-spin" />
              : <ImageIcon size={13} />
            }
            {proofOpen ? 'Hide Screenshot' : 'View Screenshot'}
          </button>
        )}

        {/* No proof uploaded yet */}
        {!hasProof && status === 'PENDING' && (
          <span className="text-xs text-gray-400 italic">No screenshot uploaded yet</span>
        )}
      </div>

      {/* Feedback message */}
      {feedback && (
        <p className={`text-xs font-bold px-3 py-2 rounded-lg ${
          feedback.ok
            ? 'bg-green-50 text-green-700 border border-green-200'
            : 'bg-red-50 text-red-600 border border-red-200'
        }`}>
          {feedback.ok ? '✓ ' : '✗ '}{feedback.msg}
        </p>
      )}

      {/* Verify / Reject buttons — UPI + not yet verified */}
      {status !== 'VERIFIED' && (
        <div className="flex gap-2 flex-wrap">
          <button
            onClick={() => handleAction('verify')}
            disabled={!!acting}
            className="flex items-center gap-1.5 bg-green-600 hover:bg-green-700 disabled:bg-green-300 text-white text-xs font-black px-4 py-2 rounded-lg transition-colors"
          >
            {acting === 'verify'
              ? <Loader2 size={13} className="animate-spin" />
              : <CheckCircle size={13} />
            }
            Verify Payment
          </button>

          {status === 'PENDING' && (
            <button
              onClick={() => handleAction('reject')}
              disabled={!!acting}
              className="flex items-center gap-1.5 bg-red-600 hover:bg-red-700 disabled:bg-red-300 text-white text-xs font-black px-4 py-2 rounded-lg transition-colors"
            >
              {acting === 'reject'
                ? <Loader2 size={13} className="animate-spin" />
                : <XCircle size={13} />
              }
              Reject Payment
            </button>
          )}
        </div>
      )}

      {/* Verified state */}
      {status === 'VERIFIED' && (
        <div className="flex items-center gap-2 text-green-700 text-xs font-bold">
          <CheckCircle size={14} className="text-green-600" />
          Payment verified — order is confirmed.
        </div>
      )}

      {/* Screenshot preview */}
      {proofOpen && proofUrl && (
        <div className="space-y-2">
          <div className="rounded-xl overflow-hidden border border-gray-200 bg-gray-50">
            <img
              src={proofUrl}
              alt="Payment screenshot"
              className="w-full max-h-72 object-contain"
            />
          </div>
          <a
            href={proofUrl}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-1 text-xs text-blue-600 hover:underline font-bold"
          >
            <ExternalLink size={12} /> Open full image
          </a>
        </div>
      )}
    </div>
  )
}
