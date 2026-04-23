import { useDomain } from "../context/DomainContext";
import { FileText } from "lucide-react";

const Section = ({ title, children }) => (
  <div className="space-y-3">
    <h2 className="text-lg font-black text-gray-900">{title}</h2>
    <div className="text-gray-600 leading-relaxed space-y-2">{children}</div>
  </div>
);

const TermsOfServicePage = () => {
  const { brandName, supportEmail } = useDomain();

  return (
    <div className="bg-white">
      <div className="bg-gradient-to-br from-pink-50 to-rose-100 py-14 text-center px-6">
        <FileText size={36} className="text-pink-600 mx-auto mb-3" />
        <h1 className="text-4xl font-black text-gray-900 mb-3">Terms of Service</h1>
        <p className="text-gray-600 max-w-xl mx-auto">
          Please read these terms carefully before using {brandName}.
        </p>
      </div>

      <div className="max-w-3xl mx-auto px-6 py-14 space-y-10">

        <Section title="Acceptance of Terms">
          <p>
            By accessing or using {brandName}, you agree to be bound by these Terms of Service.
            If you do not agree with any part of these terms, please do not use our platform.
          </p>
        </Section>

        <Section title="Use of the Platform">
          <p>You agree to use {brandName} only for lawful purposes. You must not:</p>
          <ul className="list-disc list-inside space-y-1 pl-2">
            <li>Use the platform for any fraudulent or illegal activity</li>
            <li>Attempt to gain unauthorized access to any part of the platform</li>
            <li>Post or transmit harmful, offensive, or misleading content</li>
            <li>Interfere with the normal operation of the website</li>
          </ul>
        </Section>

        <Section title="Account Responsibility">
          <p>
            You are responsible for maintaining the confidentiality of your account credentials.
            Any activity that occurs under your account is your responsibility. Please notify us
            immediately if you suspect unauthorized use of your account.
          </p>
        </Section>

        <Section title="Product Information">
          <p>
            We strive to display accurate product descriptions, images, and pricing. However,
            we do not warrant that product descriptions or other content is error-free. We
            reserve the right to correct any errors and update information at any time.
          </p>
        </Section>

        <Section title="Pricing & Payments">
          <p>
            All prices are listed in Indian Rupees (₹) and are inclusive of applicable taxes.
            We reserve the right to change prices at any time. Payment must be completed before
            an order is processed and shipped.
          </p>
        </Section>

        <Section title="Intellectual Property">
          <p>
            All content on {brandName} — including images, logos, text, and design — is the
            property of {brandName} and is protected by applicable intellectual property laws.
            You may not reproduce, distribute, or use our content without prior written permission.
          </p>
        </Section>

        <Section title="Limitation of Liability">
          <p>
            {brandName} shall not be liable for any indirect, incidental, or consequential
            damages arising from your use of the platform or products purchased. Our total
            liability shall not exceed the amount paid for the specific order in question.
          </p>
        </Section>

        <Section title="Governing Law">
          <p>
            These terms are governed by the laws of India. Any disputes shall be subject to
            the exclusive jurisdiction of the courts in India.
          </p>
        </Section>

        <Section title="Changes to Terms">
          <p>
            We reserve the right to update these Terms of Service at any time. Continued use
            of {brandName} after changes are posted constitutes your acceptance of the revised terms.
          </p>
        </Section>

        <Section title="Contact Us">
          <p>
            For any questions regarding these terms, please contact us at{" "}
            <strong>{supportEmail}</strong>.
          </p>
        </Section>

        <p className="text-xs text-gray-400">Last updated: April 2026</p>
      </div>
    </div>
  );
};

export default TermsOfServicePage;
