import React, { useState, useEffect, useContext } from "react";
import { useParams, Link } from "react-router-dom";
import { 
  ShoppingCart, 
  Heart, 
  Upload, 
  Play, 
  ChevronRight, 
  Check, 
  AlertTriangle,
  Loader2,
  Share2,
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

  const fetchProduct = async () => {
    setLoading(true);
    try {
      const currentDomain = domain || window.location.hostname;
      const response = await fetch(`http://localhost:5000/api/products/${id}?domain=${currentDomain}`);
      if (!response.ok) throw new Error("This piece is currently unavailable.");
      const data = await response.json();
      setProduct(data);
      if (data.image_url) setSelectedImage(data.image_url);
      if (data.variants?.length > 0) setSelectedColor(data.variants[0].color);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchProduct();
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
          Explore Other Labels
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
    if (!activeVariant || quantity > activeVariant.quantity) return alert("Selected style is out of stock.");
    
    addToCart({ ...product, activeVariant, cartQuantity: quantity, price: activeVariant.price });
    alert("Added to your collection!");
  };

  return (
    <div className="bg-white min-h-screen font-sans">
      <div className="max-w-7xl mx-auto px-6 py-10">
        
        {/* Modern Breadcrumb */}
        <nav className="flex items-center gap-2 mb-10 text-[10px] font-black uppercase tracking-widest text-gray-400">
          <Link to="/" className="hover:text-pink-600 transition-colors">Home</Link>
          <ChevronRight size={12} />
          <Link to="/products" className="hover:text-pink-600 transition-colors">Boutique</Link>
          <ChevronRight size={12} />
          <span className="text-gray-900">{product.name}</span>
        </nav>

        <div className="grid lg:grid-cols-2 gap-16 items-start">
          
          {/* MEDIA GALLERY: Modern Stacked Layout */}
          <div className="space-y-6">
            <div className="relative group aspect-[3/4] bg-gray-50 rounded-[40px] overflow-hidden shadow-2xl">
              {showVideo && product.video_url ? (
                <video src={product.video_url} autoPlay loop muted className="w-full h-full object-cover" />
              ) : (
                <img src={selectedImage || product.image_url} alt={product.name} className="w-full h-full object-cover" />
              )}
              
              {/* Floating Badge */}
              <div className="absolute top-8 left-8 bg-white/95 backdrop-blur-md px-4 py-2 rounded-full shadow-lg border border-gray-100 flex items-center gap-2">
                 <div className="w-2 h-2 rounded-full bg-pink-600 animate-pulse" />
                 <span className="text-[10px] font-black text-gray-900 uppercase">Premium Selection</span>
              </div>
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
                  <div className="w-10 h-10 rounded-full bg-white flex items-center justify-center shadow-md">
                     <Play size={20} className="text-pink-600 ml-0.5" />
                  </div>
                  <span className="text-[10px] font-black text-gray-900 uppercase">Video View</span>
                </button>
              )}
            </div>
          </div>

          {/* PRODUCT INFO: Elegant & Spaced */}
          <div className="flex flex-col py-4">
            <div className="space-y-2 mb-8">
              <span className="text-sm font-black text-pink-600 uppercase tracking-[0.2em]">{product.category}</span>
              <h1 className="text-5xl font-black text-gray-900 tracking-tighter leading-none">{product.name}</h1>
            </div>
            
            {/* Price section */}
            <div className="mb-12">
               <div className="flex items-baseline gap-4">
                  <span className="text-6xl font-black text-gray-900 tracking-tighter">₹{displayPrice.toLocaleString()}</span>
                  <span className="text-sm font-bold text-gray-400 uppercase tracking-widest">Tax Included</span>
               </div>
               <div className="mt-4 flex gap-4">
                  <div className="flex items-center gap-2 text-[10px] font-bold text-green-600 bg-green-50 px-3 py-1.5 rounded-full border border-green-100">
                    <Check size={14} /> EXPRESS SHIPPING AVAILABLE
                  </div>
               </div>
            </div>

            {/* Selection Engine */}
            <div className="space-y-10">
              {/* Colors */}
              <div className="space-y-4">
                <div className="flex justify-between items-center">
                   <h3 className="text-xs font-black text-gray-400 uppercase tracking-widest">Select Shade</h3>
                   <span className="text-xs font-bold text-gray-900">{selectedColor}</span>
                </div>
                <div className="flex gap-4">
                  {availableColors.map(c => (
                    <button 
                      key={c} 
                      onClick={() => { setSelectedColor(c); setSelectedSize(null); }} 
                      className={`group relative w-12 h-12 rounded-full border-2 transition-all p-1 ${selectedColor === c ? "border-gray-900" : "border-transparent hover:scale-110"}`}
                    >
                      <div className="w-full h-full rounded-full shadow-inner shadow-black/10" style={{ backgroundColor: c.toLowerCase() }} />
                      {selectedColor === c && (
                        <div className="absolute -top-1 -right-1 w-4 h-4 bg-gray-900 rounded-full flex items-center justify-center text-white border-2 border-white">
                          <Check size={10} strokeWidth={4} />
                        </div>
                      )}
                    </button>
                  ))}
                </div>
              </div>

              {/* Sizes */}
              <div className="space-y-4">
                <div className="flex justify-between items-center">
                   <h3 className="text-xs font-black text-gray-400 uppercase tracking-widest">Choose Size</h3>
                   <button className="text-[10px] font-black text-pink-600 uppercase tracking-widest underline underline-offset-4 hover:text-pink-700 transition-colors">Size Guide</button>
                </div>
                <div className="grid grid-cols-4 sm:grid-cols-6 gap-3">
                  {sizeOptionsForColor.map(v => (
                    <button 
                      key={v.size} 
                      disabled={v.quantity === 0}
                      onClick={() => setSelectedSize(v.size)} 
                      className={`h-14 rounded-2xl flex items-center justify-center text-sm font-black transition-all duration-300 relative ${
                        v.quantity === 0 ? "bg-gray-50 border border-gray-100 text-gray-300 cursor-not-allowed opacity-50" : 
                        selectedSize === v.size ? "bg-gray-900 text-white border-gray-900 shadow-xl scale-105" : "bg-white border border-gray-100 text-gray-600 hover:border-pink-300"
                      }`}
                    >
                      {v.size}
                      {v.low_stock && !selectedSize && <div className="absolute -top-1.5 -right-1.5 w-3 h-3 bg-red-500 rounded-full border-2 border-white animate-pulse" />}
                    </button>
                  ))}
                </div>
                {activeVariant?.low_stock && (
                   <div className="flex items-center gap-2 text-red-600 bg-red-50 p-4 rounded-2xl border border-red-100">
                     <AlertTriangle size={18} />
                     <p className="text-xs font-bold uppercase tracking-tight">Only {activeVariant.quantity} pieces remaining. Order soon!</p>
                   </div>
                )}
              </div>
            </div>

            {/* Modern Cart Actions */}
            <div className="mt-16 flex gap-4">
              <div className="bg-gray-100 rounded-3xl flex items-center p-1 border border-gray-200">
                <button className="w-12 h-14 font-black flex items-center justify-center hover:bg-white rounded-2xl transition" onClick={() => setQuantity(q => Math.max(1, q-1))}>-</button>
                <div className="w-10 text-center font-black text-lg">{quantity}</div>
                <button className="w-12 h-14 font-black flex items-center justify-center hover:bg-white rounded-2xl transition" onClick={() => setQuantity(q => q+1)}>+</button>
              </div>
              
              <button 
                onClick={handleAddToCart}
                className="flex-1 bg-pink-600 hover:bg-pink-700 text-white font-black text-lg rounded-[40px] py-6 shadow-2xl active:scale-95 transition-all flex items-center justify-center gap-4 relative overflow-hidden group"
              >
                <div className="absolute inset-x-0 bottom-0 top-full bg-black/10 group-hover:top-0 transition-all duration-300" />
                <ShoppingCart size={24} />
                <span className="relative z-10 uppercase tracking-tighter">Acquire This Item</span>
              </button>
              
              <button className="w-20 h-20 bg-white border border-gray-100 rounded-full flex items-center justify-center text-gray-400 hover:text-pink-600 hover:border-pink-100 hover:shadow-xl transition-all active:scale-90">
                <Heart size={28} />
              </button>
            </div>

            {/* Info Table */}
            <div className="mt-16 grid grid-cols-2 gap-8 border-t border-gray-100 pt-10">
               <div className="space-y-1">
                 <p className="text-[10px] font-black text-gray-400 uppercase tracking-widest">SKU Label</p>
                 <p className="text-sm font-bold text-gray-900 tracking-tight">MMF- Boutique-{product.id}</p>
               </div>
               <div className="space-y-1">
                 <p className="text-[10px] font-black text-gray-400 uppercase tracking-widest">Materiality</p>
                 <p className="text-sm font-bold text-gray-900 tracking-tight">Premium Heritage Fabric</p>
               </div>
            </div>

          </div>
        </div>
        
        {/* Description Section with Modern Typography */}
        <div className="mt-32 max-w-4xl">
          <h2 className="text-xs font-black text-gray-400 uppercase tracking-[0.4em] mb-10">Product Narrative</h2>
          <div className="prose prose-pink max-w-none">
             <p className="text-2xl font-medium text-gray-600 leading-relaxed tracking-tight">
               {product.description}
             </p>
          </div>
        </div>

      </div>
    </div>
  );
};

export default ProductDetailPage;