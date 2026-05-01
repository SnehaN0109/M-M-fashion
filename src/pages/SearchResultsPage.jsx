import { useState, useEffect } from "react";
import { useLocation } from "react-router-dom";
import ProductCard from "../components/ProductCard";
import Filters from "../components/Filters";
import { Loader2, SearchX } from "lucide-react";
import { useDomain } from "../context/DomainContext";

const SearchResultsPage = () => {
  const location = useLocation();
  const query = new URLSearchParams(location.search).get("query") || "";
  const { domain, priceKey } = useDomain();

  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  // Filter state
  const [filters, setFilters] = useState({ size: "", color: "", min_price: "", max_price: "" });

  useEffect(() => {
    if (!query.trim()) { setProducts([]); return; }
    const controller = new AbortController();
    setLoading(true);
    setError("");

    const params = new URLSearchParams({ search: query });
    if (domain) params.set("domain", domain);
    if (priceKey) params.set("price_key", priceKey);
    if (filters.size) params.set("size", filters.size);
    if (filters.color) params.set("color", filters.color);
    if (filters.min_price) params.set("min_price", filters.min_price);
    if (filters.max_price) params.set("max_price", filters.max_price);

    fetch(`${import.meta.env.VITE_API_URL}/api/products/?${params.toString()}`, { signal: controller.signal })
      .then((r) => r.json())
      .then((data) => {
        if (Array.isArray(data)) setProducts(data);
        else setError("Failed to load results.");
      })
      .catch((e) => { if (e.name !== "AbortError") setError("Could not connect to server."); })
      .finally(() => setLoading(false));

    return () => controller.abort();
  }, [query, domain, priceKey, filters]);

  return (
    <div className="max-w-7xl mx-auto px-6 py-10">
      <h1 className="text-3xl font-black mb-2">
        {query ? `Results for "${query}"` : "Search Products"}
      </h1>
      {!loading && products.length > 0 && (
        <p className="text-sm text-gray-400 mb-6">{products.length} product{products.length > 1 ? "s" : ""} found</p>
      )}

      <div className="flex flex-col md:flex-row gap-8">
        {/* Filters */}
        <div className="md:w-1/4">
          <Filters onFilterChange={setFilters} />
        </div>

        {/* Results */}
        <div className="md:w-3/4">
          {loading ? (
            <div className="flex items-center justify-center py-20">
              <Loader2 className="w-10 h-10 text-pink-600 animate-spin" />
            </div>
          ) : error ? (
            <div className="text-center py-20 text-red-500 font-bold">{error}</div>
          ) : products.length === 0 ? (
            <div className="flex flex-col items-center justify-center py-20 gap-4 text-center">
              <SearchX size={48} className="text-gray-200" />
              <p className="text-xl font-black text-gray-400">No products found</p>
              {query && <p className="text-sm text-gray-400">Try a different search term or adjust filters</p>}
            </div>
          ) : (
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
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

export default SearchResultsPage;
