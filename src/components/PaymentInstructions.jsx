import { useState } from 'react'
import { CheckCircle, Upload, CreditCard, Loader2 } from 'lucide-react'

const API = import.meta.env.VITE_API_URL || 'http://localhost:5000'

/**
 * PaymentInstructions
 *
 * Props:
 *   orderId         — order ID to submit proof against
 *   totalAmount     — amount to display
 *   alreadyUploaded — true if order.payment_proof is already set (from DB)
 *   onPaymentMarked — optional callback after successful submission
 */
export default function PaymentInstructions({
  orderId,
  totalAmount,
  alreadyUploaded = false,
  onPaymentMarked,
}) {
  // If proof already exists in DB, start in the "submitted" state
  const [submitted, setSubmitted] = useState(alreadyUploaded)
  const [uploading, setUploading]  = useState(false)
  const [screenshot, setScreenshot] = useState(null)
  const [message, setMessage]      = useState('')
  const [isError, setIsError]      = useState(false)

  const handleMarkPaid = async () => {
    setUploading(true)
    setMessage('')
    setIsError(false)
    try {
      const formData = new FormData()
      if (screenshot) formData.append('payment_proof', screenshot)

      const res = await fetch(`${API}/api/orders/${orderId}/mark-paid`, {
        method: 'POST',
        body: formData,
      })
      const data = await res.json()
      if (res.ok) {
        setSubmitted(true)   // lock the UI immediately
        setMessage(data.message)
        if (onPaymentMarked) onPaymentMarked()
      } else {
        setIsError(true)
        setMessage(data.error || 'Something went wrong. Please try again.')
        // If backend says already submitted, lock the UI too
        if (data.error && data.error.toLowerCase().includes('already')) {
          setSubmitted(true)
        }
      }
    } catch {
      setIsError(true)
      setMessage('Network error. Please try again.')
    }
    setUploading(false)
  }

  // ── Already submitted state (on load OR after upload) ─────────────────────
  if (submitted) {
    return (
      <div className="mt-6 bg-green-50 border border-green-200 rounded-2xl p-5 text-center">
        <div className="flex justify-center mb-3">
          <CheckCircle size={40} className="text-green-500" />
        </div>
        <h3 className="font-black text-green-700 text-base mb-1">
          Payment Proof Already Submitted
        </h3>
        <p className="text-green-600 text-sm">
          Our team will verify your payment shortly. Your order will be confirmed once verified.
        </p>
      </div>
    )
  }

  // ── Upload form ───────────────────────────────────────────────────────────
  return (
    <div className="mt-6 bg-amber-50 border border-amber-200 rounded-2xl p-5">
      {/* Header */}
      <div className="flex items-center gap-2 mb-4">
        <CreditCard size={20} className="text-amber-600" />
        <h3 className="font-black text-amber-800 text-base">Complete Your UPI Payment</h3>
      </div>

      {/* UPI Details */}
      <div className="bg-white border border-amber-200 rounded-xl p-4 mb-4">
        <p className="text-xs font-bold text-amber-700 uppercase tracking-wider mb-2">Pay via UPI</p>
        <p className="text-2xl font-black text-amber-600 tracking-wide mb-1">mmfashion@upi</p>
        <p className="text-sm text-amber-700 font-medium">UPI Name: M&amp;M Fashion</p>
        {totalAmount && (
          <p className="text-sm font-black text-gray-900 mt-2">
            Amount: <span className="text-amber-600">₹{Number(totalAmount).toLocaleString()}</span>
          </p>
        )}
        <p className="text-xs text-amber-600 mt-2">
          GPay · PhonePe · Paytm · Any UPI app
        </p>
      </div>

      {/* Upload Screenshot */}
      <div className="mb-4">
        <label className="block text-xs font-bold text-amber-800 uppercase tracking-wider mb-2">
          Upload Payment Screenshot{' '}
          <span className="text-amber-500 font-normal normal-case">(optional but recommended)</span>
        </label>
        <label className="flex items-center gap-2 cursor-pointer border-2 border-dashed border-amber-300 rounded-xl px-4 py-3 hover:border-amber-500 transition-colors bg-white">
          <Upload size={16} className="text-amber-500 shrink-0" />
          <span className="text-sm text-amber-700 truncate">
            {screenshot ? screenshot.name : 'Click to upload screenshot'}
          </span>
          <input
            type="file"
            accept="image/*"
            className="hidden"
            onChange={e => setScreenshot(e.target.files[0] || null)}
          />
        </label>
        {screenshot && (
          <p className="mt-1 text-xs text-green-600 font-bold">✓ {screenshot.name} selected</p>
        )}
      </div>

      {/* Error message */}
      {message && (
        <p className={`text-xs font-bold mb-3 ${isError ? 'text-red-600' : 'text-green-600'}`}>
          {message}
        </p>
      )}

      {/* Submit Button */}
      <button
        onClick={handleMarkPaid}
        disabled={uploading}
        className="w-full flex items-center justify-center gap-2 bg-amber-500 hover:bg-amber-600 disabled:bg-amber-300 text-white font-black py-3 rounded-xl transition-all text-sm"
      >
        {uploading ? (
          <>
            <Loader2 size={16} className="animate-spin" />
            Submitting...
          </>
        ) : (
          '✓ I Have Paid'
        )}
      </button>

      <p className="text-center text-xs text-amber-600 mt-3">
        Your order will be confirmed after admin verifies the payment.
      </p>
    </div>
  )
}
