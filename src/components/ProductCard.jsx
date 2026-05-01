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

  const isLiked = wishlist.some((item) => item.id === product.id);

  const handleLike = (e) => {
    e.stopPropagation();
    if (isLiked) {
      removeFromWishlist(product.id);
    } else {
      addToWishlist(product);
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
        className="group relative bg-white rounded-2xl overflow-hidden border border-gray-100 shadow-sm hover:shadow-xl transition-all duration-300 transform hover:-translate-y-1 cursor-pointer"
      >
        {/* Liked / Wishlist */}
        <button
          onClick={handleLike}
          className="absolute top-4 right-4 z-20 p-2.5 rounded-full bg-white/80 backdrop-blur-md shadow-sm opacity-0 group-hover:opacity-100 transition-all duration-300"
        >
          {isLiked ? (
            <FaHeart className="text-pink-600 text-lg" />
          ) : (
            <FaRegHeart className="text-gray-400 text-lg hover:text-pink-500" />
          )}
        </button>

        {/* Low Stock Badge */}
        {lowStock && (
          <div className="absolute top-4 left-4 z-20">
            <span className="bg-red-600/90 backdrop-blur-sm text-white text-[10px] font-black px-2.5 py-1 rounded-md shadow-lg animate-pulse">
              ONLY FEW LEFT
            </span>
          </div>
        )}

        {/* Media Container */}
        <div className="h-[300px] overflow-hidden bg-gray-50 relative rounded-t-2xl">
          <img
            src={product.images?.[0] || product.image_url || "https://via.placeholder.com/300x400?text=Product"}
            alt={product.name}
            className="w-full h-full object-cover transition-transform duration-700 group-hover:scale-110"
            onError={(e) => {
              e.target.onerror = null;
              e.target.src = "https://via.placeholder.com/300x400?text=No+Image";
            }}
          />
          {/* Glass Overlay on hover */}
          <div className="absolute inset-0 bg-gradient-to-t from-black/40 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
          
          {/* Quick View hint */}
          <div className="absolute bottom-4 left-0 right-0 flex justify-center translate-y-4 group-hover:translate-y-0 transition-transform duration-300">
             <span className="bg-white/95 text-gray-900 text-xs font-bold px-6 py-2.5 rounded-full shadow-xl uppercase tracking-tighter">
               View Details
             </span>
          </div>
        </div>

        {/* Content */}
        <div className="p-5">
          <div className="flex justify-between items-start mb-1">
             <span className="text-[10px] font-bold text-pink-600 tracking-widest uppercase">
               {product.category}
             </span>
             <span className="text-[10px] font-bold text-gray-400">
               {product.variants?.length} VARIANTS
             </span>
          </div>
          
          <h3 className="text-lg font-bold text-gray-900 truncate mb-2 group-hover:text-pink-600 transition-colors">
            {product.name}
          </h3>

          {/* Sizes & Colors Summary */}
          <div className="flex flex-wrap gap-1 mb-4">
             {uniqueSizes.slice(0, 4).map(s => (
               <span key={s} className="text-[9px] font-bold px-1.5 py-0.5 bg-gray-100 text-gray-500 rounded uppercase">
                 {s}
               </span>
             ))}
             {uniqueSizes.length > 4 && <span className="text-[9px] text-gray-400">+{uniqueSizes.length - 4}</span>}
          </div>

          <div className="flex justify-between items-end border-t border-gray-50 pt-4">
            <div>
               <p className="text-[10px] text-gray-400 font-bold uppercase tracking-tight">Price from</p>
               <p className="text-2xl font-black text-gray-900 tracking-tight">
                 ₹{firstVariant?.price?.toLocaleString() || 0}
               </p>
            </div>
            
            {/* Quick Add Button */}
            <button
               onClick={(e) => {
                 e.stopPropagation();
                 const firstVar = product.variants?.[0];
                 if (firstVar) {
                   addToCart({ ...product, activeVariant: firstVar, price: firstVar.price });
                   setShowMessage(true);
                   setTimeout(() => setShowMessage(false), 2000);
                 }
               }}
               className="bg-pink-600 text-white p-3 rounded-xl shadow-lg hover:bg-black transition-all active:scale-90 flex items-center justify-center"
            >
               <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round"><circle cx="8" cy="21" r="1"/><circle cx="19" cy="21" r="1"/><path d="M2.05 2.05h2l2.66 12.42a2 2 0 0 0 2 1.58h9.78a2 2 0 0 0 1.95-1.57l1.65-7.43H5.12"/></svg>
            </button>
          </div>
        </div>
      </div>

      {/* Persistence Notification */}
      {showMessage && (
        <div className="fixed top-12 left-1/2 -translate-x-1/2 z-[60] animate-bounce">
           <div className="bg-gray-900 text-white px-8 py-3 rounded-2xl shadow-2xl flex items-center gap-3">
             <FaHeart className="text-pink-500" />
             <span className="font-bold text-sm tracking-tight">Saved to wish list</span>
           </div>
        </div>
      )}
    </>
  );
};

export default ProductCard;