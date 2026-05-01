import React, { useState, useEffect } from "react";
import { useDomain } from "../context/DomainContext";
import ProductCard from "../components/ProductCard";
import { Search, SlidersHorizontal, PackageX, Loader2 } from "lucide-react";

// Modern Sidebar Filters
const Filters = ({ onFilter, activeFilters }) => {
  const [filters, setFilters] = useState({
    size: "", color: "", category: "", min_price: "", max_price: ""
  });

  const sizes = ["S", "M", "L", "XL", "XXL"];
  const colors = ["Red", "Blue", "Green", "Black", "Pink", "White", "Yellow", "Maroon", "Gold"];
  const categories = ["Ethnic", "Western", "Men", "Kids", "Party Wear"];

  const handleChange = (name, value) => {
    const updated = { ...filters, [name]: value };
    setFilters(updated);
    onFilter(updated);
  };

  return (
    <div className="bg-white rounded-3xl p-6 shadow-sm border border-gray-100 space-y-8 sticky top-24 h-fit hidden lg:block w-72">
      <div className="flex items-center justify-between border-b pb-4">
        <h2 className="font-black text-xl text-gray-900 tracking-tight">Filters</h2>
        <SlidersHorizontal size={18} className="text-gray-400" />
      </div>
      
      {/* Category */}
      <div className="space-y-4">
        <h3 className="text-xs font-black text-gray-400 uppercase tracking-widest">Collection</h3>
        <div className="space-y-2">
          {["", ...categories].map((cat) => (
            <label key={cat} className="flex items-center gap-3 cursor-pointer group">
              <input 
                type="radio" 
                name="category" 
                checked={filters.category === cat}
                onChange={() => handleChange("category", cat)}
                className="w-4 h-4 accent-pink-600 border-gray-300"
              />
              <span className={`text-sm font-medium transition-colors ${filters.category === cat ? "text-pink-600" : "text-gray-600 group-hover:text-gray-900"}`}>
                {cat || "All Collections"}
              </span>
            </label>
          ))}
        </div>
      </div>

      {/* Sizes */}
      <div className="space-y-4">
        <h3 className="text-xs font-black text-gray-400 uppercase tracking-widest">Size</h3>
        <div className="flex flex-wrap gap-2">
          {sizes.map((opt) => (
            <button
              key={opt}
              onClick={() => handleChange("size", filters.size === opt ? "" : opt)}
              className={`w-10 h-10 flex items-center justify-center rounded-xl border text-xs font-bold transition-all ${filters.size === opt ? "bg-gray-900 text-white border-gray-900 shadow-lg" : "border-gray-100 hover:border-pink-300 text-gray-600"}`}
            >
              {opt}
            </button>
          ))}
        </div>
      </div>

      {/* Colors */}
      <div className="space-y-4">
        <h3 className="text-xs font-black text-gray-400 uppercase tracking-widest">Color</h3>
        <div className="grid grid-cols-5 gap-2">
          {colors.map((c) => (
            <button 
              key={c}
              onClick={() => handleChange("color", filters.color === c ? "" : c)}
              title={c}
              className={`w-8 h-8 rounded-full border-2 transition-all scale-95 hover:scale-110 ${filters.color === c ? "border-pink-600 p-0.5" : "border-transparent"}`}
            >
              <div className="w-full h-full rounded-full shadow-inner" style={{ backgroundColor: c.toLowerCase() }} />
            </button>
          ))}
        </div>
      </div>

      {/* Price */}
      <div className="space-y-4">
        <h3 className="text-xs font-black text-gray-400 uppercase tracking-widest">Price Point</h3>
        <div className="grid grid-cols-2 gap-3">
          <input 
             type="number" 
             placeholder="From" 
             className="bg-gray-50 border-none rounded-xl p-3 text-sm focus:ring-2 ring-pink-500 w-full"
             onChange={(e) => handleChange("min_price", e.target.value)} 
          />
          <input 
             type="number" 
             placeholder="To" 
             className="bg-gray-50 border-none rounded-xl p-3 text-sm focus:ring-2 ring-pink-500 w-full"
             onChange={(e) => handleChange("max_price", e.target.value)} 
          />
        </div>
      </div>
    </div>
  );
};

