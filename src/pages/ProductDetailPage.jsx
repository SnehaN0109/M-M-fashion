import React, { useState, useEffect, useContext } from "react";
import { useParams, Link } from "react-router-dom";
import { fetchProductById } from "../services/api";
import { 
  ShoppingCart, 
  Heart, 
  Play, 
  ChevronRight, 
  Check, 
  AlertTriangle,
  Loader2,
  Info
} from "lucide-react";
import { useDomain } from "../context/DomainContext";
import { CartContext } from "../context/CartContext";

const ProductDetailPage = () => {
  const { id } = useParams();
  const { domain } = useDomain();
  const { addToCart } = useContext(CartContext);

  const [product, setProduct] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const [selectedImage, setSelectedImage] = useState(null);
  const [selectedColor, setSelectedColor] = useState(null);
  const [selectedSize, setSelectedSize] = useState(null);
  const [quantity, setQuantity] = useState(1);
  const [showVideo, setShowVideo] = useState(false);

  const loadProduct = async () => {
    setLoading(true);
    try {
      const data = await fetchProductById(id);
      setProduct(data);
      if (data.image_url) setSelectedImage(data.image_url);
      if (data.variants?.length > 0) setSelectedColor(data.variants[0].color);
      setError(null);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadProduct();
  }, [id, domain]);

  if (loading) return (
    <div className="min-h-screen bg-white flex flex-col items-center justify-center space-y-4">
      <Loader2 className="w-12 h-12 text-pink-600 animate-spin" />
      <p className="text-xs font-black text-gray-400 uppercase tracking-widest">Unveiling Style...</p>
    </div>
  );

  if (error) return (
    <div className="min-h-screen bg-white flex items-center justify-center p-6">
      <div className="max-w-md w-full text-center space-y-6">
        <div className="w-20 h-20 bg-gray-50 rounded-full flex items-center justify-center mx-auto text-gray-300">
           <Info size={40} />
        </div>
        <h2 className="text-3xl font-black text-gray-900 tracking-tighter">{error}</h2>
        <Link to="/products" className="inline-block px-10 py-4 bg-gray-900 text-white font-bold rounded-2xl shadow-xl hover:bg-black transition active:scale-95">
          Explore Boutique
        </Link>
      </div>
    </div>
  );

  if (!product) return null;

  const availableColors = [...new Set(product.variants.map(v => v.color))];
  const sizeOptionsForColor = product.variants.filter(v => v.color === selectedColor);
  const activeVariant = product.variants.find(v => v.color === selectedColor && v.size === selectedSize);
  const displayPrice = activeVariant ? activeVariant.price : (sizeOptionsForColor[0]?.price || 0);

  const handleAddToCart = () => {
    if (!selectedSize) return alert("Please select your size.");
    if (!activeVariant || quantity > activeVariant.quantity) return alert("Style out of stock.");
    
    addToCart({ ...product, activeVariant, cartQuantity: quantity, price: activeVariant.price });
    alert("Added to collection!");
  };

  return (
    <div className="bg-white min-h-screen font-sans">
      <div className="max-w-7xl mx-auto px-6 py-10">
        <nav className="flex items-center gap-2 mb-10 text-[10px] font-black uppercase tracking-widest text-gray-400">
          <Link to="/" className="hover:text-pink-600 transition-colors">Home</Link>
          <ChevronRight size={12} />
          <Link to="/products" className="hover:text-pink-600 transition-colors">Boutique</Link>
          <ChevronRight size={12} />
          <span className="text-gray-900">{product.name}</span>
        </nav>

        <div className="grid lg:grid-cols-2 gap-16 items-start">
          <div className="space-y-6">
            <div className="relative group aspect-[3/4] bg-gray-50 rounded-[40px] overflow-hidden shadow-2xl">
              {showVideo && product.video_url ? (
                <video src={product.video_url} autoPlay loop muted className="w-full h-full object-cover" />
              ) : (
                <img src={selectedImage || product.image_url} alt={product.name} className="w-full h-full object-cover" />
              )}
            </div>
            
            <div className="flex gap-4 scrollbar-hide overflow-x-auto pt-2">
              <button 
                onClick={() => {setSelectedImage(product.image_url); setShowVideo(false);}}
                className={`w-28 h-36 rounded-2xl overflow-hidden border-2 transition-all ${selectedImage === product.image_url && !showVideo ? "border-pink-600 shadow-lg scale-105" : "border-transparent opacity-60 hover:opacity-100"}`}
              >
                <img src={product.image_url} className="w-full h-full object-cover" />
              </button>
              {product.video_url && (
                <button 
                  onClick={() => setShowVideo(true)}
                  className={`w-28 h-36 rounded-2xl bg-gray-100 border-2 transition-all flex flex-col items-center justify-center gap-2 ${showVideo ? "border-pink-600 shadow-lg scale-105" : "border-transparent opacity-60 hover:opacity-100"}`}
                >
                  <Play size={24} className="text-pink-600" />
                  <span className="text-[10px] font-black text-gray-900 uppercase">Video</span>
                </button>
              )}
            </div>
          </div>

          <div className="flex flex-col py-4">
            <div className="space-y-2 mb-8">
              <span className="text-sm font-black text-pink-600 uppercase tracking-[0.2em]">{product.category}</span>
              <h1 className="text-5xl font-black text-gray-900 tracking-tighter leading-none">{product.name}</h1>
            </div>
            
            <div className="mb-12">
               <div className="flex items-baseline gap-4">
                  <span className="text-6xl font-black text-gray-900 tracking-tighter">₹{displayPrice.toLocaleString()}</span>
               </div>
            </div>

            <div className="space-y-10">
              <div className="space-y-4">
                <div className="flex justify-between items-center">
                   <h3 className="text-xs font-black text-gray-400 uppercase tracking-widest">Shade</h3>
                   <span className="text-xs font-bold text-gray-900">{selectedColor}</span>
                </div>
                <div className="flex gap-4">
                  {availableColors.map(c => (
                    <button key={c} onClick={() => { setSelectedColor(c); setSelectedSize(null); }} className={`w-10 h-10 rounded-full border-2 transition-all ${selectedColor === c ? "border-gray-900 p-0.5" : "border-transparent"}`}>
                      <div className="w-full h-full rounded-full shadow-inner" style={{ backgroundColor: c.toLowerCase() }} />
                    </button>
                  ))}
                </div>
              </div>

              <div className="space-y-4">
                <div className="flex justify-between items-center">
                   <h3 className="text-xs font-black text-gray-400 uppercase tracking-widest">Size</h3>
                </div>
                <div className="grid grid-cols-6 gap-3">
                  {sizeOptionsForColor.map(v => (
                    <button 
                      key={v.size} 
                      disabled={v.quantity === 0}
                      onClick={() => setSelectedSize(v.size)} 
                      className={`h-12 rounded-xl flex items-center justify-center text-sm font-black transition-all ${
                        v.quantity === 0 ? "bg-gray-50 text-gray-300 cursor-not-allowed" : 
                        selectedSize === v.size ? "bg-gray-900 text-white shadow-lg" : "border border-gray-100 text-gray-600 hover:border-pink-300"
                      }`}
                    >
                      {v.size}
                    </button>
                  ))}
                </div>
                {activeVariant?.low_stock && (
                   <div className="flex items-center gap-2 text-red-600 bg-red-50 p-3 rounded-xl border border-red-100">
                     <AlertTriangle size={16} />
                     <p className="text-[10px] font-black uppercase">Only {activeVariant.quantity} pieces left!</p>
                   </div>
                )}
              </div>
            </div>

            <div className="mt-16 flex gap-4">
              <div className="bg-gray-100 rounded-3xl flex items-center p-1">
                <button className="w-10 h-10 font-bold" onClick={() => setQuantity(q => Math.max(1, q-1))}>-</button>
                <div className="w-8 text-center font-bold">{quantity}</div>
                <button className="w-10 h-10 font-bold" onClick={() => setQuantity(q => q+1)}>+</button>
              </div>
              <button onClick={handleAddToCart} className="flex-1 bg-pink-600 text-white font-black rounded-[40px] py-4 shadow-xl hover:bg-pink-700 active:scale-95 transition">
                ADD TO CART
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProductDetailPage;