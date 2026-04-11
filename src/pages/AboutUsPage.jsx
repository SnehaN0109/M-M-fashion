import React from "react";

const AboutUsPage = () => {
  return (
    <div className="bg-white text-gray-800">

      {/* Hero Section */}
      <div className="bg-pink-100 py-16 text-center px-6">
        <h1 className="text-4xl font-bold mb-4">
          Celebrating Style. Delivering Confidence.
        </h1>
        <p className="text-lg max-w-2xl mx-auto">
          Premium Garba and ethnic fashion crafted with care and delivered
          directly to your doorstep.
        </p>
      </div>

      {/* Who We Are */}
      <div className="max-w-6xl mx-auto px-6 py-16">
        <h2 className="text-2xl font-semibold mb-6">Who We Are</h2>
        <p className="leading-7 mb-4">
          We are a premium clothing manufacturer specializing in traditional
          Garba and ethnic wear. Our mission is to bring authentic cultural
          designs together with modern comfort and quality.
        </p>
        <p className="leading-7">
          With years of craftsmanship and strict quality control, we proudly
          serve customers across India and internationally through a seamless
          online shopping experience.
        </p>
      </div>

      {/* What We Offer */}
      <div className="bg-gray-100 py-16">
        <div className="max-w-6xl mx-auto px-6">
          <h2 className="text-2xl font-semibold mb-8">What We Offer</h2>
          <div className="grid md:grid-cols-2 gap-8">
            <ul className="list-disc pl-6 space-y-3">
              <li>Exclusive Garba & Festive Collections</li>
              <li>Premium Ethnic & Occasion Wear</li>
              <li>Multiple Sizes & Color Options</li>
              <li>Real-time Stock Availability</li>
            </ul>
            <ul className="list-disc pl-6 space-y-3">
              <li>Secure & Easy Checkout</li>
              <li>Discount Code Benefits</li>
              <li>Verified Customer Reviews</li>
              <li>Wishlist & Smooth Order Tracking</li>
            </ul>
          </div>
        </div>
      </div>

      {/* Why Choose Us */}
      <div className="max-w-6xl mx-auto px-6 py-16">
        <h2 className="text-2xl font-semibold mb-8 text-center">
          Why Shop With Us?
        </h2>

        <div className="grid md:grid-cols-3 gap-8 text-center">
          <div className="p-6 shadow-md rounded-xl">
            <h3 className="font-semibold mb-2 text-lg">Premium Quality</h3>
            <p>
              Every product goes through strict quality checks before dispatch.
            </p>
          </div>

          <div className="p-6 shadow-md rounded-xl">
            <h3 className="font-semibold mb-2 text-lg">Secure Payments</h3>
            <p>
              Safe and encrypted transactions for a worry-free shopping
              experience.
            </p>
          </div>

          <div className="p-6 shadow-md rounded-xl">
            <h3 className="font-semibold mb-2 text-lg">Easy Returns</h3>
            <p>
              Hassle-free return and refund process designed for customer
              convenience.
            </p>
          </div>
        </div>
      </div>

      {/* Vision Section */}
      <div className="bg-pink-100 py-16 text-center px-6">
        <h2 className="text-2xl font-semibold mb-4">Our Vision</h2>
        <p className="max-w-2xl mx-auto">
          To become a trusted fashion destination where customers feel
          confident, valued, and inspired by authentic ethnic wear.
        </p>
      </div>

    </div>
  );
};

export default AboutUsPage;