import { useNavigate } from "react-router-dom";
import { useContext, useState } from "react";
import { FaHeart, FaRegHeart } from "react-icons/fa";
import { WishlistContext } from "../context/WishlistContext";
import { CartContext } from "../context/CartContext";

const ProductCard = ({ product }) => {
  const navigate = useNavigate();
  const { wishlist, addToWishlist, removeFromWishlist } = useContext(WishlistContext);
  const { addToCart } = useContext(CartContext);
  const [showMessage, setShowMessage] = useState(false);
  const [cartToast, setCartToast] = useState(null); // "added" | "already" | null

  const isLiked = wishlist.some((item) => item.id === product.id);

  const handleLike = (e) => {
    e.stopPropagation();
    if (isLiked) {
      removeFromWishlist(product.id);
    } else {
      addToWishlist(product);
      setCartToast(null); // ensure wishlist toast shows
      setShowMessage(true);
      setTimeout(() => setShowMessage(false), 2000);
    }
  };

  const firstVariant = product.variants?.[0];
  const lowStock = product.variants?.some(v => v.low_stock);
  const uniqueSizes = [...new Set(product.variants?.map(v => v.size))];
  const uniqueColors = [...new Set(product.variants?.map(v => v.color))];

  return (
    <>
      <div
        onClick={() => navigate(`/product/${product.id}`)}
        className="group relative bg-white rounded-2xl overflow-hidden border border-gray-100 hover:border-gray-200 hover:shadow-[0_8px_40px_rgba(0,0,0,0.10)] transition-all duration-400 cursor-pointer"
        data-aos="fade-up"
      >
        {/* Wishlist */}
        <button
          onClick={handleLike}
          className="absolute top-3 right-3 z-20 w-9 h-9 rounded-full bg-white shadow-sm border border-gray-100 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-all duration-200 hover:scale-110 active:scale-95"
        >
          {isLiked ? (
            <FaHeart className="text-black text-sm" />
          ) : (
            <FaRegHeart className="text-gray-400 text-sm" />
          )}
        </button>

        {/* Low Stock Badge */}
        {lowStock && (
          <div className="absolute top-3 left-3 z-20">
            <span className="bg-black text-white text-[9px] font-semibold px-2.5 py-1 rounded-full tracking-wide">
              Low Stock
            </span>
          </div>
        )}

        {/* Image */}
        <div className="h-[280px] overflow-hidden bg-gray-50 relative">
          {(() => {
            const raw = product.images?.[0] || product.image_url || "";
            const src = raw.startsWith("http")
              ? raw
              : raw
              ? `${import.meta.env.VITE_API_URL}${raw}`
              : "https://via.placeholder.com/300x400?text=Product";
            return (
              <img
                src={src}
                alt={product.name}
                loading="lazy"
                className="w-full h-full object-cover transition-transform duration-700 group-hover:scale-108"
                style={{ '--tw-scale-x': 'var(--scale)', '--tw-scale-y': 'var(--scale)' }}
                onError={(e) => {
                  e.target.onerror = null;
                  e.target.src = "https://via.placeholder.com/300x400?text=No+Image";
                }}
              />
            );
          })()}
          {/* Overlay with quick view */}
          <div className="absolute inset-0 bg-black/0 group-hover:bg-black/5 transition-all duration-300" />
          <div className="absolute bottom-0 left-0 right-0 p-3 translate-y-full group-hover:translate-y-0 transition-transform duration-300">
            <div className="bg-white text-black text-xs font-semibold py-2.5 rounded-xl text-center shadow-lg tracking-wide">
              Quick View
            </div>
          </div>
        </div>

        {/* Content */}
        <div className="p-4">
          <div className="flex items-center justify-between mb-1.5">
            <span className="text-[10px] font-semibold text-gray-400 uppercase tracking-widest">
              {product.category}
            </span>
            <span className="text-[10px] text-gray-300">
              {product.variants?.length} variants
            </span>
          </div>

          <h3 className="text-sm font-semibold text-gray-900 truncate mb-2 group-hover:text-black transition-colors leading-snug">
            {product.name}
          </h3>

          {/* Sizes */}
          <div className="flex flex-wrap gap-1 mb-3">
            {uniqueSizes.slice(0, 4).map(s => (
              <span key={s} className="text-[9px] font-medium px-1.5 py-0.5 bg-gray-100 text-gray-500 rounded-md">
                {s}
              </span>
            ))}
            {uniqueSizes.length > 4 && <span className="text-[9px] text-gray-400">+{uniqueSizes.length - 4}</span>}
          </div>

          <div className="flex items-center justify-between pt-3 border-t border-gray-50">
            <div>
              <p className="text-[10px] text-gray-400 mb-0.5">From</p>
              <p className="text-lg font-bold text-black">
                ₹{firstVariant?.price?.toLocaleString() || 0}
              </p>
            </div>

            {/* Quick Add */}
            <button
              onClick={async (e) => {
                e.stopPropagation();
                const inStock = product.variants?.find(v => v.quantity > 0);
                const firstVar = inStock || product.variants?.[0];
                if (firstVar) {
                  const result = await addToCart({ ...product, activeVariant: firstVar, price: firstVar.price, cartQuantity: 1 });
                  setShowMessage(true);
                  setCartToast(result?.duplicate ? "already" : "added");
                  setTimeout(() => { setShowMessage(false); setCartToast(null); }, 2000);
                }
              }}
              className="w-9 h-9 bg-black text-white rounded-xl flex items-center justify-center hover:bg-gray-800 transition-all duration-200 active:scale-90 shadow-sm"
            >
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round"><circle cx="8" cy="21" r="1"/><circle cx="19" cy="21" r="1"/><path d="M2.05 2.05h2l2.66 12.42a2 2 0 0 0 2 1.58h9.78a2 2 0 0 0 1.95-1.57l1.65-7.43H5.12"/></svg>
            </button>
          </div>
        </div>
      </div>

      {/* Toast */}
      {showMessage && (
        <div className="fixed top-6 left-1/2 -translate-x-1/2 z-[60]">
          {cartToast === "added" ? (
            <div className="bg-black text-white px-6 py-3 rounded-2xl shadow-2xl flex items-center gap-2.5 text-sm font-medium">
              <svg xmlns="http://www.w3.org/2000/svg" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5"><path d="M20 6L9 17l-5-5"/></svg>
              Added to cart
            </div>
          ) : cartToast === "already" ? (
            <div className="bg-gray-700 text-white px-6 py-3 rounded-2xl shadow-2xl flex items-center gap-2.5 text-sm font-medium">
              Already in cart
            </div>
          ) : (
            <div className="bg-black text-white px-6 py-3 rounded-2xl shadow-2xl flex items-center gap-2.5 text-sm font-medium">
              <FaHeart className="text-white" />
              Saved to wishlist
            </div>
          )}
        </div>
      )}
    </>
  );
};

export default ProductCard;