const ProductListPage = ({ category: initialCategory }) => {
  const { domain, priceKey } = useDomain();
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [search, setSearch] = useState("");

  const fetchProducts = async (filters = {}) => {
    setLoading(true);
    try {
      const queryParams = new URLSearchParams({
        domain: domain || window.location.hostname,
        price_key: priceKey || "price_b2c",
        category: initialCategory || "",
        ...filters
      });
      const response = await fetch(`${import.meta.env.VITE_API_URL}/api/products/?${queryParams}`);
      if (!response.ok) throw new Error("Our shop is currently restyling. Please try again later.");
      const data = await response.json();
      setProducts(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchProducts();
  }, [domain, priceKey, initialCategory]);

  const handleFilter = (filters) => {
    fetchProducts(filters);
  };

  const handleSearch = (e) => {
    e.preventDefault();
    fetchProducts({ search });
  };

  return (
    <div className="bg-[#fafafa] min-h-screen">
      {/* Dynamic Header */}
      <div className="bg-white pt-12 pb-16 border-b border-gray-100">
        <div className="max-w-7xl mx-auto px-6 flex flex-col items-center text-center">
          <h1 className="text-5xl md:text-6xl font-black text-gray-900 tracking-tighter mb-4">
            New Collections <span className="text-pink-600">.</span>
          </h1>
          <p className="max-w-xl text-gray-500 font-medium text-lg leading-relaxed">
            Curated pieces from premium labels, designed for comfort and crafted with elegance.
          </p>
          
          {/* Search Bar */}
          <form onSubmit={handleSearch} className="mt-8 relative w-full max-w-2xl group">
             <input 
                type="text" 
                placeholder="Search for styles, collections, or trends..."
                className="w-full bg-white border border-gray-200 rounded-2xl py-5 pl-14 pr-6 text-gray-900 placeholder:text-gray-400 focus:outline-none focus:ring-4 focus:ring-pink-500/10 focus:border-pink-600 transition-all shadow-sm group-hover:shadow-md"
                value={search}
                onChange={(e) => setSearch(e.target.value)}
             />
             <Search className="absolute left-5 top-1/2 -translate-y-1/2 text-gray-400 group-hover:text-pink-600 transition-colors" size={22} />
             <button type="submit" className="hidden">Search</button>
          </form>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-6 flex gap-12 py-16">
        {/* Sidebar */}
        <Filters onFilter={handleFilter} />

        {/* Product Grid Container */}
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
              <button 
                onClick={() => fetchProducts()} 
                className="px-8 py-3 bg-gray-900 text-white font-bold rounded-2xl hover:bg-black transition shadow-lg active:scale-95"
              >
                Reconnect to Shop
              </button>
            </div>
          ) : (
            <>
              <div className="mb-10 flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
                <div>
                   <span className="text-sm font-black text-gray-400 uppercase tracking-widest">Results</span>
                   <h2 className="text-2xl font-bold text-gray-900">{products.length} Products Found</h2>
                </div>
                
                <div className="flex items-center gap-4 bg-white p-2 rounded-2xl border border-gray-100 shadow-sm">
                   <select className="border-none bg-transparent text-sm font-bold text-gray-700 focus:ring-0 cursor-pointer pr-8">
                     <option>Sort by: Latest Arrived</option>
                     <option>Price: Low to High</option>
                     <option>Price: High to Low</option>
                   </select>
                </div>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-3 gap-8">
                {products.map((product) => (
                  <ProductCard key={product.id} product={product} />
                ))}
              </div>

              {products.length === 0 && (
                <div className="flex flex-col items-center justify-center py-32 bg-white rounded-[40px] border border-gray-100 shadow-sm">
                  <div className="w-20 h-20 bg-gray-50 rounded-full flex items-center justify-center mb-6 text-gray-300">
                     <Search size={40} />
                  </div>
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