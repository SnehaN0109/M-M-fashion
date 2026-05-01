import { Link } from "react-router-dom";
import { CreditCard } from "lucide-react";

const PaymentPage = () => {
  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center px-6">
      <div className="max-w-md w-full bg-white rounded-3xl shadow-xl p-10 text-center">
        <div className="w-20 h-20 bg-pink-50 rounded-full flex items-center justify-center mx-auto mb-6">
          <CreditCard size={40} className="text-pink-600" />
        </div>
        <h1 className="text-2xl font-black text-gray-900 mb-2">Payment Coming Soon</h1>
        <p className="text-gray-500 font-medium mb-8">
          Online payment integration is under development. All orders are currently processed as Cash on Delivery.
        </p>
        <Link
          to="/checkout"
          className="block w-full bg-pink-600 text-white font-black py-4 rounded-2xl hover:bg-pink-700 transition"
        >
          Back to Checkout
        </Link>
      </div>
    </div>
  );
};

export default PaymentPage;
