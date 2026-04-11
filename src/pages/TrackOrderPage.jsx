import { useParams } from "react-router-dom";

const TrackOrderPage = () => {
  const { orderId } = useParams();

  // Sample Order Data (Later connect to backend)
  const order = {
    id: orderId || "OD123456789012345000",
    product: {
      name: "Premium Cotton Kurti",
      image: "https://via.placeholder.com/100",
      quantity: 1,
      seller: "Saraswati Fashion Hub",
    },
    status: "Shipped", // Change to test
    address: {
      name: "Saraswati Jadhav",
      details: "Flat No 12, ABC Apartments, Nagpur, Maharashtra - 440001",
      mobile: "9876543210",
    },
    payment: {
      method: "UPI",
      status: "Paid",
      total: 4599,
    },
    estimatedDelivery: "Tomorrow",
    courier: {
      partner: "Ekart Logistics",
      trackingNumber: "EK123456789IN",
    },
  };

  const statusSteps = [
    "Order Confirmed",
    "Packed",
    "Shipped",
    "Out for Delivery",
    "Delivered",
  ];

  const currentStep = statusSteps.indexOf(order.status);

  return (
    <div className="max-w-5xl mx-auto px-6 py-10">

      {/* 1️⃣ Order ID */}
      <div className="mb-8">
        <h1 className="text-2xl font-bold mb-2">Order Details</h1>
        <p className="text-gray-600">
          <span className="font-semibold">Order ID:</span> {order.id}
        </p>
        <p className="text-sm text-gray-500">
          Used for customer support and reference
        </p>
      </div>

      {/* 2️⃣ Product Details */}
      <div className="border rounded-lg p-5 mb-6 flex gap-5">
        <img
          src={order.product.image}
          alt="product"
          className="w-24 h-24 object-cover rounded"
        />
        <div>
          <h2 className="font-semibold text-lg">{order.product.name}</h2>
          <p>Quantity: {order.product.quantity}</p>
          <p className="text-sm text-gray-600">
            Seller: {order.product.seller}
          </p>
        </div>
      </div>

      {/* 3️⃣ Order Status Timeline */}
      <div className="mb-8">
        <h2 className="font-semibold text-lg mb-4">Order Status</h2>

        <div className="flex justify-between items-center">
          {statusSteps.map((step, index) => (
            <div key={step} className="flex-1 text-center">
              <div
                className={`w-8 h-8 mx-auto rounded-full flex items-center justify-center text-white
                ${index <= currentStep ? "bg-green-500" : "bg-gray-300"}`}
              >
                ✓
              </div>
              <p className="text-xs mt-2">{step}</p>
            </div>
          ))}
        </div>
      </div>

      {/* 4️⃣ Delivery Address */}
      <div className="border rounded-lg p-5 mb-6">
        <h2 className="font-semibold mb-2">Delivery Address</h2>
        <p>{order.address.name}</p>
        <p className="text-sm text-gray-600">{order.address.details}</p>
        <p className="text-sm">Mobile: {order.address.mobile}</p>
      </div>

      {/* 5️⃣ Payment Info */}
      <div className="border rounded-lg p-5 mb-6">
        <h2 className="font-semibold mb-2">Payment Information</h2>
        <p>Method: {order.payment.method}</p>
        <p>Status: {order.payment.status}</p>
        <p>Total: ₹{order.payment.total}</p>
      </div>

      {/* 6️⃣ Estimated Delivery */}
      <div className="border rounded-lg p-5 mb-6">
        <h2 className="font-semibold mb-2">Estimated Delivery</h2>
        <p className="text-green-600 font-medium">
          Arriving {order.estimatedDelivery}
        </p>
      </div>

      {/* 7️⃣ Courier Details */}
      <div className="border rounded-lg p-5 mb-6">
        <h2 className="font-semibold mb-2">Courier Details</h2>
        <p>Partner: {order.courier.partner}</p>
        <p>Tracking No: {order.courier.trackingNumber}</p>
      </div>

      {/* 8️⃣ Options */}
      <div className="flex gap-4 flex-wrap">
        <button className="bg-red-500 text-white px-4 py-2 rounded">
          Cancel Order
        </button>

        <button className="bg-yellow-500 text-white px-4 py-2 rounded">
          Return / Replace
        </button>

        <button className="bg-blue-600 text-white px-4 py-2 rounded">
          Download Invoice
        </button>

        <button className="bg-black text-white px-4 py-2 rounded">
          Contact Support
        </button>
      </div>
    </div>
  );
};

export default TrackOrderPage;