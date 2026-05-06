import { useState } from 'react'
import { CheckCircle, Upload, Loader2, Copy, Check } from 'lucide-react'
import qrImage from '../assets/payment-qr.jpg'

const API = import.meta.env.VITE_API_URL || 'http://localhost:5000'

/**
 * PaymentInstructions
 *
 * Props:
 *   orderId         — order ID to submit proof against
 *   totalAmount     — amount to display
 *   alreadyUploaded — true if order.payment_proof is already set (from DB)
 *   onPaymentMarked — optional callback after successful submission
 *   paymentMethod   — 'UPI' or 'COD' (only shows for UPI)
 */
export default function PaymentInstructions({
  orderId,
  totalAmount,
  alreadyUploaded = false,
  onPaymentMarked,
  paymentMethod = 'UPI'
}) {
  const [submitted, setSubmitted] = useState(alreadyUploaded)
  const [uploading, setUploading]  = useState(false)
  const [screenshot, setScreenshot] = useState(null)
  const [preview, setPreview] = useState(null)
  const [message, setMessage]      = useState('')
  const [isError, setIsError]      = useState(false)
  const [copied, setCopied] = useState(false)

  const upiId = "MSMNMFASHION.eazypay@icici"

  // Show this entire UI ONLY when payment method = "UPI"
  if (paymentMethod !== 'UPI' && paymentMethod !== 'Manual UPI') return null;

  const handleCopy = () => {
    navigator.clipboard.writeText(upiId)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setScreenshot(file);
      setPreview(URL.createObjectURL(file));
    }
  };

  const handleMarkPaid = async () => {
    if (!screenshot) {
      setIsError(true);
      setMessage('Required.');
      return;
    }

    setUploading(true)
    setMessage('')
    setIsError(false)
    try {
      const formData = new FormData()
      formData.append('payment_proof', screenshot)

      const res = await fetch(`${API}/api/orders/${orderId}/mark-paid`, {
        method: 'POST',
        body: formData,
      })
      const data = await res.json()
      if (res.ok) {
        setSubmitted(true)
        setMessage(data.message)
        if (onPaymentMarked) onPaymentMarked()
      } else {
        setIsError(true)
        setMessage(data.error || 'Failed.')
        if (data.error && data.error.toLowerCase().includes('already')) {
          setSubmitted(true)
        }
      }
    } catch {
      setIsError(true)
      setMessage('Error.')
    }
    setUploading(false)
  }

  if (submitted) {
    return (
      <div className="mt-3 bg-green-50 border border-green-100 rounded-xl p-3 text-center shadow-sm max-w-[420px] mx-auto">
        <CheckCircle size={24} className="text-green-600 mx-auto mb-1.5" />
        <h3 className="font-black text-green-900 text-xs mb-0.5">Proof Submitted</h3>
        <p className="text-green-700 text-[9px]">Status updates after verification.</p>
      </div>
    )
  }

  return (
    <div className="mt-3 bg-white border border-gray-100 rounded-2xl p-3 md:p-4 shadow-xl shadow-gray-200/50 max-w-[420px] mx-auto">
      {/* Header */}
      <div className="text-center mb-3">
        <h3 className="text-sm font-black text-gray-900 uppercase tracking-tight">Complete Payment</h3>
        <p className="text-gray-400 text-[8px] font-bold uppercase mt-0.5 tracking-widest">Scan QR or pay via UPI</p>
      </div>

      {/* Middle: QR + Details */}
      <div className="flex flex-col md:flex-row items-center md:items-stretch gap-2 mb-3">
        {/* QR Code */}
        <div className="flex-shrink-0">
          <div className="p-1 bg-white border border-gray-100 rounded-lg shadow-sm">
            <img 
              src={qrImage} 
              alt="Scan" 
              className="w-[110px] h-[110px] md:w-[120px] md:h-[120px] object-contain rounded-md"
            />
          </div>
        </div>

        {/* Details Box */}
        <div className="flex-1 w-full flex flex-col justify-between py-0.5">
          <div className="bg-gray-50 rounded-lg p-2.5 space-y-2 text-left">
            <div>
              <p className="text-[8px] font-black text-gray-400 uppercase tracking-widest mb-0.5">UPI ID</p>
              <div className="flex items-center justify-between gap-1">
                <p className="text-[10px] font-bold text-gray-900 break-all leading-none">{upiId}</p>
                <button 
                  onClick={handleCopy}
                  className="p-1 hover:bg-white rounded-md transition-colors text-gray-400 hover:text-pink-600"
                >
                  {copied ? <Check size={10} className="text-green-600" /> : <Copy size={10} />}
                </button>
              </div>
            </div>
            <div className="flex justify-between items-end">
              <div>
                <p className="text-[8px] font-black text-gray-400 uppercase tracking-widest mb-0.5">UPI Name</p>
                <p className="text-[10px] font-bold text-gray-900 leading-none">M&M Fashion</p>
              </div>
              <span className="px-2 py-0.5 bg-pink-600 text-white text-[10px] font-black rounded-md">
                ₹{Number(totalAmount).toLocaleString()}
              </span>
            </div>
          </div>
          <p className="text-[8px] text-gray-400 font-bold text-center md:text-left uppercase tracking-tighter">
            GPay · PhonePe · Paytm · UPI
          </p>
        </div>
      </div>

      {/* Upload */}
      <div className="space-y-1.5 mb-3">
        <div className="flex items-center justify-between px-1">
            <p className="text-[8px] font-black text-gray-400 uppercase tracking-widest">Payment Proof</p>
            {screenshot && <p className="text-[8px] text-green-600 font-black tracking-widest">✓ UPLOADED</p>}
        </div>
        
        <label className="relative group cursor-pointer block w-full h-[80px] border-2 border-dashed border-gray-100 rounded-lg hover:border-pink-300 hover:bg-pink-50/30 transition-all overflow-hidden bg-gray-50">
          {preview ? (
            <div className="w-full h-full relative">
              <img src={preview} alt="Preview" className="w-full h-full object-contain" />
              <div className="absolute inset-0 bg-black/40 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity">
                <span className="bg-white text-gray-900 px-2 py-1 rounded-full text-[8px] font-black uppercase">Change</span>
              </div>
            </div>
          ) : (
            <div className="flex flex-col items-center justify-center h-full gap-1">
              <Upload size={14} className="text-gray-300 group-hover:text-pink-500" />
              <p className="text-[8px] font-black text-gray-400 uppercase tracking-widest">Tap to upload</p>
            </div>
          )}
          <input type="file" accept="image/*" className="hidden" onChange={handleFileChange} />
        </label>
      </div>

      {message && (
        <p className={`text-[8px] font-black mb-2 text-center uppercase tracking-widest ${isError ? 'text-red-500' : 'text-green-500'}`}>
          {message}
        </p>
      )}

      {/* Button */}
      <button
        onClick={handleMarkPaid}
        disabled={uploading}
        className="w-full h-9 flex items-center justify-center gap-2 bg-gray-900 hover:bg-black disabled:bg-gray-200 text-white font-black rounded-lg transition-all shadow-md shadow-gray-200 active:scale-[0.98] text-[10px] uppercase tracking-[0.15em]"
      >
        {uploading ? <Loader2 size={12} className="animate-spin" /> : 'I have paid'}
      </button>

      <div className="flex items-center justify-center mt-3 border-t pt-2 border-gray-50">
        <span className="text-[7px] text-gray-300 font-black uppercase tracking-[0.3em]">🔐 Verified Secure Checkout</span>
      </div>
    </div>
  )
}

