import { useState, useContext } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import { MessageCircle, Loader2, Mail, Phone } from "lucide-react";
import { WishlistContext } from "../context/WishlistContext";
import { CartContext } from "../context/CartContext";

const LoginPage = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const redirectTo = location.state?.redirectTo || "/";
  const { loadWishlistForUser } = useContext(WishlistContext);
  const { loadCart } = useContext(CartContext);

  const [step, setStep] = useState("details"); // "details" | "otp" | "success"
  const [phoneNumber, setPhoneNumber] = useState("");
  const [email, setEmail] = useState("");
  const [otp, setOtp] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSendOTP = async () => {
    // Validate Phone number
    const cleanedPhone = phoneNumber.replace(/\D/g, "");
    if (cleanedPhone.length !== 10) {
      setError("Please enter a valid 10-digit phone number.");
      return;
    }

    // Validate email
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!email || !emailRegex.test(email)) {
      setError("Please enter a valid email address.");
      return;
    }

    setLoading(true);
    setError("");
    
    try {
      const res = await fetch(`${import.meta.env.VITE_API_URL}/api/auth/send-otp`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ 
          phone_number: cleanedPhone, 
          email: email.toLowerCase().trim() 
        })
      });
      
      const data = await res.json();
      console.log("[LOGIN] send-otp response:", data);
      if (!res.ok) {
        setError(data.error || "Failed to send OTP.");
        return;
      }
      
      setStep("otp");
    } catch (err) {
      console.error("[LOGIN] send-otp network error:", err);
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
        body: JSON.stringify({ 
          email: email.toLowerCase().trim(), 
          otp: otp 
        })
      });
      
      const data = await res.json();
      console.log("[LOGIN] verify-otp response:", data);
      if (!res.ok) {
        setError(data.error || "Invalid OTP.");
        return;
      }

      // Store authentication data
      localStorage.setItem("auth_token", data.token);
      localStorage.setItem("user_id", data.user_id);
      localStorage.setItem("phone_number", data.phone_number);
      localStorage.setItem("whatsapp_number", data.phone_number); // Legacy fallback
      localStorage.setItem("email", data.email);

      // ── Merge guest cart into DB cart ─────────────────────────────────────
      // Read guest cart from localStorage before loadCart() clears it
      const guestCartRaw = localStorage.getItem("guest_cart");
      if (guestCartRaw) {
        try {
          const guestItems = JSON.parse(guestCartRaw);
          const validGuest = guestItems.filter(i => i.activeVariant?.id && i.cartQuantity >= 1);
          if (validGuest.length > 0) {
            // Push each guest item to the DB cart (backend deduplicates)
            await Promise.allSettled(
              validGuest.map(item =>
                fetch(`${import.meta.env.VITE_API_URL}/api/cart/add`, {
                  method: "POST",
                  headers: { "Content-Type": "application/json" },
                  body: JSON.stringify({
                    phone_number: data.phone_number,
                    variant_id: item.activeVariant.id,
                    quantity: item.cartQuantity || 1,
                  }),
                })
              )
            );
          }
        } catch {
          // silent — guest cart merge failure must never block login
        }
        // Clear guest cart now that it's been merged
        localStorage.removeItem("guest_cart");
      }

      // Load this user's wishlist and cart (now includes merged guest items)
      loadWishlistForUser();
      loadCart();

      setStep("success");
      setTimeout(() => navigate(redirectTo), 1500);
    } catch {
      setError("Network error. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 via-white to-pink-50 flex items-center justify-center p-6">
      <div className="bg-white rounded-3xl shadow-2xl p-8 w-full max-w-md border border-gray-100">
        
        {/* Header */}
        <div className="text-center mb-8">
          <div className="w-16 h-16 bg-gradient-to-r from-blue-500 to-indigo-500 rounded-2xl flex items-center justify-center mx-auto mb-4">
            {step === "details" && <Mail size={28} className="text-white" />}
            {step === "otp" && <MessageCircle size={28} className="text-white" />}
            {step === "success" && <div className="text-white text-2xl">✓</div>}
          </div>
          <h1 className="text-2xl font-black text-gray-900 tracking-tight">
            {step === "details" && "Login with Phone"}
            {step === "otp" && "Enter OTP"}
            {step === "success" && "Login Successful!"}
          </h1>
          <p className="text-gray-500 text-sm mt-2 font-medium">
            {step === "details" && "Enter your details to receive OTP via email"}
            {step === "otp" && `OTP sent to your email`}
            {step === "success" && "Redirecting you..."}
          </p>
        </div>

        {/* Error Message */}
        {error && (
          <div className="bg-red-50 border border-red-100 text-red-600 text-sm font-bold p-3 rounded-xl mb-4">
            {error}
          </div>
        )}

        {/* Step 1 — Details Input */}
        {step === "details" && (
          <div className="space-y-4">
            {/* Phone Number */}
            <div>
              <label className="text-xs font-bold text-gray-500 uppercase tracking-wider flex items-center gap-2 mb-2">
                <Phone size={14} />
                Mobile Number
              </label>
              <div className="flex gap-2">
                <div className="bg-gray-100 border border-gray-200 rounded-xl px-3 py-3 text-sm font-bold text-gray-600">
                  +91
                </div>
                <input
                  type="tel"
                  maxLength={10}
                  value={phoneNumber}
                  onChange={(e) => { 
                    setPhoneNumber(e.target.value.replace(/\D/g, "")); 
                    setError(""); 
                  }}
                  placeholder="10-digit phone number"
                  className="flex-1 border border-gray-200 rounded-xl px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                  onKeyDown={(e) => e.key === "Enter" && handleSendOTP()}
                />
              </div>
            </div>

            {/* Email */}
            <div>
              <label className="text-xs font-bold text-gray-500 uppercase tracking-wider flex items-center gap-2 mb-2">
                <Mail size={14} />
                Email Address
              </label>
              <input
                type="email"
                value={email}
                onChange={(e) => { 
                  setEmail(e.target.value); 
                  setError(""); 
                }}
                placeholder="your.email@example.com"
                className="w-full border border-gray-200 rounded-xl px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                onKeyDown={(e) => e.key === "Enter" && handleSendOTP()}
              />
              <p className="text-xs text-gray-400 mt-1 font-medium">
                📧 OTP will be sent to this email address
              </p>
            </div>

            <button
              onClick={handleSendOTP}
              disabled={loading || phoneNumber.length !== 10 || !email}
              className="w-full bg-blue-600 hover:bg-blue-700 text-white font-black py-4 rounded-2xl flex items-center justify-center gap-3 transition disabled:opacity-60"
            >
              {loading ? <Loader2 size={20} className="animate-spin" /> : <Phone size={20} />}
              {loading ? "Sending..." : "Request Login OTP"}
            </button>

            <div className="text-center">
              <p className="text-xs text-gray-400 font-medium">
                🔐 We'll send a 4-digit OTP to your email
              </p>
            </div>
          </div>
        )}

        {/* Step 2 — OTP */}
        {step === "otp" && (
          <div className="space-y-4">
            <div className="bg-green-50 border border-green-100 rounded-xl p-3 text-center">
              <p className="text-green-700 text-xs font-bold">📧 OTP sent to {email}</p>
              <p className="text-green-600 text-xs mt-0.5">Check your email and enter the 4-digit OTP below</p>
              <p className="text-green-500 text-xs mt-1">💡 Test OTP: 1234 (always works)</p>
            </div>

            <input
              type="tel"
              maxLength={4}
              value={otp}
              onChange={(e) => { 
                setOtp(e.target.value.replace(/\D/g, "")); 
                setError(""); 
              }}
              placeholder="• • • •"
              autoFocus
              className="w-full border border-gray-200 rounded-xl px-4 py-4 text-center tracking-[0.8em] text-2xl font-black focus:outline-none focus:ring-2 focus:ring-green-500"
              onKeyDown={(e) => e.key === "Enter" && handleVerifyOTP()}
            />

            <button
              onClick={handleVerifyOTP}
              disabled={loading || otp.length < 4}
              className="w-full bg-green-500 hover:bg-green-600 text-white font-black py-4 rounded-2xl flex items-center justify-center gap-2 transition disabled:opacity-60"
            >
              {loading ? <Loader2 size={20} className="animate-spin" /> : null}
              {loading ? "Verifying..." : "Verify OTP"}
            </button>

            <button
              onClick={() => { 
                setStep("details"); 
                setOtp(""); 
                setError(""); 
              }}
              className="w-full flex items-center justify-center gap-2 text-gray-500 text-sm font-bold hover:text-gray-700 transition"
            >
              ← Back to details
            </button>
          </div>
        )}

        {/* Step 3 — Success */}
        {step === "success" && (
          <div className="text-center space-y-4">
            <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto">
              <div className="text-green-600 text-2xl">✓</div>
            </div>
            <p className="text-gray-600 font-medium">
              Welcome! Redirecting you now...
            </p>
            <div className="flex justify-center">
              <Loader2 size={20} className="animate-spin text-green-500" />
            </div>
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

export default LoginPage;