import { useDomain } from "../context/DomainContext";
import { Shield } from "lucide-react";

const Section = ({ title, children }) => (
  <div className="space-y-3">
    <h2 className="text-lg font-black text-gray-900">{title}</h2>
    <div className="text-gray-600 leading-relaxed space-y-2">{children}</div>
  </div>
);

const PrivacyPolicyPage = () => {
  const { brandName, supportEmail } = useDomain();

  return (
    <div className="bg-white">
      <div className="bg-gradient-to-br from-pink-50 to-rose-100 py-14 text-center px-6">
        <Shield size={36} className="text-pink-600 mx-auto mb-3" />
        <h1 className="text-4xl font-black text-gray-900 mb-3">Privacy Policy</h1>
        <p className="text-gray-600 max-w-xl mx-auto">
          How {brandName} collects, uses, and protects your personal information.
        </p>
      </div>

      <div className="max-w-3xl mx-auto px-6 py-14 space-y-10">

        <Section title="Information We Collect">
          <p>When you use our platform, we may collect the following information:</p>
          <ul className="list-disc list-inside space-y-1 pl-2">
            <li>Name, phone number, and email address</li>
            <li>Shipping and billing address</li>
            <li>Order history and preferences</li>
            <li>Device and browser information for analytics</li>
          </ul>
        </Section>

        <Section title="How We Use Your Information">
          <p>Your information is used to:</p>
          <ul className="list-disc list-inside space-y-1 pl-2">
            <li>Process and deliver your orders</li>
            <li>Send order updates via WhatsApp or email</li>
            <li>Improve our products and services</li>
            <li>Respond to customer support queries</li>
            <li>Send promotional offers (only with your consent)</li>
          </ul>
        </Section>

        <Section title="Data Sharing">
          <p>
            We do <strong>not</strong> sell or rent your personal data to third parties. We may
            share limited information with:
          </p>
          <ul className="list-disc list-inside space-y-1 pl-2">
            <li>Logistics partners for order delivery</li>
            <li>Payment gateways for secure transaction processing</li>
            <li>Legal authorities if required by law</li>
          </ul>
        </Section>

        <Section title="Cookies">
          <p>
            We use cookies to enhance your browsing experience, remember your cart, and analyze
            site traffic. You can disable cookies in your browser settings, though some features
            may not function correctly.
          </p>
        </Section>

        <Section title="Data Security">
          <p>
            We implement industry-standard security measures to protect your data. All payment
            transactions are encrypted and processed through secure payment gateways. We do not
            store your card or UPI details on our servers.
          </p>
        </Section>

        <Section title="Your Rights">
          <p>You have the right to:</p>
          <ul className="list-disc list-inside space-y-1 pl-2">
            <li>Access the personal data we hold about you</li>
            <li>Request correction or deletion of your data</li>
            <li>Opt out of marketing communications at any time</li>
          </ul>
          <p>
            To exercise these rights, contact us at <strong>{supportEmail}</strong>.
          </p>
        </Section>

        <Section title="Changes to This Policy">
          <p>
            We may update this Privacy Policy from time to time. Any changes will be posted on
            this page with an updated date. Continued use of {brandName} after changes constitutes
            acceptance of the revised policy.
          </p>
        </Section>

        <p className="text-xs text-gray-400">Last updated: April 2026</p>
      </div>
    </div>
  );
};

export default PrivacyPolicyPage;
