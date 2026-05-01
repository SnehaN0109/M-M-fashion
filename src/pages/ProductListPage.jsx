import React, { useState, useEffect } from "react";
import { useDomain } from "../context/DomainContext";
import ProductCard from "../components/ProductCard";
import Filters from "../components/Filters";
import { fetchProducts } from "../services/api";
import { Search, Loader2, PackageX } from "lucide-react";

const ProductListPage = ({ category: initialCategory }) => {
  const { domain } = useDomain();
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [search, setSearch] = useState("");

  const loadProducts = async (filters = {}) => {
    setLoading(true);
    try {
      const data = await fetchProducts({
        category: initialCategory || filters.category || "",
        ...filters
      });
      setProducts(data);
      setError(null);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadProducts();
  }, [domain, initialCategory]);

  const handleFilter = (filters) => {
    loadProducts(filters);
  };

  const handleSearch = (e) => {
    e.preventDefault();
    loadProducts({ search });
  };

  return (
    <div className="bg-[#fafafa] min-h-screen">
      <div className="bg-white pt-12 pb-16 border-b border-gray-100">
        <div className="max-w-7xl mx-auto px-6 flex flex-col items-center text-center">
          <h1 className="text-5xl md:text-6xl font-black text-gray-900 tracking-tighter mb-4">
            {initialCategory ? `${initialCategory} Collection` : "New Collections"} <span className="text-pink-600">.</span>
          </h1>
          <p className="max-w-xl text-gray-500 font-medium text-lg leading-relaxed">
            Curated pieces from premium labels, designed for comfort and crafted with elegance.
          </p>
          
          <form onSubmit={handleSearch} className="mt-8 relative w-full max-w-2xl group">
             <input 
                type="text" 
                placeholder="Search for styles, collections, or trends..."
                className="w-full bg-white border border-gray-200 rounded-2xl py-5 pl-14 pr-6 text-gray-900 placeholder:text-gray-400 focus:outline-none focus:ring-4 focus:ring-pink-500/10 focus:border-pink-600 transition-all shadow-sm group-hover:shadow-md"
                value={search}
                onChange={(e) => setSearch(e.target.value)}
             />
             <Search className="absolute left-5 top-1/2 -translate-y-1/2 text-gray-400 group-hover:text-pink-600 transition-colors" size={22} />
          </form>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-6 flex gap-12 py-16">
        <Filters onFilter={handleFilter} />

        <div className="flex-1">
          {loading ? (
            <div className="flex flex-col items-center justify-center py-32 space-y-4">
              <Loader2 className="w-12 h-12 text-pink-600 animate-spin" />
              <p className="text-sm font-bold text-gray-400 uppercase tracking-widest">Loading styles...</p>
            </div>
          ) : error ? (
            <div className="bg-white border-2 border-dashed border-red-100 p-12 rounded-[40px] text-center max-w-lg mx-auto">
              <div className="w-16 h-16 bg-red-50 rounded-full flex items-center justify-center mx-auto mb-6 text-red-600">
                 <PackageX size={32} />
              </div>
              <h2 className="text-2xl font-black text-gray-900 mb-2">Oops! Integration Issue</h2>
              <p className="text-gray-500 mb-8">{error}</p>
              <button onClick={() => loadProducts()} className="px-8 py-3 bg-gray-900 text-white font-bold rounded-2xl hover:bg-black transition shadow-lg active:scale-95">Reconnect</button>
            </div>
          ) : (
            <>
              <div className="mb-10 flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
                <div>
                   <span className="text-sm font-black text-gray-400 uppercase tracking-widest">Results</span>
                   <h2 className="text-2xl font-bold text-gray-900">{products.length} Products Found</h2>
                </div>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-3 gap-8">
                {products.map((product) => (
                  <ProductCard key={product.id} product={product} />
                ))}
              </div>

              {products.length === 0 && (
                <div className="flex flex-col items-center justify-center py-32 bg-white rounded-[40px] border border-gray-100 shadow-sm">
                  <h3 className="text-2xl font-bold text-gray-900 mb-2">No matching styles</h3>
                  <p className="text-gray-500">Try adjusting your filters or search terms.</p>
                </div>
              )}
            </>
          )}
        </div>
      </div>
    </div>
  );
};

export default ProductListPage;