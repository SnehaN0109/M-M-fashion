// src/pages/WhatsAppLoginPage.jsx
const WhatsAppLoginPage = () => {
  return (
    <div className="max-w-md mx-auto px-6 py-16">
      <h1 className="text-3xl font-bold mb-6">Login via WhatsApp</h1>
      <input
        type="text"
        placeholder="Enter your WhatsApp number"
        className="border p-3 w-full mb-4"
      />
      <button className="w-full bg-pink-600 text-white py-3 rounded">
        Send OTP
      </button>
    </div>
  );
};

export default WhatsAppLoginPage;
