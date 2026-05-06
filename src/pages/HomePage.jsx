import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { useDomain } from "../context/DomainContext";
import ProductCard from "../components/ProductCard";
import { Loader2, PackageX } from "lucide-react";

const HomePage = () => {
  const { showSliders, showWelcomeOffer, domain, priceKey } = useDomain();
  const navigate = useNavigate();
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [visibleCount, setVisibleCount] = useState(8);
  const [error, setError] = useState(null);
  const [popupMsg, setPopupMsg] = useState("");

  useEffect(() => {
    if (showWelcomeOffer) {
      fetch(`${import.meta.env.VITE_API_URL}/api/products/settings/popup`)
        .then(r => r.json())
        .then(d => {
          if (d.is_active) setPopupMsg(d.message);
        })
        .catch(() => {});
    }
  }, [showWelcomeOffer]);

  const fetchFeatured = async () => {
    setLoading(true);
    try {
      const currentDomain = domain || window.location.hostname;
      const response = await fetch(
        `${import.meta.env.VITE_API_URL}/api/products/?domain=${currentDomain}&price_key=${priceKey || "price_b2c"}`
      );
      if (!response.ok) throw new Error("Connection lost");
      const data = await response.json();
      setProducts(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchFeatured();
  }, [domain]);

  return (
    <div className="min-h-screen bg-white">

      {/* Promo Banner */}
      {showWelcomeOffer && popupMsg && (
        <div className="bg-black text-white py-2.5 px-6 text-center text-xs font-medium tracking-widest">
          {popupMsg}
        </div>
      )}

      {/* Hero */}
      {showSliders && (
        <section className="relative w-full h-[85vh] bg-gray-50 overflow-hidden">
          <img
            src="/src/assets/images/web_banner.jpg"
            className="w-full h-full object-cover"
            alt="Hero"
          />
          {/* Subtle dark overlay */}
          <div className="absolute inset-0 bg-black/30" />
          <div className="absolute inset-0 flex flex-col items-center justify-center text-center px-6">
            <p className="text-white/70 text-xs font-semibold uppercase tracking-[0.4em] mb-5">New Season</p>
            <h1 className="text-5xl sm:text-7xl md:text-8xl font-black text-white tracking-tight leading-none mb-6">
              Spring<br />Collection
            </h1>
            <p className="text-white/80 text-base max-w-md mb-10 leading-relaxed font-light">
              Discover the latest seasonal trends crafted with care and designed for the modern individual.
            </p>
            <button
              onClick={() => navigate('/products')}
              className="px-10 py-4 bg-white text-black text-sm font-semibold rounded-full hover:bg-gray-100 transition-all active:scale-95 shadow-xl"
            >
              Shop Now
            </button>
          </div>
        </section>
      )}

      {/* Category Strip */}
      <section className="border-b border-gray-100">
        <div className="max-w-7xl mx-auto px-6 py-5 flex items-center justify-center gap-2 overflow-x-auto">
          {[
            { label: "All", path: "/products" },
            { label: "Women", path: "/women" },
            { label: "Men", path: "/men" },
            { label: "Kids", path: "/kids" },
            { label: "Ethnic", path: "/ethnic" },
            { label: "Western", path: "/western" },
            { label: "Party Wear", path: "/party-wear" },
          ].map(cat => (
            <button
              key={cat.label}
              onClick={() => navigate(cat.path)}
              className="flex-shrink-0 px-5 py-2 rounded-full border border-gray-200 text-xs font-semibold text-gray-600 hover:border-black hover:text-black hover:bg-gray-50 transition-all duration-150"
            >
              {cat.label}
            </button>
          ))}
        </div>
      </section>

      {/* Products Section */}
      <section className="max-w-7xl mx-auto px-6 py-16">
        <div className="flex items-end justify-between mb-10">
          <div>
            <p className="text-xs font-semibold text-gray-400 uppercase tracking-widest mb-1">Handpicked for you</p>
            <h2 className="text-3xl font-black text-black tracking-tight">Featured Styles</h2>
          </div>
          <button
            onClick={() => navigate('/products')}
            className="text-sm font-semibold text-gray-500 hover:text-black transition-colors underline underline-offset-4"
          >
            View all
          </button>
        </div>

        {loading ? (
          <div className="flex flex-col items-center justify-center py-24 gap-4">
            <Loader2 className="w-8 h-8 text-gray-400 animate-spin" />
            <p className="text-xs text-gray-400 uppercase tracking-widest">Loading...</p>
          </div>
        ) : error ? (
          <div className="text-center py-20">
            <PackageX size={40} className="mx-auto text-gray-300 mb-4" />
            <p className="text-sm text-gray-400">Unable to load products.</p>
          </div>
        ) : (
          <>
            <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-4 sm:gap-6">
              {products.slice(0, visibleCount).map((product) => (
                <ProductCard key={product.id} product={product} />
              ))}
            </div>

            {visibleCount < products.length && (
              <div className="flex justify-center mt-14">
                <button
                  onClick={() => setVisibleCount(v => v + 8)}
                  className="px-10 py-3.5 border border-black text-black text-sm font-semibold rounded-full hover:bg-black hover:text-white transition-all duration-200 active:scale-95"
                >
                  Load More
                </button>
              </div>
            )}
          </>
        )}
      </section>

      {/* Trust Badges */}
      <section className="border-t border-gray-100 py-12">
        <div className="max-w-7xl mx-auto px-6 grid grid-cols-2 md:grid-cols-4 gap-8 text-center">
          {[
            { title: "Free Shipping", sub: "On orders above ₹999" },
            { title: "Secure Checkout", sub: "100% safe & encrypted" },
            { title: "Premium Quality", sub: "Curated collections" },
            { title: "Easy Returns", sub: "7-day return policy" },
          ].map(b => (
            <div key={b.title} className="space-y-1">
              <p className="text-sm font-semibold text-black">{b.title}</p>
              <p className="text-xs text-gray-400">{b.sub}</p>
            </div>
          ))}
        </div>
      </section>

    </div>
  );
};

export default HomePage;