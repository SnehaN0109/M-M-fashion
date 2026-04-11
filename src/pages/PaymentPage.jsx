import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

/* Payment methods constants */
const PAYMENT_METHODS = {
  UPI: "upi",
  CARD: "card",
  COD: "cod",
};

/* UPI Apps with icons and links (dummy links for simulation) */
const UPI_APPS = [
  { id: "phonepe", name: "PhonePe", link: "https://www.phonepe.com/" },
  { id: "gpay", name: "Google Pay", link: "https://pay.google.com/" },
  { id: "paytm", name: "Paytm", link: "https://paytm.com/" },
];

/* Gift Card Modal */
function GiftCardModal({ open, onClose, onAdd }) {
  const [voucher, setVoucher] = useState("");
  const [pin, setPin] = useState("");

  if (!open) return null;

  return (
    <div
      onClick={(e) => e.target === e.currentTarget && onClose()}
      className="fixed inset-0 bg-black/50 flex items-end justify-center z-50"
    >
      <div className="bg-white w-full max-w-lg rounded-t-2xl p-6 mx-4">
        <h3 className="text-lg font-bold mb-2">Add New Gift Card</h3>
        <p className="text-sm text-gray-500 mb-4">
          Up to 15 gift cards can be added per transaction
        </p>
        <input
          type="text"
          placeholder="Enter voucher number"
          value={voucher}
          onChange={(e) => setVoucher(e.target.value)}
          className="w-full mb-3 p-2 border rounded"
        />
        <input
          type="password"
          placeholder="Enter voucher PIN"
          value={pin}
          onChange={(e) => setPin(e.target.value)}
          className="w-full mb-4 p-2 border rounded"
        />
        <button
          onClick={() => {
            onAdd({ voucher, pin });
            setVoucher("");
            setPin("");
          }}
          className="w-full bg-blue-600 text-white py-2 rounded font-bold"
        >
          Add Gift Card
        </button>
      </div>
    </div>
  );
}

