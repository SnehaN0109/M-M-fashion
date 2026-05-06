import React, { useState, useEffect, useRef } from "react";
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
    <div className="bg-white rounded-2xl p-5 border border-gray-100 space-y-7 sticky top-20 h-fit hidden lg:block w-64 flex-shrink-0">
      <div className="flex items-center justify-between pb-4 border-b border-gray-100">
        <h2 className="font-semibold text-sm text-black">Filters</h2>
        <SlidersHorizontal size={15} className="text-gray-400" />
      </div>
      
      {/* Category */}
      <div className="space-y-3">
        <h3 className="text-[10px] font-semibold text-gray-400 uppercase tracking-widest">Category</h3>
        <div className="space-y-1">
          {["", ...categories].map((cat) => (
            <label key={cat} className="flex items-center gap-2.5 cursor-pointer group py-1">
              <input
                type="radio"
                name="category"
                checked={filters.category === cat}
                onChange={() => handleChange("category", cat)}
                className="w-3.5 h-3.5 accent-black border-gray-300"
              />
              <span className={`text-sm transition-colors ${filters.category === cat ? "text-black font-semibold" : "text-gray-500 group-hover:text-black"}`}>
                {cat || "All"}
              </span>
            </label>
          ))}
        </div>
      </div>

      {/* Sizes */}
      <div className="space-y-3">
        <h3 className="text-[10px] font-semibold text-gray-400 uppercase tracking-widest">Size</h3>
        <div className="flex flex-wrap gap-1.5">
          {sizes.map((opt) => (
            <button
              key={opt}
              onClick={() => handleChange("size", filters.size === opt ? "" : opt)}
              className={`w-9 h-9 flex items-center justify-center rounded-lg border text-xs font-medium transition-all ${filters.size === opt ? "bg-black text-white border-black" : "border-gray-200 text-gray-600 hover:border-gray-400"}`}
            >
              {opt}
            </button>
          ))}
        </div>
      </div>

      {/* Colors */}
      <div className="space-y-3">
        <h3 className="text-[10px] font-semibold text-gray-400 uppercase tracking-widest">Color</h3>
        <div className="grid grid-cols-5 gap-2">
          {colors.map((c) => (
            <button
              key={c}
              onClick={() => handleChange("color", filters.color === c ? "" : c)}
              title={c}
              className={`w-7 h-7 rounded-full border-2 transition-all hover:scale-110 ${filters.color === c ? "border-black scale-110" : "border-transparent"}`}
              style={{ backgroundColor: c.toLowerCase() }}
            />
          ))}
        </div>
      </div>

      {/* Price */}
      <div className="space-y-3">
        <h3 className="text-[10px] font-semibold text-gray-400 uppercase tracking-widest">Price</h3>
        <div className="grid grid-cols-2 gap-2">
          <input
            type="number"
            placeholder="Min"
            className="bg-gray-50 border border-gray-200 rounded-xl px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-black/10 w-full"
            onChange={(e) => handleChange("min_price", e.target.value)}
          />
          <input
            type="number"
            placeholder="Max"
            className="bg-gray-50 border border-gray-200 rounded-xl px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-black/10 w-full"
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

  const categoryCache = useRef({});

  const fetchProducts = async (filters = {}) => {
    // Determine the category to fetch/cache based on filters or initialCategory
    const cat = filters.category !== undefined ? filters.category : (initialCategory || "");
    const cacheKey = cat || "all";
    
    // Use cache if no complex filters are applied and it exists
    const hasComplexFilters = !!(filters.size || filters.color || filters.min_price || filters.max_price || filters.search);
    if (!hasComplexFilters && categoryCache.current[cacheKey]) {
      setProducts(categoryCache.current[cacheKey]);
      setLoading(false);
      return;
    }

    setLoading(true);
    try {
      const queryParams = new URLSearchParams({
        domain: domain || window.location.hostname,
        price_key: priceKey || "price_b2c",
        category: cat,
        ...filters
      });
      const response = await fetch(`${import.meta.env.VITE_API_URL}/api/products/?${queryParams}`, {
        headers: { 'Cache-Control': 'max-age=300' }
      });
      if (!response.ok) throw new Error("Our shop is currently restyling. Please try again later.");
      const data = await response.json();
      
      // Save to cache if no complex filters
      if (!hasComplexFilters) {
        categoryCache.current[cacheKey] = data;
      }
      setProducts(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchProducts();
    
    // Prefetch neighboring categories silently
    const prefetchCategories = ['Men', 'Women', 'Ethnic', 'Kids'];
    prefetchCategories.forEach(cat => {
      if (cat !== initialCategory && !categoryCache.current[cat]) {
        const queryParams = new URLSearchParams({
          domain: domain || window.location.hostname,
          price_key: priceKey || "price_b2c",
          category: cat
        });
        fetch(`${import.meta.env.VITE_API_URL}/api/products/?${queryParams}`)
          .then(r => r.json())
          .then(data => { categoryCache.current[cat] = data; })
          .catch(() => {});
      }
    });
  }, [domain, priceKey, initialCategory]);

  const handleFilter = (filters) => {
    fetchProducts(filters);
  };

  const handleSearch = (e) => {
    e.preventDefault();
    fetchProducts({ search });
  };

  return (
    <div className="bg-white min-h-screen">
      {/* Page Header */}
      <div className="border-b border-gray-100 py-10">
        <div className="max-w-7xl mx-auto px-6">
          <h1 className="text-3xl font-black text-black tracking-tight mb-1">
            {initialCategory || "All Collections"}
          </h1>
          <p className="text-sm text-gray-400">
            {products.length > 0 ? `${products.length} products` : "Curated pieces for every occasion"}
          </p>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-6 flex gap-8 py-10">
        {/* Sidebar */}
        <Filters onFilter={handleFilter} />

        {/* Main */}
        <div className="flex-1 min-w-0">
          {/* Toolbar */}
          <div className="flex items-center justify-between mb-6 gap-4">
            <form onSubmit={handleSearch} className="relative flex-1 max-w-sm">
              <input
                type="text"
                placeholder="Search products..."
                className="w-full bg-gray-50 border border-gray-200 rounded-xl py-2.5 pl-9 pr-4 text-sm text-gray-700 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-black/10 focus:border-gray-400 transition-all"
                value={search}
                onChange={(e) => setSearch(e.target.value)}
              />
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" size={15} />
            </form>
            <select className="border border-gray-200 rounded-xl px-4 py-2.5 text-sm text-gray-600 bg-white focus:outline-none focus:ring-2 focus:ring-black/10 cursor-pointer">
              <option>Latest</option>
              <option>Price: Low to High</option>
              <option>Price: High to Low</option>
            </select>
          </div>

          {loading ? (
            <div className="grid grid-cols-2 xl:grid-cols-3 gap-4 sm:gap-6">
              {[...Array(9)].map((_, i) => (
                <div key={i} className="animate-pulse bg-gray-100 rounded-2xl h-[380px] w-full" />
              ))}
            </div>
          ) : error ? (
            <div className="text-center py-24 border border-dashed border-gray-200 rounded-2xl">
              <PackageX size={36} className="mx-auto text-gray-300 mb-4" />
              <h3 className="text-base font-semibold text-gray-700 mb-2">Something went wrong</h3>
              <p className="text-sm text-gray-400 mb-6">{error}</p>
              <button
                onClick={() => fetchProducts()}
                className="px-6 py-2.5 bg-black text-white text-sm font-semibold rounded-xl hover:bg-gray-800 transition active:scale-95"
              >
                Try Again
              </button>
            </div>
          ) : products.length === 0 ? (
            <div className="flex flex-col items-center justify-center py-32 gap-4">
              <Search size={36} className="text-gray-200" />
              <p className="text-sm text-gray-400">No products found. Try different filters.</p>
            </div>
          ) : (
            <div className="grid grid-cols-2 xl:grid-cols-3 gap-4 sm:gap-6">
              {products.map((product) => (
                <ProductCard key={product.id} product={product} />
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default ProductListPage;