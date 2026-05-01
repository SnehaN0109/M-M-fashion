import React, { useState } from "react";
import { SlidersHorizontal } from "lucide-react";

const Filters = ({ onFilter }) => {
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

export default Filters;