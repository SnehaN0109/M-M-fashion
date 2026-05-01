import { useDomain } from "../context/DomainContext";
import { Heart, Shield, RefreshCw, Star } from "lucide-react";

const AboutUsPage = () => {
  const { brandName, supportEmail, supportPhone } = useDomain();

  return (
    <div className="bg-white text-gray-800">

      {/* Hero */}
      <div className="bg-gradient-to-br from-pink-50 to-rose-100 py-20 text-center px-6">
        <h1 className="text-4xl sm:text-5xl font-black text-gray-900 mb-4">
          Celebrating Style.<br />Delivering Confidence.
        </h1>
        <p className="text-lg text-gray-600 max-w-2xl mx-auto">
          {brandName} — premium Garba and ethnic fashion crafted with care, delivered to your doorstep.
        </p>
      </div>

      {/* Who We Are */}
      <div className="max-w-4xl mx-auto px-6 py-16 space-y-5">
        <h2 className="text-2xl font-black text-gray-900">Who We Are</h2>
        <p className="text-gray-600 leading-relaxed">
          We are a premium clothing manufacturer specialising in traditional Garba and ethnic wear.
          Our mission is to bring authentic cultural designs together with modern comfort and quality.
        </p>
        <p className="text-gray-600 leading-relaxed">
          With years of craftsmanship and strict quality control, we proudly serve customers across
          India through a seamless online shopping experience — from festive lehengas to everyday kurtis.
        </p>
      </div>

      {/* Why Us */}
      <div className="bg-gray-50 py-16">
        <div className="max-w-5xl mx-auto px-6">
          <h2 className="text-2xl font-black text-gray-900 text-center mb-10">Why Shop With Us?</h2>
          <div className="grid sm:grid-cols-2 md:grid-cols-4 gap-6">
            {[
              { icon: Star, title: "Premium Quality", desc: "Every product passes strict quality checks before dispatch." },
              { icon: Shield, title: "Secure Payments", desc: "Safe and encrypted transactions for worry-free shopping." },
              { icon: RefreshCw, title: "Easy Returns", desc: "Hassle-free 7-day return and refund process." },
              { icon: Heart, title: "Customer First", desc: "Dedicated support team ready to help you anytime." },
            ].map(({ icon: Icon, title, desc }) => (
              <div key={title} className="bg-white rounded-2xl p-6 shadow-sm text-center space-y-3">
                <div className="w-12 h-12 bg-pink-50 rounded-2xl flex items-center justify-center mx-auto">
                  <Icon size={22} className="text-pink-600" />
                </div>
                <h3 className="font-black text-gray-900">{title}</h3>
                <p className="text-sm text-gray-500 leading-relaxed">{desc}</p>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* What We Offer */}
      <div className="max-w-4xl mx-auto px-6 py-16">
        <h2 className="text-2xl font-black text-gray-900 mb-8">What We Offer</h2>
        <div className="grid sm:grid-cols-2 gap-4">
          {[
            "Exclusive Garba & Festive Collections",
            "Premium Ethnic & Occasion Wear",
            "Multiple Sizes & Colour Options",
            "Real-time Stock Availability",
            "Secure & Easy Checkout",
            "Discount Code Benefits",
            "Verified Customer Reviews",
            "Smooth Order Tracking",
          ].map((item) => (
            <div key={item} className="flex items-center gap-3 bg-gray-50 rounded-xl px-4 py-3">
              <span className="w-2 h-2 rounded-full bg-pink-500 flex-shrink-0" />
              <span className="text-sm font-medium text-gray-700">{item}</span>
            </div>
          ))}
        </div>
      </div>

      {/* Vision */}
      <div className="bg-gradient-to-br from-pink-50 to-rose-100 py-16 text-center px-6">
        <h2 className="text-2xl font-black text-gray-900 mb-4">Our Vision</h2>
        <p className="max-w-2xl mx-auto text-gray-600 leading-relaxed">
          To become a trusted fashion destination where every customer feels confident, valued,
          and inspired by authentic ethnic wear — from Navratri to everyday elegance.
        </p>
        <div className="mt-8 flex flex-col sm:flex-row gap-3 justify-center text-sm text-gray-500">
          <span>📧 {supportEmail}</span>
          <span className="hidden sm:block">·</span>
          <span>📞 {supportPhone}</span>
        </div>
      </div>

    </div>
  );
};

export default AboutUsPage;
