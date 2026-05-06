import { useState, useEffect, useContext } from "react";
import { useParams, Link } from "react-router-dom";
import {
  ShoppingCart, Heart, Play, ChevronRight, Check,
  AlertTriangle, Loader2, Info, Star, Upload, Share2
} from "lucide-react";
import { useDomain } from "../context/DomainContext";
import { CartContext } from "../context/CartContext";
import { WishlistContext } from "../context/WishlistContext";

const ProductDetailPage = () => {
  const { id } = useParams();
  const { domain, priceKey } = useDomain();
  const { addToCart, cartItems } = useContext(CartContext);
  const { wishlist, addToWishlist, removeFromWishlist } = useContext(WishlistContext);

  const [product, setProduct] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [reviews, setReviews] = useState([]);
  const [userPhotos, setUserPhotos] = useState([]);

  const [selectedImage, setSelectedImage] = useState(null);
  const [selectedColor, setSelectedColor] = useState(null);
  const [selectedSize, setSelectedSize] = useState(null);
  const [quantity, setQuantity] = useState(1);
  const [showVideo, setShowVideo] = useState(false);

  const [cartMsg, setCartMsg] = useState("");

  // Review form state
  const [reviewRating, setReviewRating] = useState(0);
  const [reviewComment, setReviewComment] = useState("");
  const [reviewSubmitting, setReviewSubmitting] = useState(false);
  const [reviewMsg, setReviewMsg] = useState("");

  const isWishlisted = wishlist.some((item) => item.id === parseInt(id));

  const fetchProduct = async () => {
    setLoading(true);
    try {
      const currentDomain = domain || window.location.hostname;
      const res = await fetch(
        `${import.meta.env.VITE_API_URL}/api/products/${id}?domain=${currentDomain}&price_key=${priceKey || "price_b2c"}`
      );
      if (!res.ok) throw new Error("This product is currently unavailable.");
      const data = await res.json();
      setProduct(data);
      if (data.image_url) setSelectedImage(data.image_url);
      if (data.variants?.length > 0) setSelectedColor(data.variants[0].color?.trim());
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const fetchReviews = async () => {
    try {
      const res = await fetch(`${import.meta.env.VITE_API_URL}/api/products/${id}/reviews`);
      if (res.ok) setReviews(await res.json());
    } catch { /* silent */ }
  };

  const fetchUserPhotos = async () => {
    try {
      const res = await fetch(`${import.meta.env.VITE_API_URL}/api/products/${id}/photos`);
      if (res.ok) setUserPhotos(await res.json());
    } catch { /* silent */ }
  };

  useEffect(() => {
    fetchProduct();
    fetchReviews();
    fetchUserPhotos();
  }, [id, domain]);

  const handleAddToCart = () => {
    if (!selectedSize) { setCartMsg("Please select a size."); return; }
    if (!activeVariant) { setCartMsg("Selected size/color combination is not available."); return; }
    if (activeVariant.quantity === 0) { setCartMsg("This variant is out of stock."); return; }
    if (quantity > activeVariant.quantity) {
      setCartMsg(`Only ${activeVariant.quantity} unit${activeVariant.quantity > 1 ? "s" : ""} available.`);
      return;
    }

    // Check if already in cart
    const alreadyInCart = cartItems?.some(
      i => i.id === product.id && i.activeVariant?.id === activeVariant.id
    );
    if (alreadyInCart) {
      setCartMsg("This item is already in your cart!");
      setTimeout(() => setCartMsg(""), 2500);
      return;
    }

    addToCart({ ...product, activeVariant, cartQuantity: quantity, price: activeVariant.price });
    setCartMsg("Added to cart!");
    setTimeout(() => setCartMsg(""), 2500);
  };

  const handleWishlist = () => {
    if (isWishlisted) removeFromWishlist(parseInt(id));
    else addToWishlist(product);
  };

  const handleWhatsAppShare = () => {
    const text = `Check out this product: ${product.name} ${window.location.href}`;
    window.open(`https://wa.me/?text=${encodeURIComponent(text)}`, "_blank");
  };

  const handleSubmitReview = async () => {
    // Validation
    if (reviewRating === 0) {
      setReviewMsg("Please select a star rating");
      return;
    }

    if (reviewComment.trim().length > 500) {
      setReviewMsg("Comment must be 500 characters or less");
      return;
    }

    const whatsapp = localStorage.getItem("whatsapp_number");
    if (!whatsapp) {
      setReviewMsg("Please login with WhatsApp to submit a review");
      return;
    }

    setReviewSubmitting(true);
    setReviewMsg("");

    try {
      const res = await fetch(`${import.meta.env.VITE_API_URL}/api/products/${id}/reviews`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          rating: reviewRating,
          comment: reviewComment.trim(),
          whatsapp_number: whatsapp
        })
      });

      const data = await res.json();

      if (!res.ok) {
        setReviewMsg(data.error || "Failed to submit review");
        return;
      }

      // Success!
      setReviewMsg("✓ Review submitted successfully!");
      setReviewRating(0);
      setReviewComment("");
      
      // Refresh reviews list
      fetchReviews();

      // Clear success message after 3 seconds
      setTimeout(() => setReviewMsg(""), 3000);
    } catch {
      setReviewMsg("Network error. Please try again.");
    } finally {
      setReviewSubmitting(false);
    }
  };

  if (loading) return (
    <div className="min-h-screen bg-white flex flex-col items-center justify-center space-y-4">
      <div className="relative">
        <div className="w-16 h-16 rounded-full border-4 border-pink-100 border-t-pink-500 animate-spin" />
      </div>
      <p className="text-xs font-semibold text-gray-400 uppercase tracking-[0.2em]">Loading product...</p>
    </div>
  );

  if (error) return (
    <div className="min-h-screen bg-white flex items-center justify-center p-6">
      <div className="max-w-md w-full text-center space-y-6">
        <Info size={48} className="mx-auto text-gray-300" />
        <h2 className="text-2xl font-black text-gray-900">{error}</h2>
        <Link to="/products" className="inline-block px-10 py-4 bg-gray-900 text-white font-bold rounded-2xl">
          Back to Products
        </Link>
      </div>
    </div>
  );

  if (!product) return null;

  const availableColors = [...new Set(product.variants.map(v => v.color?.trim()).filter(Boolean))];
  const sizeOptionsForColor = product.variants.filter(v => v.color?.trim() === selectedColor);
  const activeVariant = product.variants.find(v => v.color?.trim() === selectedColor && v.size?.trim() === selectedSize);
  const displayPrice = activeVariant ? activeVariant.price : (sizeOptionsForColor[0]?.price || 0);
  const allImages = product.images?.length > 0 ? product.images : (product.image_url ? [{ image_url: product.image_url }] : []);

  const avgRating = reviews.length > 0
    ? (reviews.reduce((s, r) => s + r.rating, 0) / reviews.length).toFixed(1)
    : null;

  return (
    <div className="bg-white min-h-screen">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 py-8">

        {/* Breadcrumb */}
        <nav className="flex items-center gap-1.5 mb-8 text-[11px] font-medium text-gray-400">
          <Link to="/" className="hover:text-pink-500 transition-colors">Home</Link>
          <ChevronRight size={11} className="text-gray-300" />
          <Link to="/products" className="hover:text-pink-500 transition-colors">Products</Link>
          <ChevronRight size={11} className="text-gray-300" />
          <span className="text-gray-700 font-semibold truncate max-w-[200px]">{product.name}</span>
        </nav>

        <div className="grid lg:grid-cols-2 gap-12 xl:gap-20 items-start">

          {/* ── Media Gallery ── */}
          <div className="space-y-3 lg:sticky lg:top-24 max-w-[550px]">
            <div className="relative h-[500px] max-h-[500px] bg-gray-50 rounded-3xl overflow-hidden group shadow-sm">
              {showVideo && product.video_url ? (
                <video src={product.video_url} autoPlay loop muted className="w-full h-full object-cover" />
              ) : (
                <img src={selectedImage || product.image_url} alt={product.name} className="w-full h-full object-contain transition-transform duration-700 ease-out group-hover:scale-105" />
              )}
              <div className="absolute top-4 left-4">
                <span className="bg-white/90 backdrop-blur-sm text-pink-600 text-[10px] font-bold px-3 py-1.5 rounded-full uppercase tracking-wider shadow-sm">
                  {product.category}
                </span>
              </div>
              <button onClick={handleWishlist}
                className={`absolute top-4 right-4 w-10 h-10 rounded-full flex items-center justify-center shadow-md transition-all duration-200 active:scale-90 ${isWishlisted ? "bg-pink-500 text-white" : "bg-white/90 backdrop-blur-sm text-gray-400 hover:text-pink-500"}`}>
                <Heart size={18} className={isWishlisted ? "fill-white" : ""} />
              </button>
            </div>

            {/* Thumbnails */}
            <div className="flex gap-2 overflow-x-auto pb-1">
              {allImages.map((img, i) => (
                <button key={i}
                  onClick={() => { setSelectedImage(img.image_url); setShowVideo(false); }}
                  className={`flex-shrink-0 w-[72px] h-[88px] rounded-2xl overflow-hidden border-2 transition-all duration-200 ${selectedImage === img.image_url && !showVideo ? "border-pink-500 shadow-md scale-105" : "border-transparent opacity-50 hover:opacity-90"}`}
                >
                  <img src={img.image_url} className="w-full h-full object-cover" alt="" />
                </button>
              ))}
              {product.video_url && (
                <button
                  onClick={() => setShowVideo(true)}
                  className={`flex-shrink-0 w-[72px] h-[88px] rounded-2xl bg-gray-100 border-2 flex flex-col items-center justify-center gap-1 transition-all duration-200 ${showVideo ? "border-pink-500 scale-105" : "border-transparent opacity-50 hover:opacity-90"}`}
                >
                  <div className="w-8 h-8 bg-pink-500 rounded-full flex items-center justify-center">
                    <Play size={14} className="text-white ml-0.5" />
                  </div>
                  <span className="text-[9px] font-bold text-gray-500 uppercase tracking-wide">Video</span>
                </button>
              )}
            </div>
          </div>

          {/* ── Product Info ── */}
          <div className="py-2 space-y-7">

            {/* Title & Price */}
            <div className="space-y-3">
              <h1 className="text-3xl sm:text-4xl font-black text-gray-900 leading-tight tracking-tight">{product.name}</h1>
              {avgRating && (
                <div className="flex items-center gap-2">
                  <div className="flex items-center gap-0.5">
                    {[1,2,3,4,5].map(s => (
                      <Star key={s} size={14} className={s <= Math.round(avgRating) ? "text-amber-400 fill-amber-400" : "text-gray-200 fill-gray-200"} />
                    ))}
                  </div>
                  <span className="text-xs font-semibold text-gray-500">{avgRating}</span>
                  <span className="text-xs text-gray-400">({reviews.length} reviews)</span>
                </div>
              )}
              <div className="flex items-baseline gap-3">
                <span className="text-4xl font-black text-gray-900">₹{displayPrice.toLocaleString()}</span>
                <span className="text-xs text-gray-400 font-medium bg-gray-100 px-2 py-1 rounded-lg">Incl. all taxes</span>
              </div>
            </div>

            <div className="h-px bg-gray-100" />

            {/* Color Selection */}
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <span className="text-xs font-bold text-gray-500 uppercase tracking-widest">Color</span>
                <span className="text-sm font-semibold text-gray-800 capitalize">{selectedColor}</span>
              </div>
              <div className="flex gap-3 flex-wrap">
                {availableColors.map(c => (
                  <button key={c}
                    onClick={() => { setSelectedColor(c.trim()); setSelectedSize(null); }}
                    title={c}
                    className={`relative w-9 h-9 rounded-full transition-all duration-200 ${selectedColor === c ? "ring-2 ring-offset-2 ring-pink-500 scale-110" : "ring-1 ring-gray-200 hover:scale-110 hover:ring-gray-400"}`}
                    style={{ backgroundColor: c.toLowerCase() }}
                  >
                    {selectedColor === c && (
                      <span className="absolute inset-0 flex items-center justify-center">
                        <Check size={12} strokeWidth={3} className="text-white drop-shadow" />
                      </span>
                    )}
                  </button>
                ))}
              </div>
            </div>

            {/* Size Selection */}
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <span className="text-xs font-bold text-gray-500 uppercase tracking-widest">Size</span>
                <button className="text-xs font-semibold text-pink-500 hover:text-pink-700 transition-colors underline underline-offset-2">Size Guide</button>
              </div>
              <div className="flex flex-wrap gap-2">
                {sizeOptionsForColor.map(v => (
                  <button key={v.size}
                    disabled={v.quantity === 0}
                    onClick={() => setSelectedSize(v.size)}
                    className={`relative min-w-[52px] h-11 px-3 rounded-xl text-sm font-bold transition-all duration-200 ${
                      v.quantity === 0
                        ? "bg-gray-50 text-gray-300 cursor-not-allowed border border-dashed border-gray-200"
                        : selectedSize === v.size
                        ? "bg-gray-900 text-white shadow-lg scale-105 border border-gray-900"
                        : "bg-white text-gray-700 border border-gray-200 hover:border-pink-400 hover:text-pink-600 hover:shadow-sm"
                    }`}
                  >
                    {v.quantity === 0 && (
                      <span className="absolute inset-0 flex items-center justify-center pointer-events-none">
                        <span className="absolute w-full h-px bg-gray-300 rotate-45 origin-center" />
                      </span>
                    )}
                    {v.size}
                  </button>
                ))}
              </div>

              {/* Stock status messages */}
              {activeVariant && activeVariant.quantity === 0 && (
                <div className="flex items-center gap-2 text-red-600 bg-red-50 px-4 py-2.5 rounded-xl border border-red-100">
                  <AlertTriangle size={14} />
                  <p className="text-xs font-semibold">This size is out of stock.</p>
                </div>
              )}
              {activeVariant && activeVariant.quantity > 0 && activeVariant.low_stock && (
                <div className="flex items-center gap-2 text-orange-600 bg-orange-50 px-4 py-2.5 rounded-xl border border-orange-100">
                  <AlertTriangle size={14} />
                  <p className="text-xs font-semibold">Only {activeVariant.quantity} left — order soon!</p>
                </div>
              )}
              {selectedSize && !activeVariant && (
                <div className="flex items-center gap-2 text-gray-500 bg-gray-50 px-4 py-2.5 rounded-xl border border-gray-200">
                  <AlertTriangle size={14} />
                  <p className="text-xs font-semibold">This combination is not available.</p>
                </div>
              )}
            </div>

            {/* Quantity + Actions */}
            <div className="space-y-3">
              <div className="flex gap-3 items-center">
                <div className="flex items-center border border-gray-200 rounded-xl overflow-hidden">
                  <button onClick={() => setQuantity(q => Math.max(1, q - 1))} className="w-10 h-11 flex items-center justify-center text-gray-600 hover:bg-gray-50 transition-colors font-bold text-lg">−</button>
                  <span className="w-10 text-center font-bold text-gray-900 text-sm">{quantity}</span>
                  <button onClick={() => setQuantity(q => q + 1)} className="w-10 h-11 flex items-center justify-center text-gray-600 hover:bg-gray-50 transition-colors font-bold text-lg">+</button>
                </div>

                {activeVariant && activeVariant.quantity === 0 ? (
                  <div className="flex-1 bg-gray-100 text-gray-400 font-bold rounded-xl py-3.5 flex items-center justify-center gap-2 cursor-not-allowed text-sm">
                    <ShoppingCart size={18} />
                    Out of Stock
                  </div>
                ) : (
                  <button onClick={handleAddToCart}
                    className="flex-1 bg-pink-500 hover:bg-pink-600 active:bg-pink-700 text-white font-bold rounded-xl py-3.5 flex items-center justify-center gap-2 shadow-lg shadow-pink-200 active:scale-[0.98] transition-all duration-150 text-sm">
                    <ShoppingCart size={18} />
                    Add to Cart
                  </button>
                )}

                <button onClick={handleWishlist}
                  className={`w-11 h-11 rounded-xl border flex items-center justify-center transition-all duration-200 active:scale-90 ${isWishlisted ? "bg-pink-50 border-pink-300 text-pink-500" : "border-gray-200 text-gray-400 hover:text-pink-500 hover:border-pink-200"}`}>
                  <Heart size={18} className={isWishlisted ? "fill-pink-500" : ""} />
                </button>

                <button onClick={handleWhatsAppShare}
                  className="w-11 h-11 rounded-xl border border-gray-200 flex items-center justify-center text-gray-400 hover:text-green-500 hover:border-green-300 transition-all duration-200 active:scale-90">
                  <Share2 size={18} />
                </button>
              </div>

              {cartMsg && (
                <div className={`text-xs font-semibold px-4 py-2.5 rounded-xl flex items-center gap-2 ${
                  cartMsg.includes("Added")
                    ? "bg-green-50 text-green-700 border border-green-200"
                    : cartMsg.includes("already in your cart")
                    ? "bg-blue-50 text-blue-700 border border-blue-200"
                    : "bg-red-50 text-red-600 border border-red-200"
                }`}>
                  {cartMsg}
                </div>
              )}
            </div>

            {/* Product Meta */}
            {(product.fabric || product.occasion || product.pattern || product.gender) && (
              <div className="grid grid-cols-2 gap-3 pt-2 border-t border-gray-100">
                {[
                  { label: "Fabric", value: product.fabric },
                  { label: "Occasion", value: product.occasion },
                  { label: "Pattern", value: product.pattern },
                  { label: "Gender", value: product.gender },
                ].filter(m => m.value).map(m => (
                  <div key={m.label} className="bg-gray-50 rounded-xl px-3 py-2.5">
                    <p className="text-[10px] font-bold text-gray-400 uppercase tracking-widest mb-0.5">{m.label}</p>
                    <p className="text-sm font-semibold text-gray-800">{m.value}</p>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>

        {/* Description */}
        {product.description && (
          <div className="mt-16 max-w-3xl">
            <h2 className="text-xs font-bold text-gray-400 uppercase tracking-widest mb-3">About this product</h2>
            <p className="text-base text-gray-600 leading-relaxed">{product.description}</p>
          </div>
        )}

        {/* ── User Photos ── */}
        {userPhotos.length > 0 && (
          <div className="mt-16">
            <div className="flex items-center justify-between mb-5">
              <h2 className="text-xl font-black text-gray-900">Customer Photos</h2>
              <Link to={`/upload-photos/${id}`} className="text-xs font-bold text-pink-500 hover:text-pink-700 uppercase tracking-wider underline underline-offset-2 transition-colors">
                Upload Yours
              </Link>
            </div>
            <div className="grid grid-cols-3 sm:grid-cols-5 gap-3">
              {userPhotos.map(photo => (
                <div key={photo.id} className="aspect-square rounded-2xl overflow-hidden bg-gray-100 group">
                  <img src={photo.photo_url} alt="Customer photo" className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-110" />
                </div>
              ))}
            </div>
          </div>
        )}

        {userPhotos.length === 0 && (
          <div className="mt-16">
            <h2 className="text-xl font-black text-gray-900 mb-4">Customer Photos</h2>
            <div className="border-2 border-dashed border-gray-200 rounded-2xl p-10 text-center hover:border-pink-300 transition-colors">
              <Upload size={28} className="mx-auto text-gray-300 mb-3" />
              <p className="text-gray-400 font-medium text-sm">No customer photos yet.</p>
              <Link to={`/upload-photos/${id}`} className="mt-3 inline-block text-xs font-bold text-pink-500 uppercase tracking-widest underline underline-offset-4">
                Be the first to upload
              </Link>
            </div>
          </div>
        )}

        {/* ── Reviews ── */}
        <div className="mt-16 mb-16">
          <div className="flex items-center gap-3 mb-8">
            <h2 className="text-xl font-black text-gray-900">Reviews</h2>
            {reviews.length > 0 && (
              <span className="bg-pink-50 text-pink-600 text-xs font-bold px-2.5 py-1 rounded-full">{reviews.length}</span>
            )}
            {avgRating && (
              <div className="flex items-center gap-1 ml-auto">
                <Star size={16} className="text-amber-400 fill-amber-400" />
                <span className="text-sm font-bold text-gray-700">{avgRating}</span>
              </div>
            )}
          </div>

          {/* Write a Review Form */}
          <div className="bg-gray-50 rounded-2xl p-6 mb-6 border border-gray-100">
            <h3 className="text-base font-bold text-gray-900 mb-5">Write a Review</h3>

            {/* Star Rating Selector */}
            <div className="mb-5">
              <label className="text-xs font-bold text-gray-500 uppercase tracking-wider mb-2.5 block">Your Rating *</label>
              <div className="flex gap-1.5">
                {[1, 2, 3, 4, 5].map(star => (
                  <button
                    key={star}
                    type="button"
                    onClick={() => setReviewRating(star)}
                    onMouseEnter={(e) => {
                      // Hover effect - show preview
                      const stars = e.currentTarget.parentElement.children;
                      for (let i = 0; i < stars.length; i++) {
                        const starIcon = stars[i].querySelector('svg');
                        if (i < star) {
                          starIcon.classList.add('text-yellow-400', 'fill-yellow-400');
                          starIcon.classList.remove('text-gray-300', 'fill-gray-300');
                        }
                      }
                    }}
                    onMouseLeave={(e) => {
                      // Reset to actual rating
                      const stars = e.currentTarget.parentElement.children;
                      for (let i = 0; i < stars.length; i++) {
                        const starIcon = stars[i].querySelector('svg');
                        if (i < reviewRating) {
                          starIcon.classList.add('text-yellow-400', 'fill-yellow-400');
                          starIcon.classList.remove('text-gray-300', 'fill-gray-300');
                        } else {
                          starIcon.classList.add('text-gray-300', 'fill-gray-300');
                          starIcon.classList.remove('text-yellow-400', 'fill-yellow-400');
                        }
                      }
                    }}
                    className="transition-transform hover:scale-125 active:scale-110"
                  >
                    <Star size={28} className={star <= reviewRating ? "text-yellow-400 fill-yellow-400" : "text-gray-300 fill-gray-300"} />
                  </button>
                ))}
              </div>
              {reviewRating > 0 && (
                <p className="text-xs text-gray-600 font-bold mt-2">
                  {reviewRating === 1 && "Poor"}
                  {reviewRating === 2 && "Fair"}
                  {reviewRating === 3 && "Good"}
                  {reviewRating === 4 && "Very Good"}
                  {reviewRating === 5 && "Excellent"}
                </p>
              )}
            </div>

            {/* Comment Textarea */}
            <div className="mb-4">
              <label className="text-xs font-black text-gray-500 uppercase tracking-wider mb-2 block">Your Review (Optional)</label>
              <textarea
                value={reviewComment}
                onChange={(e) => setReviewComment(e.target.value)}
                maxLength={500}
                rows={4}
                placeholder="Share your experience with this product..."
                className="w-full border border-gray-200 rounded-xl px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-pink-500 resize-none"
              />
              <div className="flex justify-between items-center mt-1">
                <p className="text-xs text-gray-400">Maximum 500 characters</p>
                <p className={`text-xs font-bold ${reviewComment.length > 500 ? 'text-red-600' : 'text-gray-500'}`}>
                  {reviewComment.length}/500
                </p>
              </div>
            </div>

            {/* Submit Button */}
            <button
              onClick={handleSubmitReview}
              disabled={reviewSubmitting || reviewRating === 0}
              className="w-full bg-gray-900 hover:bg-black text-white font-bold py-3 rounded-xl transition-all active:scale-[0.98] disabled:opacity-40 disabled:cursor-not-allowed flex items-center justify-center gap-2 text-sm"
            >
              {reviewSubmitting ? (
                <><Loader2 size={16} className="animate-spin" /> Submitting...</>
              ) : (
                <><Star size={16} /> Submit Review</>
              )}
            </button>

            {/* Message */}
            {reviewMsg && (
              <div className={`mt-3 text-sm font-bold px-4 py-3 rounded-xl ${
                reviewMsg.includes("✓") || reviewMsg.includes("success") 
                  ? "bg-green-100 text-green-700 border border-green-200" 
                  : "bg-red-100 text-red-700 border border-red-200"
              }`}>
                {reviewMsg}
              </div>
            )}

            {!localStorage.getItem("whatsapp_number") && (
              <div className="mt-3 bg-blue-50 border border-blue-200 text-blue-700 text-xs font-bold px-4 py-3 rounded-xl flex items-center gap-2">
                <Info size={16} />
                <span>Please <Link to="/whatsapp-login" className="underline">login with WhatsApp</Link> to submit a review</span>
              </div>
            )}
          </div>

          {/* Existing Reviews */}
          {reviews.length === 0 ? (
            <div className="border-2 border-dashed border-gray-200 rounded-2xl p-10 text-center">
              <Star size={28} className="mx-auto text-gray-200 mb-3" />
              <p className="text-gray-400 font-medium text-sm">No reviews yet. Be the first to review this product.</p>
            </div>
          ) : (
            <div className="space-y-3">
              {reviews.map(review => (
                <div key={review.id} className="bg-white rounded-2xl p-5 border border-gray-100 shadow-sm hover:shadow-md transition-shadow">
                  <div className="flex items-center justify-between mb-2">
                    <div className="flex items-center gap-0.5">
                      {[1,2,3,4,5].map(s => (
                        <Star key={s} size={13} className={s <= review.rating ? "text-amber-400 fill-amber-400" : "text-gray-200 fill-gray-200"} />
                      ))}
                    </div>
                    <span className="text-xs text-gray-400">
                      {new Date(review.created_at).toLocaleDateString('en-IN', { day: 'numeric', month: 'short', year: 'numeric' })}
                    </span>
                  </div>
                  {review.comment && <p className="text-sm text-gray-700 leading-relaxed">{review.comment}</p>}
                </div>
              ))}
            </div>
          )}
        </div>

      </div>

      {/* ── Sticky mobile Add to Cart ── */}
      <div className="fixed bottom-0 left-0 right-0 md:hidden bg-white border-t border-gray-100 px-4 py-3 z-50 shadow-2xl">
        <div className="flex gap-3 items-center">
          <button onClick={handleWishlist}
            className={`w-12 h-12 rounded-xl border flex items-center justify-center flex-shrink-0 transition-all ${isWishlisted ? "bg-pink-50 border-pink-300 text-pink-500" : "border-gray-200 text-gray-400"}`}>
            <Heart size={20} className={isWishlisted ? "fill-pink-500" : ""} />
          </button>
          {activeVariant && activeVariant.quantity === 0 ? (
            <div className="flex-1 bg-gray-100 text-gray-400 font-bold rounded-xl py-3.5 flex items-center justify-center gap-2 text-sm cursor-not-allowed">
              <ShoppingCart size={18} /> Out of Stock
            </div>
          ) : (
            <button onClick={handleAddToCart}
              className="flex-1 bg-pink-500 hover:bg-pink-600 text-white font-bold rounded-xl py-3.5 flex items-center justify-center gap-2 shadow-lg shadow-pink-200 active:scale-[0.98] transition-all text-sm">
              <ShoppingCart size={18} /> Add to Cart
            </button>
          )}
        </div>
      </div>
    </div>
  );
};

export default ProductDetailPage;
