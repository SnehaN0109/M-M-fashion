import { useState } from "react";
import { useLocation } from "react-router-dom";
import ProductCard from "../components/ProductCard";
import Filters from "../components/Filters";

const SearchResultsPage = () => {

  /* ===== Get Search Query from URL ===== */
  const location = useLocation();
  const query = new URLSearchParams(location.search).get("query") || "";

  /* ===== Product Data ===== */
  const [products] = useState([
    {
      id: 1,
      name: "Red Garba Dress",
      price: 1499,
      image: "https://via.placeholder.com/300",
      sizes: ["S", "M", "L"],
      colors: ["Red", "Blue"],
    },
    {
      id: 2,
      name: "Blue Ethnic Kurti",
      price: 899,
      image: "https://via.placeholder.com/300",
      sizes: ["M", "L"],
      colors: ["Blue", "Green"],
    },
    {
      id: 3,
      name: "Green Lehenga",
      price: 2999,
      image: "https://via.placeholder.com/300",
      sizes: ["S", "M", "L", "XL"],
      colors: ["Green", "Yellow"],
    },
  ]);

  /* ===== Filter Products Based on Search Query ===== */
  const filteredProducts = products.filter((product) =>
    product.name.toLowerCase().includes(query.toLowerCase())
  );

  return (
    <div className="max-w-7xl mx-auto px-6 py-10">
      
      {/* ===== Title ===== */}
      <h1 className="text-3xl font-bold mb-6">
        Search Results {query && `for "${query}"`}
      </h1>

      <div className="flex flex-col md:flex-row gap-6">
        
        {/* ===== Filters Sidebar ===== */}
        <div className="md:w-1/4">
          <Filters />
        </div>

        {/* ===== Product Grid ===== */}
        <div className="md:w-3/4 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredProducts.length > 0 ? (
            filteredProducts.map((product) => (
              <ProductCard key={product.id} product={product} />
            ))
          ) : (
            <p className="col-span-full text-center text-gray-500">
              No products found.
            </p>
          )}
        </div>

      </div>
    </div>
  );
};

export default SearchResultsPage;