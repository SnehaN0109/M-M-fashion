const Filters = ({ onFilterChange, sizes = [], colors = [] }) => {

  const priceRanges = ["2000", "3000", "4000"];

  return (
    <div className="space-y-4">
      <h3 className="font-semibold">Filters</h3>

      {/* Size */}
      <select
        className="w-full border p-2 rounded"
        onChange={(e) => onFilterChange("size", e.target.value)}
      >
        <option value="">All Sizes</option>
        {sizes.map((size, index) => (
          <option key={index} value={size}>{size}</option>
        ))}
      </select>

      {/* Color */}
      <select
        className="w-full border p-2 rounded"
        onChange={(e) => onFilterChange("color", e.target.value)}
      >
        <option value="">All Colors</option>
        {colors.map((color, index) => (
          <option key={index} value={color}>{color}</option>
        ))}
      </select>

      {/* Price */}
      <select
        className="w-full border p-2 rounded"
        onChange={(e) => onFilterChange("price", e.target.value)}
      >
        <option value="">All Prices</option>
        {priceRanges.map((price, index) => (
          <option key={index} value={price}>
            Under ₹{price}
          </option>
        ))}
      </select>

    </div>
  );
};

export default Filters;