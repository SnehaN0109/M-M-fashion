import React, { useState, useEffect } from "react";
import { useDomain } from "../context/DomainContext";
import ProductCard from "../components/ProductCard";
import { fetchProducts } from "../services/api";
import { ChevronDown, Sparkles, Loader2, PackageX } from "lucide-react";

const HomePage = () => {
  const { showSliders, showWelcomeOffer, domain } = useDomain();
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [visibleCount, setVisibleCount] = useState(8);
  const [error, setError] = useState(null);

  const loadFeatured = async () => {
    setLoading(true);
    try {
      const data = await fetchProducts();
      setProducts(data);
      setError(null);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadFeatured();
  }, [domain]);

  return (
    <div className="min-h-screen bg-white">
      {showWelcomeOffer && (
        <div className="bg-pink-600 text-white overflow-hidden relative">
          <div className="max-w-7xl mx-auto py-3 px-6 text-center text-xs font-black uppercase tracking-[0.3em] flex items-center justify-center gap-4">
             <Sparkles size={16} />
             <span>Welcome Offer: 10% OFF with code FIRST10</span>
             <Sparkles size={16} />
          </div>
        </div>
      )}

      {showSliders && (
        <div className="relative w-full h-[70vh] bg-gray-900 overflow-hidden">
           <img src="https://images.unsplash.com/photo-1490481651871-ab68de25d43d?q=80&w=2070&auto=format&fit=crop" className="w-full h-full object-cover opacity-60" alt="Hero" />
           <div className="absolute inset-0 flex flex-col items-center justify-center text-center text-white px-6">
              <span className="text-sm font-black uppercase tracking-[0.5em] mb-6 animate-pulse">New Arrival</span>
              <h1 className="text-7xl md:text-9xl font-black tracking-tighter mb-8 leading-none">
                SPRING <br/> <span className="text-pink-600">COLLECTION</span>
              </h1>
              <button className="px-12 py-5 bg-white text-gray-900 font-black rounded-full shadow-2xl hover:bg-pink-600 hover:text-white transition-all transform hover:scale-105">
                SHOP THE LOOK
              </button>
           </div>
        </div>
      )}

      <section className="max-w-7xl mx-auto px-6 py-24">
        <div className="flex flex-col items-center text-center mb-16 space-y-4">
           <span className="text-xs font-black text-pink-600 uppercase tracking-widest">Handpicked for you</span>
           <h2 className="text-5xl font-black text-gray-900 tracking-tighter italic">Suggested Styles</h2>
           <div className="w-12 h-1 bg-pink-600 rounded-full" />
        </div>

        {loading ? (
             <div className="flex flex-col items-center justify-center py-20 space-y-4">
               <Loader2 className="w-12 h-12 text-pink-600 animate-spin" />
               <p className="text-xs font-black text-gray-400 uppercase tracking-widest">Loading Boutique...</p>
             </div>
        ) : error ? (
            <div className="text-center py-20 space-y-4 opacity-50">
               <PackageX size={48} className="mx-auto text-gray-400" />
               <p className="text-sm font-black text-gray-400 uppercase tracking-widest">Sync Issue: {error}</p>
            </div>
        ) : (
          <>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-8">
              {products.slice(0, visibleCount).map((product) => (
                <ProductCard key={product.id} product={product} />
              ))}
            </div>

            {visibleCount < products.length && (
              <div className="flex flex-col items-center mt-20 group cursor-pointer" onClick={() => setVisibleCount(v => v + 8)}>
                <div className="px-10 py-4 border-2 border-gray-900 rounded-full font-black text-sm uppercase tracking-widest hover:bg-gray-900 hover:text-white transition-all shadow-lg flex items-center gap-3">
                   Discover More Pieces
                   <ChevronDown size={20} className="group-hover:translate-y-1 transition-transform" />
                </div>
              </div>
            )}
          </>
        )}
      </section>
    </div>
  );
};

export default HomePage;