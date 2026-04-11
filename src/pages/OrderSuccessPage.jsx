import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

const OrderSuccessPage = () => {
  const navigate = useNavigate();
  const [order, setOrder] = useState(null);

  useEffect(() => {
    const storedOrder = JSON.parse(localStorage.getItem("lastOrder"));

    if (!storedOrder) {
      navigate("/");
    } else {
      setOrder(storedOrder);
    }
  }, [navigate]);

  if (!order) return null;

  // Estimated Delivery (5 days from now)
  const deliveryDate = new Date();
  deliveryDate.setDate(deliveryDate.getDate() + 5);

  const handleDownloadInvoice = () => {
    const invoiceContent = `
      ORDER INVOICE
      --------------------------
      Order ID: ${order.orderId}
      Date: ${order.date}

      Product: ${order.name}
      Size: ${order.size}
      Color: ${order.color}
      Quantity: ${order.quantity}
      Total Paid: ₹${order.price * order.quantity}

      Thank you for shopping with us!
    `;

    const blob = new Blob([invoiceContent], { type: "text/plain" });
    const url = window.URL.createObjectURL(blob);

    const a = document.createElement("a");
    a.href = url;
    a.download = "Invoice.txt";
    a.click();

    window.URL.revokeObjectURL(url);
  };

  return (
    <div className="max-w-4xl mx-auto px-6 py-16 text-center">

      <div className="bg-white shadow-lg rounded-lg p-10">

        <h1 className="text-4xl font-bold text-green-600 mb-4">
          🎉 Order Placed Successfully!
        </h1>

        <p className="text-lg mb-6">
          Thank you for your purchase. Your order has been confirmed.
        </p>

        <div className="bg-gray-100 p-6 rounded-lg text-left inline-block">

          <p className="mb-2">
            <strong>Order ID:</strong> {order.orderId}
          </p>

          <p className="mb-2">
            <strong>Order Date:</strong> {order.date}
          </p>

          <p className="mb-2">
            <strong>Estimated Delivery:</strong>{" "}
            {deliveryDate.toLocaleDateString()}
          </p>

          <p className="mb-2">
            <strong>Total Paid:</strong> ₹
            {order.price * order.quantity}
          </p>
        </div>

        <div className="mt-8 flex flex-col md:flex-row justify-center gap-4">

          <button
            onClick={() => navigate("/")}
            className="bg-black text-white px-6 py-3 rounded"
          >
            🏠 Continue Shopping
          </button>

          <button
            className="bg-blue-600 text-white px-6 py-3 rounded"
          >
            🚚 Track Order
          </button>

          <button
            onClick={handleDownloadInvoice}
            className="bg-green-600 text-white px-6 py-3 rounded"
          >
            📄 Download Invoice
          </button>

        </div>

        <p className="text-sm text-gray-500 mt-6">
          🔐 Safe & Secure Payment | 7 Days Easy Return Policy
        </p>

      </div>
    </div>
  );
};

export default OrderSuccessPage;