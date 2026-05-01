import { useState } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import { Loader2, MessageCircle, ArrowLeft, CheckCircle } from "lucide-react";

const WhatsAppLoginPage = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const redirectTo = location.state?.redirectTo || "/";

  const [step, setStep] = useState("number"); // "number" | "otp" | "success"
  const [phone, setPhone] = useState("");
  const [otp, setOtp] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSendOTP = async () => {
    const cleaned = phone.replace(/\D/g, "");
    if (cleaned.length !== 10) {
      setError("Please enter a valid 10-digit WhatsApp number.");
      return;
    }
    setLoading(true);
    setError("");
    try {
      const res = await fetch(`${import.meta.env.VITE_API_URL}/api/auth/send-otp`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ whatsapp_number: cleaned })
      });
      const data = await res.json();
      if (!res.ok) {
        setError(data.error || "Failed to send OTP.");
        return;
      }
      setStep("otp");
    } catch {
      setError("Network error. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const handleVerifyOTP = async () => {
    if (otp.length < 4) {
      setError("Please enter the 4-digit OTP.");
      return;
    }
    setLoading(true);
    setError("");
    try {
      const res = await fetch(`${import.meta.env.VITE_API_URL}/api/auth/verify-otp`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ whatsapp_number: phone.replace(/\D/g, ""), otp })
      });
      const data = await res.json();
      if (!res.ok) {
        setError(data.error || "Invalid OTP.");
        return;
      }
      // Store auth data in localStorage
      localStorage.setItem("auth_token", data.token);
      localStorage.setItem("user_id", data.user_id);
      localStorage.setItem("whatsapp_number", data.whatsapp_number);

      setStep("success");
      setTimeout(() => navigate(redirectTo), 1200);
    } catch {
      setError("Network error. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center px-6">
      <div className="max-w-md w-full bg-white rounded-3xl shadow-xl p-10">

        {/* Header */}
        <div className="text-center mb-8">
          <div className={`w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4 transition-colors ${step === "success" ? "bg-green-100" : "bg-green-50"}`}>
            {step === "success"
              ? <CheckCircle size={36} className="text-green-500" />
              : <MessageCircle size={36} className="text-green-500" />
            }
          </div>
          <h1 className="text-2xl font-black text-gray-900 tracking-tight">
            {step === "number" && "Login with WhatsApp"}
            {step === "otp" && "Enter OTP"}
            {step === "success" && "Login Successful!"}
          </h1>
          <p className="text-gray-500 text-sm mt-2 font-medium">
            {step === "number" && "Enter your WhatsApp number to continue"}
            {step === "otp" && `OTP sent to +91 ${phone}`}
            {step === "success" && "Redirecting you..."}
          </p>
        </div>

        {/* Step 1 — Phone number */}
        {step === "number" && (
          <div className="space-y-4">
            <div className="flex gap-3">
              <div className="bg-gray-100 rounded-xl px-4 py-3 text-sm font-bold text-gray-600 flex items-center">
                +91
              </div>
              <input
                type="tel"
                maxLength={10}
                value={phone}
                onChange={(e) => { setPhone(e.target.value.replace(/\D/g, "")); setError(""); }}
                placeholder="10-digit WhatsApp number"
                className="flex-1 border border-gray-200 rounded-xl px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-green-500"
                onKeyDown={(e) => e.key === "Enter" && handleSendOTP()}
              />
            </div>

            {error && <p className="text-red-500 text-xs font-bold">{error}</p>}

            <button
              onClick={handleSendOTP}
              disabled={loading || phone.length !== 10}
              className="w-full bg-green-500 hover:bg-green-600 text-white font-black py-4 rounded-2xl flex items-center justify-center gap-3 transition disabled:opacity-60"
            >
              {loading ? <Loader2 size={20} className="animate-spin" /> : <MessageCircle size={20} />}
              {loading ? "Sending..." : "Send OTP"}
            </button>

            <p className="text-center text-xs text-gray-400 font-medium">
              You can browse products without logging in. Login is required to checkout.
            </p>
          </div>
        )}

        {/* Step 2 — OTP */}
        {step === "otp" && (
          <div className="space-y-4">
            <div className="bg-green-50 border border-green-100 rounded-xl p-3 text-center">
              <p className="text-green-700 text-xs font-bold">OTP sent to +91 {phone}</p>
              <p className="text-green-600 text-xs mt-0.5">Enter the 4-digit OTP below</p>
            </div>

            <input
              type="tel"
              maxLength={4}
              value={otp}
              onChange={(e) => { setOtp(e.target.value.replace(/\D/g, "")); setError(""); }}
              placeholder="• • • •"
              autoFocus
              className="w-full border border-gray-200 rounded-xl px-4 py-4 text-center tracking-[0.8em] text-2xl font-black focus:outline-none focus:ring-2 focus:ring-green-500"
              onKeyDown={(e) => e.key === "Enter" && handleVerifyOTP()}
            />

            {error && <p className="text-red-500 text-xs font-bold text-center">{error}</p>}

            <button
              onClick={handleVerifyOTP}
              disabled={loading || otp.length < 4}
              className="w-full bg-green-500 hover:bg-green-600 text-white font-black py-4 rounded-2xl flex items-center justify-center gap-2 transition disabled:opacity-60"
            >
              {loading && <Loader2 size={18} className="animate-spin" />}
              {loading ? "Verifying..." : "Verify & Login"}
            </button>

            <button
              onClick={() => { setStep("number"); setOtp(""); setError(""); }}
              className="w-full flex items-center justify-center gap-2 text-gray-500 text-sm font-bold hover:text-gray-700 transition"
            >
              <ArrowLeft size={16} /> Change Number
            </button>
          </div>
        )}

        {/* Step 3 — Success */}
        {step === "success" && (
          <div className="text-center space-y-3">
            <p className="text-green-600 font-black text-lg">Welcome back!</p>
            <p className="text-gray-400 text-sm">Taking you to your destination...</p>
            <Loader2 size={24} className="animate-spin text-green-500 mx-auto" />
          </div>
        )}

        {step !== "success" && (
          <div className="mt-6 text-center">
            <button
              onClick={() => navigate("/")}
              className="text-xs text-gray-400 underline underline-offset-4 hover:text-gray-600 transition"
            >
              Continue as Guest
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default WhatsAppLoginPage;
