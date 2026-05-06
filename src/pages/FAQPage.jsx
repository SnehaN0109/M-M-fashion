import { useState } from "react";
import { useDomain } from "../context/DomainContext";
import { ChevronDown, ChevronUp } from "lucide-react";

const faqs = [
  {
    category: "Orders",
    items: [
      {
        q: "How do I place an order?",
        a: "Browse our collection, add items to your cart, and proceed to checkout. Pay securely via UPI.",
      },
      {
        q: "Can I modify or cancel my order after placing it?",
        a: "Orders can be modified or cancelled within 12 hours of placement. Contact us via WhatsApp or email immediately after placing the order.",
      },
      {
        q: "How will I know my order is confirmed?",
        a: "You will receive an order confirmation via SMS and email once your payment is successful.",
      },
    ],
  },
  {
    category: "Shipping",
    items: [
      {
        q: "How long does delivery take?",
        a: "Standard delivery takes 3–7 business days. Metro cities usually receive orders in 3–4 days.",
      },
      {
        q: "Is there free shipping?",
        a: "Yes! Orders above ₹999 qualify for free shipping. A flat fee of ₹99 applies to orders below ₹999.",
      },
      {
        q: "How can I track my order?",
        a: "Once shipped, you will receive a tracking link via SMS. You can also track from the My Orders section.",
      },
    ],
  },
  {
    category: "Returns & Refunds",
    items: [
      {
        q: "What is your return policy?",
        a: "We accept returns within 7 days of delivery for unused items in original condition with tags intact.",
      },
      {
        q: "How long does a refund take?",
        a: "Refunds are processed within 5–7 business days after we receive and inspect the returned item.",
      },
      {
        q: "What if I received a wrong or damaged item?",
        a: "Contact us within 48 hours of delivery with photos. We will arrange a free replacement or full refund.",
      },
    ],
  },
  {
    category: "Payments",
    items: [
      {
        q: "What payment methods do you accept?",
        a: "We accept UPI payments (GPay, PhonePe, Paytm, and any UPI app). Pay after placing your order and upload the screenshot for verification.",
      },
      {
        q: "Is it safe to pay on your website?",
        a: "Yes. All transactions are encrypted and processed through secure payment gateways. We never store your card details.",
      },
      {
        q: "Can I use multiple payment methods for one order?",
        a: "Currently, we support one payment method per order. You can use a coupon code along with your chosen payment method.",
      },
    ],
  },
];

const AccordionItem = ({ q, a }) => {
  const [open, setOpen] = useState(false);

  return (
    <div className="border-b last:border-b-0">
      <button
        onClick={() => setOpen(!open)}
        className="w-full flex items-center justify-between py-4 text-left gap-4 focus:outline-none"
      >
        <span className="font-semibold text-gray-800">{q}</span>
        {open ? (
          <ChevronUp size={18} className="text-pink-500 flex-shrink-0" />
        ) : (
          <ChevronDown size={18} className="text-gray-400 flex-shrink-0" />
        )}
      </button>
      {open && (
        <p className="pb-4 text-gray-600 leading-relaxed text-sm">{a}</p>
      )}
    </div>
  );
};

const FAQPage = () => {
  const { brandName, supportEmail } = useDomain();

  return (
    <div className="bg-white">
      <div className="bg-gradient-to-br from-pink-50 to-rose-100 py-14 text-center px-6">
        <h1 className="text-4xl font-black text-gray-900 mb-3">FAQs</h1>
        <p className="text-gray-600 max-w-xl mx-auto">
          Got questions? We've got answers. Here are the most common queries about {brandName}.
        </p>
      </div>

      <div className="max-w-3xl mx-auto px-6 py-14 space-y-10">
        {faqs.map(({ category, items }) => (
          <div key={category}>
            <h2 className="text-base font-black text-pink-600 uppercase tracking-widest mb-3">
              {category}
            </h2>
            <div className="border rounded-2xl px-5 divide-y">
              {items.map((item) => (
                <AccordionItem key={item.q} q={item.q} a={item.a} />
              ))}
            </div>
          </div>
        ))}

        <div className="bg-pink-50 border border-pink-100 rounded-2xl p-6 text-center space-y-2">
          <p className="font-black text-gray-900">Still have questions?</p>
          <p className="text-sm text-gray-600">
            Reach us at <strong>{supportEmail}</strong> or WhatsApp us — we typically reply within a few hours.
          </p>
        </div>

        <p className="text-xs text-gray-400">Last updated: April 2026</p>
      </div>
    </div>
  );
};

export default FAQPage;
