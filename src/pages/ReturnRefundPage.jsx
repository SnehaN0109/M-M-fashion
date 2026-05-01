import { useDomain } from "../context/DomainContext";
import { RefreshCw, XCircle, CheckCircle, AlertCircle } from "lucide-react";

const Section = ({ title, children }) => (
  <div className="space-y-3">
    <h2 className="text-lg font-black text-gray-900">{title}</h2>
    <div className="text-gray-600 leading-relaxed space-y-2">{children}</div>
  </div>
);

const ReturnRefundPage = () => {
  const { brandName, supportEmail } = useDomain();

  return (
    <div className="bg-white">
      <div className="bg-gradient-to-br from-pink-50 to-rose-100 py-14 text-center px-6">
        <h1 className="text-4xl font-black text-gray-900 mb-3">Returns &amp; Refunds</h1>
        <p className="text-gray-600 max-w-xl mx-auto">
          Our hassle-free return policy so you can shop at {brandName} with confidence.
        </p>
      </div>

      <div className="max-w-3xl mx-auto px-6 py-14 space-y-10">

        {/* Quick cards */}
        <div className="grid sm:grid-cols-3 gap-4">
          {[
            { icon: RefreshCw, title: "Return Window", value: "7 days from delivery" },
            { icon: CheckCircle, title: "Refund Mode", value: "Original payment method" },
            { icon: XCircle, title: "Non-Returnable", value: "Sale & stitched items" },
          ].map(({ icon: Icon, title, value }) => (
            <div key={title} className="border rounded-2xl p-5 text-center space-y-2">
              <Icon size={22} className="text-pink-600 mx-auto" />
              <p className="text-xs font-black text-gray-400 uppercase tracking-widest">{title}</p>
              <p className="font-black text-gray-900">{value}</p>
            </div>
          ))}
        </div>

        <Section title="Return Eligibility">
          <p>Items can be returned within <strong>7 days</strong> of delivery if they are:</p>
          <ul className="list-disc list-inside space-y-1 pl-2">
            <li>Unused, unwashed, and in original condition</li>
            <li>With all original tags and packaging intact</li>
            <li>Accompanied by the original invoice</li>
          </ul>
        </Section>

        <Section title="Non-Returnable Items">
          <p>The following items are <strong>not eligible</strong> for return:</p>
          <ul className="list-disc list-inside space-y-1 pl-2">
            <li>Items purchased during sale or with discount codes</li>
            <li>Custom-stitched or altered garments</li>
            <li>Innerwear, lingerie, and accessories</li>
            <li>Items that have been used, washed, or damaged by the customer</li>
          </ul>
        </Section>

        <Section title="How to Initiate a Return">
          <p>To start a return, follow these steps:</p>
          <ol className="list-decimal list-inside space-y-1 pl-2">
            <li>Contact us via WhatsApp or email within 7 days of delivery</li>
            <li>Share your order ID and reason for return with photos</li>
            <li>Our team will review and approve the return within 24–48 hours</li>
            <li>Ship the item back to our address (provided upon approval)</li>
          </ol>
        </Section>

        <Section title="Refund Process">
          <p>Once we receive and inspect the returned item:</p>
          <ul className="list-disc list-inside space-y-1 pl-2">
            <li>Refunds are processed within <strong>5–7 business days</strong></li>
            <li>Amount is credited to your original payment method</li>
            <li>UPI / bank transfer refunds may take 3–5 additional banking days</li>
          </ul>
        </Section>

        <Section title="Damaged or Wrong Items">
          <p>
            If you received a damaged, defective, or wrong item, please contact us within{" "}
            <strong>48 hours</strong> of delivery with photos. We will arrange a free replacement
            or full refund at no extra cost.
          </p>
        </Section>

        <div className="bg-pink-50 border border-pink-100 rounded-2xl p-5 flex gap-3">
          <AlertCircle size={20} className="text-pink-600 flex-shrink-0 mt-0.5" />
          <p className="text-sm text-gray-600">
            For return or refund queries, reach us at <strong>{supportEmail}</strong> or WhatsApp us directly.
          </p>
        </div>

        <p className="text-xs text-gray-400">Last updated: April 2026</p>
      </div>
    </div>
  );
};

export default ReturnRefundPage;
