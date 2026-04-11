import { Link } from "react-router-dom";

const MyOrdersPage = () => {
  const orders = [
    { id: "ORD12345", status: "Delivered", total: 4599 },
    { id: "ORD12346", status: "In Transit", total: 2999 },
  ];

  return (
    <div className="max-w-6xl mx-auto px-6 py-10">
      <h1 className="text-3xl font-bold mb-6">My Orders</h1>

      {orders.map((order) => (
        <div key={order.id} className="border rounded-lg p-5 mb-5 shadow-sm">
          <p className="font-semibold text-lg">Order ID: #{order.id}</p>
          <p className="mt-1">Status: {order.status}</p>
          <p>Total: ₹{order.total}</p>

          <div className="mt-3">
            <Link
              to={`/trackorder/${order.id}`}
              className="inline-block bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 transition"
            >
              Track Order
            </Link>
          </div>
        </div>
      ))}
    </div>
  );
};

export default MyOrdersPage;