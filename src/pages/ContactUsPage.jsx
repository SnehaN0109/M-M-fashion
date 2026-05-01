import { useState } from "react";
import { useDomain } from "../context/DomainContext";
import { Mail, Phone, Clock, MessageCircle, CheckCircle, Loader2 } from "lucide-react";

const ContactUsPage = () => {
  const { brandName, supportEmail, supportPhone } = useDomain();

  const [form, setForm] = useState({
    name: "", email: "", whatsapp: "", order_id: "", subject: "", message: "",
  });
  const [loading, setLoading] = useState(false);
  const [sent, setSent] = useState(false);

  const handleChange = (e) => setForm((f) => ({ ...f, [e.target.name]: e.target.value }));

  const handleSubmit = (e) => {
    e.preventDefault();
    setLoading(true);
    // Simulate submission — replace with real API if needed
    setTimeout(() => { setLoading(false); setSent(true); }, 1200);
  };

  return (
    <div className="bg-white text-gray-800">

      {/* Hero */}
      <div className="bg-gradient-to-br from-pink-50 to-rose-100 py-16 text-center px-6">
        <h1 className="text-4xl font-black text-gray-900 mb-3">Contact Us</h1>
        <p className="text-gray-600 max-w-xl mx-auto">
          Have a question or need help with your order? We're here for you.
        </p>
      </div>

      {/* Contact cards */}
      <div className="max-w-5xl mx-auto px-6 py-14 grid sm:grid-cols-3 gap-6">
        {[
          { icon: Mail, title: "Email Support", value: supportEmail, sub: "Reply within 24 hours" },
          { icon: Phone, title: "WhatsApp Support", value: supportPhone, sub: "Quick responses on WhatsApp" },
          { icon: Clock, title: "Working Hours", value: "Mon – Sat", sub: "10:00 AM – 7:00 PM IST" },
        ].map(({ icon: Icon, title, value, sub }) => (
          <div key={title} className="border rounded-2xl p-6 text-center space-y-2 hover:shadow-md transition">
            <div className="w-12 h-12 bg-pink-50 rounded-2xl flex items-center justify-center mx-auto">
              <Icon size={20} className="text-pink-600" />
            </div>
            <h3 className="font-black text-gray-900">{title}</h3>
            <p className="text-sm font-bold text-gray-700">{value}</p>
            <p className="text-xs text-gray-400">{sub}</p>
          </div>
        ))}
      </div>

      {/* Form */}
      <div className="max-w-2xl mx-auto px-6 pb-20">
        <h2 className="text-2xl font-black text-gray-900 mb-8 text-center">Send Us a Message</h2>

        {sent ? (
          <div className="text-center space-y-4 py-10">
            <CheckCircle size={56} className="text-green-500 mx-auto" />
            <p className="text-xl font-black text-gray-900">Message Sent!</p>
            <p className="text-gray-500 text-sm">We'll get back to you within 24 hours.</p>
            <button onClick={() => setSent(false)} className="text-pink-600 text-sm font-bold underline">
              Send another message
            </button>
          </div>
        ) : (
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="grid sm:grid-cols-2 gap-4">
              {[
                { name: "name", placeholder: "Full Name", type: "text", required: true },
                { name: "email", placeholder: "Email Address", type: "email", required: false },
                { name: "whatsapp", placeholder: "WhatsApp Number", type: "tel", required: true },
                { name: "order_id", placeholder: "Order ID (optional)", type: "text", required: false },
              ].map(({ name, placeholder, type, required }) => (
                <div key={name}>
                  <input
                    name={name}
                    type={type}
                    placeholder={placeholder}
                    value={form[name]}
                    onChange={handleChange}
                    required={required}
                    className="w-full border border-gray-200 rounded-2xl px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-pink-400"
                  />
                </div>
              ))}
            </div>

            <select
              name="subject"
              value={form.subject}
              onChange={handleChange}
              required
              className="w-full border border-gray-200 rounded-2xl px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-pink-400 text-gray-600"
            >
              <option value="">Select Subject</option>
              {["Order Issue", "Return / Refund", "Size Inquiry", "Payment Issue", "General Question"].map((s) => (
                <option key={s} value={s}>{s}</option>
              ))}
            </select>

            <textarea
              name="message"
              rows={4}
              placeholder="Describe your issue or question..."
              value={form.message}
              onChange={handleChange}
              required
              className="w-full border border-gray-200 rounded-2xl px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-pink-400 resize-none"
            />

            <button
              type="submit"
              disabled={loading}
              className="w-full bg-pink-600 hover:bg-pink-700 text-white font-black py-4 rounded-2xl flex items-center justify-center gap-2 disabled:opacity-50 transition-all"
            >
              {loading ? <Loader2 size={18} className="animate-spin" /> : <MessageCircle size={18} />}
              {loading ? "Sending..." : "Send Message"}
            </button>
          </form>
        )}
      </div>

      {/* WhatsApp floating button */}
      <a
        href={`https://wa.me/${supportPhone?.replace(/\D/g, "")}?text=Hello%20I%20need%20help`}
        target="_blank"
        rel="noopener noreferrer"
        className="fixed bottom-6 right-6 bg-green-500 hover:bg-green-600 text-white px-5 py-3 rounded-full shadow-xl flex items-center gap-2 font-bold text-sm transition z-50"
      >
        <MessageCircle size={18} /> WhatsApp
      </a>
    </div>
  );
};

export default ContactUsPage;
