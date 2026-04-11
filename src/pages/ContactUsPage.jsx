import React from "react";

const ContactUsPage = () => {
  return (
    <div className="bg-white text-gray-800">

      {/* Hero Section */}
      <div className="bg-pink-100 py-16 text-center px-6">
        <h1 className="text-4xl font-bold mb-4">Contact Us</h1>
        <p className="text-lg max-w-2xl mx-auto">
          Have questions? Need help with your order? We’re here to assist you.
        </p>
      </div>

      {/* Contact Info Cards */}
      <div className="max-w-6xl mx-auto px-6 py-16 grid md:grid-cols-3 gap-8">

        <div className="shadow-md p-6 rounded-xl text-center">
          <h3 className="font-semibold text-lg mb-2">Email Support</h3>
          <p className="text-gray-600">support@garba.shop</p>
        </div>

        <div className="shadow-md p-6 rounded-xl text-center">
          <h3 className="font-semibold text-lg mb-2">WhatsApp Support</h3>
          <p className="text-gray-600">+91 98765 43210</p>
        </div>

        <div className="shadow-md p-6 rounded-xl text-center">
          <h3 className="font-semibold text-lg mb-2">Working Hours</h3>
          <p className="text-gray-600">Mon - Sat: 10:00 AM - 7:00 PM</p>
        </div>

      </div>

      {/* Contact Form Section */}
      <div className="max-w-3xl mx-auto px-6 pb-16">
        <h2 className="text-2xl font-semibold mb-6 text-center">
          Send Us a Message
        </h2>

        <form className="space-y-6">

          <input
            type="text"
            placeholder="Full Name"
            className="w-full border p-3 rounded-lg focus:outline-none focus:ring-2 focus:ring-pink-400"
          />

          <input
            type="email"
            placeholder="Email Address"
            className="w-full border p-3 rounded-lg focus:outline-none focus:ring-2 focus:ring-pink-400"
          />

          <input
            type="text"
            placeholder="WhatsApp Number"
            className="w-full border p-3 rounded-lg focus:outline-none focus:ring-2 focus:ring-pink-400"
          />

          <input
            type="text"
            placeholder="Order ID (Optional)"
            className="w-full border p-3 rounded-lg focus:outline-none focus:ring-2 focus:ring-pink-400"
          />

          <select className="w-full border p-3 rounded-lg focus:outline-none focus:ring-2 focus:ring-pink-400">
            <option>Select Subject</option>
            <option>Order Issue</option>
            <option>Return / Refund</option>
            <option>Size Inquiry</option>
            <option>Payment Issue</option>
            <option>General Question</option>
          </select>

          <textarea
            rows="4"
            placeholder="Your Message"
            className="w-full border p-3 rounded-lg focus:outline-none focus:ring-2 focus:ring-pink-400"
          ></textarea>

          <input type="file" className="w-full" />

          <button
            type="submit"
            className="w-full bg-pink-500 text-white py-3 rounded-lg hover:bg-pink-600 transition duration-300"
          >
            Submit Message
          </button>

        </form>
      </div>

      {/* WhatsApp Floating Button */}
      <div className="fixed bottom-6 right-6">
        <a
          href="https://wa.me/919876543210?text=Hello%20I%20need%20help%20with%20my%20order"
          target="_blank"
          rel="noopener noreferrer"
          className="bg-green-500 text-white px-6 py-3 rounded-full shadow-lg hover:bg-green-600 transition"
        >
          Chat on WhatsApp
        </a>
      </div>

    </div>
  );
};

export default ContactUsPage;