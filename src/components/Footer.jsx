import { Link } from "react-router-dom";

const Footer = () => {
  return (
    <footer className="bg-[#0b1c2d] text-white mt-20">
      <div className="max-w-7xl mx-auto px-6 py-12 grid md:grid-cols-4 gap-8">

        {/* Brand Section */}
        <div>
          <h3 className="text-lg font-semibold mb-4">M&M Fashion</h3>
          <p className="text-sm text-gray-300">
            Premium ethnic & western clothing manufacturer.
          </p>
        </div>

        {/* Company */}
        <div>
          <h3 className="text-lg font-semibold mb-4">Company</h3>
          <ul className="space-y-2 text-sm text-gray-300">
            <li>
              <Link to="/about-us" className="hover:text-pink-400 transition">
                About Us
              </Link>
            </li>
            <li>
              <Link to="/contact-us" className="hover:text-pink-400 transition">
                Contact
              </Link>
            </li>
            <li>
              <Link to="/faq" className="hover:text-pink-400 transition">
                FAQ
              </Link>
            </li>
          </ul>
        </div>

        {/* Policies */}
        <div>
          <h3 className="text-lg font-semibold mb-4">Policies</h3>
          <ul className="space-y-2 text-sm text-gray-300">
            <li>
              <Link to="/shipping-policy" className="hover:text-pink-400 transition">
                Shipping Policy
              </Link>
            </li>
            <li>
              <Link to="/returns" className="hover:text-pink-400 transition">
                Return & Refund
              </Link>
            </li>
            <li>
              <Link to="/privacy-policy" className="hover:text-pink-400 transition">
                Privacy Policy
              </Link>
            </li>
          </ul>
        </div>

        {/* Support */}
        <div>
          <h3 className="text-lg font-semibold mb-4">Support</h3>
          <ul className="space-y-2 text-sm text-gray-300">
            <li>
              <Link to="/whatsapp-support" className="hover:text-pink-400 transition">
                WhatsApp Support
              </Link>
            </li>
            <li>
              <a
                href="mailto:support@mmfashion.com"
                className="hover:text-pink-400 transition"
              >
                Email: support@mmfashion.com
              </a>
            </li>
          </ul>
        </div>

      </div>

      {/* Bottom Copyright */}
      <div className="text-center py-5 border-t border-gray-700 text-sm text-gray-400">
        © 2026 M&M Fashion. All rights reserved.
      </div>
    </footer>
  );
};

export default Footer;