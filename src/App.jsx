import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

/* ===== Layout Components ===== */
import Navbar from "./components/Navbar";
import Footer from "./components/Footer";

/* ===== Pages ===== */
import HomePage from "./pages/HomePage";
import ProductListPage from "./pages/ProductListPage";
import ProductDetailPage from "./pages/ProductDetailPage";
import CartPage from "./pages/CartPage";
import CheckoutPage from "./pages/CheckoutPage";
import PaymentPage from "./pages/PaymentPage";
import OrderSuccessPage from "./pages/OrderSuccessPage";
import TrackOrderPage from "./pages/TrackOrderPage";
import SearchResultsPage from "./pages/SearchResultsPage";
import WishlistPage from "./pages/WishlistPage";
import WhatsAppLoginPage from "./pages/WhatsAppLoginPage";
import MyOrdersPage from "./pages/MyOrdersPage";
import UploadUserPhotosPage from "./pages/UploadUserPhotosPage";
import AboutUsPage from "./pages/AboutUsPage";
import ContactUsPage from "./pages/ContactUsPage";
import ShippingPolicyPage from "./pages/ShippingPolicyPage";
import ReturnRefundPage from "./pages/ReturnRefundPage";
import PrivacyPolicyPage from "./pages/PrivacyPolicyPage";

/* ===== Category Pages Removed (Now using ProductListPage with props) ===== */

function App() {
  return (
    <Router>
      <Navbar />

      <Routes>

        {/* ===== Home ===== */}
        <Route path="/" element={<HomePage />} />

        {/* ===== Categories ===== */}
        <Route path="/men" element={<ProductListPage category="Men" />} />
        <Route path="/women" element={<ProductListPage category="Women" />} />
        <Route path="/kids" element={<ProductListPage category="Kids" />} />
        <Route path="/ethnic" element={<ProductListPage category="Ethnic" />} />
        <Route path="/western" element={<ProductListPage category="Western" />} />
        <Route path="/party-wear" element={<ProductListPage category="Party Wear" />} />

        {/* ===== Products ===== */}
        <Route path="/products" element={<ProductListPage />} />
        <Route path="/product/:id" element={<ProductDetailPage />} />

        {/* ===== Cart & Checkout ===== */}
        <Route path="/cart" element={<CartPage />} />
        <Route path="/checkout" element={<CheckoutPage />} />
        <Route path="/payment" element={<PaymentPage />} />
        <Route path="/order-success" element={<OrderSuccessPage />} />

        {/* ===== Orders ===== */}
        <Route path="/my-orders" element={<MyOrdersPage />} />
        <Route path="/trackorder/:orderId" element={<TrackOrderPage />} />

        {/* ===== Search ===== */}
        <Route path="/search" element={<SearchResultsPage />} />

        {/* ===== Wishlist ===== */}
        <Route path="/wishlist" element={<WishlistPage />} />

        {/* ===== Authentication ===== */}
        <Route path="/login" element={<WhatsAppLoginPage />} />

        {/* ===== Upload Photos ===== */}
        <Route path="/upload-photos" element={<UploadUserPhotosPage />} />

        {/* ===== Information Pages ===== */}
        <Route path="/about-us" element={<AboutUsPage />} />
        <Route path="/contact-us" element={<ContactUsPage />} />
        <Route path="/shipping-policy" element={<ShippingPolicyPage />} />
        <Route path="/return-refund" element={<ReturnRefundPage />} />
        <Route path="/privacy-policy" element={<PrivacyPolicyPage />} />

        {/* ===== 404 Page ===== */}
        <Route
          path="*"
          element={
            <div className="text-center mt-16">
              <h1 className="text-3xl font-semibold">404 - Page Not Found</h1>
              <p className="text-gray-500 mt-2">
                The page you are looking for does not exist.
              </p>
            </div>
          }
        />

      </Routes>

      <Footer />
    </Router>
  );
}

export default App;