export default function PaymentPage() {
  const navigate = useNavigate();
  const [openSection, setOpenSection] = useState(PAYMENT_METHODS.UPI);
  const [order, setOrder] = useState(null);

  /* Card State */
  const [cardNumber, setCardNumber] = useState("");
  const [cardName, setCardName] = useState("");
  const [expiry, setExpiry] = useState("");
  const [cvv, setCvv] = useState("");

  /* UPI State */
  const [selectedUPI, setSelectedUPI] = useState("phonepe");

  /* Gift Card Modal */
  const [giftCardOpen, setGiftCardOpen] = useState(false);

  /* Payment Confirmation Popup */
  const [confirmOpen, setConfirmOpen] = useState(false);
  const [paymentMethodUsed, setPaymentMethodUsed] = useState("");

  /* Load pending order */
  useEffect(() => {
    const pending = JSON.parse(localStorage.getItem("pendingOrder"));
    if (!pending) navigate("/");
    else setOrder(pending);
  }, [navigate]);

  if (!order) return null;
  const totalAmount = order.totalAmount;

  /* Open confirmation popup after payment method selected */
  const handlePayment = (method) => {
    setPaymentMethodUsed(method);
    setConfirmOpen(true);
  };

  /* Confirm or cancel order */
  const handleOrderConfirm = (confirm) => {
    setConfirmOpen(false);
    if (confirm) {
      const existingOrders = JSON.parse(localStorage.getItem("orders")) || [];
      const updatedOrders = [
        ...existingOrders,
        { ...order, paymentMethod: paymentMethodUsed },
      ];
      localStorage.setItem("orders", JSON.stringify(updatedOrders));
      localStorage.removeItem("pendingOrder");

      // Simulate WhatsApp message sending
      const msg = `Order of ₹${totalAmount} confirmed via ${paymentMethodUsed}.`;
      window.open(`https://wa.me/?text=${encodeURIComponent(msg)}`, "_blank");

      navigate("/order-success");
    } else {
      alert("Order cancelled!");
    }
  };

  const toggleSection = (section) => {
    setOpenSection(openSection === section ? null : section);
  };

  return (
    <div className="bg-gray-100 min-h-screen pb-20 flex flex-col items-center">

      {/* Header */}
      <div className="bg-blue-600 text-white p-4 w-full max-w-lg flex justify-between items-center shadow">
        <div>
          <p className="text-xs opacity-80">Step 3 of 3</p>
          <h1 className="text-lg font-bold">Payments</h1>
        </div>
        <div className="text-xs bg-white/20 px-3 py-1 rounded">🔒 100% Secure</div>
      </div>

      {/* Total Amount */}
      <div className="bg-white m-4 p-4 rounded shadow flex justify-between items-center w-full max-w-lg">
        <span className="font-semibold text-blue-600">Total Amount</span>
        <span className="text-xl font-bold text-blue-600">₹{totalAmount}</span>
      </div>

      {/* Payment Options */}
      <div className="bg-white rounded shadow overflow-hidden w-full max-w-lg">

        {/* UPI */}
        <div
          onClick={() => toggleSection(PAYMENT_METHODS.UPI)}
          className={`p-4 border-b cursor-pointer flex justify-between items-center ${openSection === PAYMENT_METHODS.UPI ? "bg-gray-50" : ""}`}
        >
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 flex items-center justify-center border rounded bg-gray-100">
              <img
                src="https://upload.wikimedia.org/wikipedia/commons/6/65/UPI_India_Logo.svg"
                alt="UPI"
                className="w-6 h-6 object-contain"
              />
            </div>
            <div>
              <h2 className="font-semibold">UPI</h2>
              <p className="text-sm text-gray-500">Pay using any UPI app</p>
            </div>
          </div>
          <span>{openSection === PAYMENT_METHODS.UPI ? "▲" : "▼"}</span>
        </div>
        {openSection === PAYMENT_METHODS.UPI && (
          <div className="p-4 space-y-3 bg-gray-50">
            {UPI_APPS.map((app) => (
              <button
                key={app.id}
                onClick={() => window.open(app.link, "_blank")}
                className="w-full border p-3 rounded hover:bg-gray-100 font-medium text-left"
              >
                Pay via {app.name}
              </button>
            ))}
            <button
              onClick={() => handlePayment(`UPI - ${selectedUPI}`)}
              className="w-full bg-orange-500 text-white py-3 rounded font-bold mt-2"
            >
              Pay ₹{totalAmount}
            </button>
          </div>
        )}

        {/* Card */}
        <div
          onClick={() => toggleSection(PAYMENT_METHODS.CARD)}
          className={`p-4 border-t border-b cursor-pointer flex justify-between items-center ${openSection === PAYMENT_METHODS.CARD ? "bg-gray-50" : ""}`}
        >
          <div className="flex items-center gap-3">
            <span className="w-10 h-10 flex items-center justify-center border rounded bg-gray-100">💳</span>
            <div>
              <h2 className="font-semibold">Credit / Debit / ATM Card</h2>
              <p className="text-sm text-gray-500">Secure card payment</p>
            </div>
          </div>
          <span>{openSection === PAYMENT_METHODS.CARD ? "▲" : "▼"}</span>
        </div>
        {openSection === PAYMENT_METHODS.CARD && (
          <div className="p-4 space-y-3 bg-gray-50">
            <input type="text" placeholder="Card Number" value={cardNumber} onChange={(e) => setCardNumber(e.target.value)} className="w-full p-2 border rounded" />
            <input type="text" placeholder="Name on Card" value={cardName} onChange={(e) => setCardName(e.target.value)} className="w-full p-2 border rounded" />
            <div className="flex gap-2">
              <input type="text" placeholder="MM/YY" value={expiry} onChange={(e) => setExpiry(e.target.value)} className="w-1/2 p-2 border rounded" />
              <input type="password" placeholder="CVV" value={cvv} onChange={(e) => setCvv(e.target.value)} className="w-1/2 p-2 border rounded" />
            </div>
            <button onClick={() => handlePayment("Card")} className="w-full bg-orange-500 text-white py-3 rounded font-bold">
              Pay ₹{totalAmount}
            </button>
          </div>
        )}

        {/* COD */}
        <div
          onClick={() => toggleSection(PAYMENT_METHODS.COD)}
          className={`p-4 border-t cursor-pointer flex justify-between items-center ${openSection === PAYMENT_METHODS.COD ? "bg-gray-50" : ""}`}
        >
          <div className="flex items-center gap-3">
            <span className="w-10 h-10 flex items-center justify-center border rounded bg-gray-100">💵</span>
            <div>
              <h2 className="font-semibold">Cash on Delivery</h2>
            </div>
          </div>
          <span>{openSection === PAYMENT_METHODS.COD ? "▲" : "▼"}</span>
        </div>
        {openSection === PAYMENT_METHODS.COD && (
          <div className="p-4 bg-gray-50">
            <button onClick={() => handlePayment("Cash on Delivery")} className="w-full bg-orange-500 text-white py-3 rounded font-bold">
              Place Order ₹{totalAmount}
            </button>
          </div>
        )}

        {/* Gift Card */}
        <div
          onClick={() => setGiftCardOpen(true)}
          className="p-4 border-t cursor-pointer flex justify-between items-center"
        >
          <span className="w-10 h-10 flex items-center justify-center border rounded bg-gray-100">🎁</span>
          <span>Have a Gift Card?</span>
          <span className="text-blue-600 font-bold">Add</span>
        </div>
      </div>

      {/* Footer */}
      <div className="text-center text-gray-400 text-sm mt-10">
        35 Crore happy customers and counting! 🙂
      </div>

      {/* Gift Card Modal */}
      <GiftCardModal
        open={giftCardOpen}
        onClose={() => setGiftCardOpen(false)}
        onAdd={(data) => {
          console.log("Gift Card Added:", data);
          setGiftCardOpen(false);
        }}
      />

      {/* Payment Confirmation Popup */}
      {confirmOpen && (
        <div className="fixed bottom-0 left-0 w-full bg-white shadow-lg p-4 flex justify-between items-center z-50 border-t">
          <span className="font-medium">Confirm your order of ₹{totalAmount}?</span>
          <div className="flex gap-2">
            <button onClick={() => handleOrderConfirm(true)} className="bg-green-600 text-white py-1 px-3 rounded">Confirm</button>
            <button onClick={() => handleOrderConfirm(false)} className="bg-red-600 text-white py-1 px-3 rounded">Cancel</button>
          </div>
        </div>
      )}
    </div>
  );
}