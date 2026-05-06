import { useDomain } from "../context/DomainContext";
import { Truck, Clock, MapPin, AlertCircle } from "lucide-react";

const Section = ({ title, children }) => (
  <div className="space-y-3">
    <h2 className="text-lg font-black text-gray-900">{title}</h2>
    <div className="text-gray-600 leading-relaxed space-y-2">{children}</div>
  </div>
);

const ShippingPolicyPage = () => {
  const { brandName, supportEmail } = useDomain();

  return (
    <div className="bg-white">
      <div className="bg-gradient-to-br from-pink-50 to-rose-100 py-14 text-center px-6">
        <h1 className="text-4xl font-black text-gray-900 mb-3">Shipping Policy</h1>
        <p className="text-gray-600 max-w-xl mx-auto">Everything you need to know about how {brandName} ships your orders.</p>
      </div>

      <div className="max-w-3xl mx-auto px-6 py-14 space-y-10">

        {/* Quick cards */}
        <div className="grid sm:grid-cols-3 gap-4">
          {[
            { icon: Clock, title: "Processing Time", value: "1–2 business days" },
            { icon: Truck, title: "Delivery Time", value: "3–7 business days" },
            { icon: MapPin, title: "Shipping Coverage", value: "Pan India" },
          ].map(({ icon: Icon, title, value }) => (
            <div key={title} className="border rounded-2xl p-5 text-center space-y-2">
              <Icon size={22} className="text-pink-600 mx-auto" />
              <p className="text-xs font-black text-gray-400 uppercase tracking-widest">{title}</p>
              <p className="font-black text-gray-900">{value}</p>
            </div>
          ))}
        </div>

        <Section title="Shipping Charges">
          <p>Orders above <strong>₹999</strong> qualify for <strong>free shipping</strong>.</p>
          <p>Orders below ₹999 attract a flat shipping fee of <strong>₹99</strong>.</p>
        </Section>

        <Section title="Order Processing">
          <p>Orders are processed within 1–2 business days after payment confirmation.</p>
          <p>Orders placed on Sundays or public holidays are processed the next business day.</p>
        </Section>

        <Section title="Delivery Timeline">
          <p>Standard delivery takes <strong>3–7 business days</strong> depending on your location.</p>
          <p>Metro cities (Mumbai, Delhi, Bangalore, etc.) typically receive orders in 3–4 days.</p>
          <p>Remote or rural areas may take up to 7–10 business days.</p>
        </Section>

        <Section title="Order Tracking">
          <p>Once your order is shipped, you will receive a tracking number via SMS/email.</p>
          <p>You can also track your order anytime from the <strong>My Orders</strong> section.</p>
        </Section>

        <Section title="Damaged or Lost Shipments">
          <p>If your order arrives damaged or is lost in transit, please contact us within <strong>48 hours</strong> of the expected delivery date.</p>
          <p>We will arrange a replacement or full refund after investigation.</p>
        </Section>

        <div className="bg-pink-50 border border-pink-100 rounded-2xl p-5 flex gap-3">
          <AlertCircle size={20} className="text-pink-600 flex-shrink-0 mt-0.5" />
          <p className="text-sm text-gray-600">
            For any shipping queries, reach us at <strong>{supportEmail}</strong> or WhatsApp us directly.
          </p>
        </div>

        <p className="text-xs text-gray-400">Last updated: April 2026</p>
      </div>
    </div>
  );
};

export default ShippingPolicyPage;
