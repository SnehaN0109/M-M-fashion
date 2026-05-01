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
  const { addToCart } = useContext(CartContext);
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
    if (!activeVariant || quantity > activeVariant.quantity) { setCartMsg("Selected variant is out of stock."); return; }
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
      <Loader2 className="w-12 h-12 text-pink-600 animate-spin" />
      <p className="text-xs font-black text-gray-400 uppercase tracking-widest">Loading...</p>
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
      <div className="max-w-7xl mx-auto px-6 py-10">

        {/* Breadcrumb */}
        <nav className="flex items-center gap-2 mb-10 text-[10px] font-black uppercase tracking-widest text-gray-400">
          <Link to="/" className="hover:text-pink-600 transition-colors">Home</Link>
          <ChevronRight size={12} />
          <Link to="/products" className="hover:text-pink-600 transition-colors">Products</Link>
          <ChevronRight size={12} />
          <span className="text-gray-900">{product.name}</span>
        </nav>

        <div className="grid lg:grid-cols-2 gap-16 items-start">

          {/* ── Media Gallery ── */}
          <div className="space-y-4">
            <div className="relative aspect-[3/4] bg-gray-50 rounded-[32px] overflow-hidden shadow-xl">
              {showVideo && product.video_url ? (
                <video src={product.video_url} autoPlay loop muted className="w-full h-full object-cover" />
              ) : (
                <img src={selectedImage || product.image_url} alt={product.name} className="w-full h-full object-cover" />
              )}
            </div>

            {/* Thumbnails */}
            <div className="flex gap-3 overflow-x-auto pb-1">
              {allImages.map((img, i) => (
                <button key={i}
                  onClick={() => { setSelectedImage(img.image_url); setShowVideo(false); }}
                  className={`flex-shrink-0 w-20 h-24 rounded-2xl overflow-hidden border-2 transition-all ${selectedImage === img.image_url && !showVideo ? "border-pink-600 scale-105" : "border-transparent opacity-60 hover:opacity-100"}`}
                >
                  <img src={img.image_url} className="w-full h-full object-cover" alt="" />
                </button>
              ))}
              {product.video_url && (
                <button
                  onClick={() => setShowVideo(true)}
                  className={`flex-shrink-0 w-20 h-24 rounded-2xl bg-gray-100 border-2 flex flex-col items-center justify-center gap-1 transition-all ${showVideo ? "border-pink-600 scale-105" : "border-transparent opacity-60 hover:opacity-100"}`}
                >
                  <Play size={18} className="text-pink-600" />
                  <span className="text-[9px] font-black text-gray-600 uppercase">Video</span>
                </button>
              )}
            </div>
          </div>

          {/* ── Product Info ── */}
          <div className="py-4 space-y-8">

            {/* Title & Price */}
            <div>
              <span className="text-xs font-black text-pink-600 uppercase tracking-widest">{product.category}</span>
              <h1 className="text-4xl font-black text-gray-900 tracking-tight leading-tight mt-1">{product.name}</h1>
              <div className="flex items-baseline gap-3 mt-4">
                <span className="text-5xl font-black text-gray-900">₹{displayPrice.toLocaleString()}</span>
                <span className="text-sm text-gray-400 font-bold uppercase">Incl. taxes</span>
              </div>
              {avgRating && (
                <div className="flex items-center gap-2 mt-2">
                  <div className="flex">
                    {[1,2,3,4,5].map(s => (
                      <Star key={s} size={14} className={s <= Math.round(avgRating) ? "text-yellow-400 fill-yellow-400" : "text-gray-200 fill-gray-200"} />
                    ))}
                  </div>
                  <span className="text-xs font-bold text-gray-500">{avgRating} ({reviews.length} reviews)</span>
                </div>
              )}
            </div>

            {/* Color Selection */}
            <div className="space-y-3">
              <div className="flex justify-between">
                <h3 className="text-xs font-black text-gray-400 uppercase tracking-widest">Color</h3>
                <span className="text-xs font-bold text-gray-900">{selectedColor}</span>
              </div>
              <div className="flex gap-3 flex-wrap">
                {availableColors.map(c => (
                  <button key={c}
                    onClick={() => { setSelectedColor(c.trim()); setSelectedSize(null); }}
                    className={`relative w-10 h-10 rounded-full border-2 p-0.5 transition-all ${selectedColor === c ? "border-gray-900" : "border-transparent hover:scale-110"}`}
                  >
                    <div className="w-full h-full rounded-full shadow-inner" style={{ backgroundColor: c.toLowerCase() }} />
                    {selectedColor === c && (
                      <div className="absolute -top-1 -right-1 w-4 h-4 bg-gray-900 rounded-full flex items-center justify-center border-2 border-white">
                        <Check size={8} strokeWidth={4} className="text-white" />
                      </div>
                    )}
                  </button>
                ))}
              </div>
            </div>

            {/* Size Selection */}
            <div className="space-y-3">
              <div className="flex justify-between">
                <h3 className="text-xs font-black text-gray-400 uppercase tracking-widest">Size</h3>
                <button className="text-[10px] font-black text-pink-600 uppercase tracking-widest underline underline-offset-4">Size Guide</button>
              </div>
              <div className="flex flex-wrap gap-2">
                {sizeOptionsForColor.map(v => (
                  <button key={v.size}
                    disabled={v.quantity === 0}
                    onClick={() => setSelectedSize(v.size)}
                    className={`w-14 h-12 rounded-xl text-sm font-black transition-all ${
                      v.quantity === 0 ? "bg-gray-50 text-gray-300 cursor-not-allowed line-through" :
                      selectedSize === v.size ? "bg-gray-900 text-white shadow-lg scale-105" :
                      "bg-white border border-gray-200 text-gray-700 hover:border-pink-400"
                    }`}
                  >
                    {v.size}
                  </button>
                ))}
              </div>
              {activeVariant?.low_stock && (
                <div className="flex items-center gap-2 text-red-600 bg-red-50 p-3 rounded-xl border border-red-100">
                  <AlertTriangle size={16} />
                  <p className="text-xs font-bold">Only {activeVariant.quantity} left!</p>
                </div>
              )}
            </div>

            {/* Quantity + Actions */}
            <div className="flex gap-3 items-center">
              <div className="bg-gray-100 rounded-2xl flex items-center p-1">
                <button onClick={() => setQuantity(q => Math.max(1, q - 1))} className="w-10 h-10 font-black flex items-center justify-center hover:bg-white rounded-xl transition">−</button>
                <span className="w-8 text-center font-black">{quantity}</span>
                <button onClick={() => setQuantity(q => q + 1)} className="w-10 h-10 font-black flex items-center justify-center hover:bg-white rounded-xl transition">+</button>
              </div>

              <button onClick={handleAddToCart}
                className="flex-1 bg-pink-600 hover:bg-pink-700 text-white font-black rounded-2xl py-4 flex items-center justify-center gap-3 shadow-lg active:scale-95 transition-all">
                <ShoppingCart size={20} />
                Add to Cart
              </button>

              <button onClick={handleWishlist}
                className={`w-14 h-14 rounded-full border flex items-center justify-center transition-all active:scale-90 ${isWishlisted ? "bg-pink-50 border-pink-200 text-pink-600" : "bg-white border-gray-200 text-gray-400 hover:text-pink-600 hover:border-pink-200"}`}>
                <Heart size={22} className={isWishlisted ? "fill-pink-600" : ""} />
              </button>

              <button onClick={handleWhatsAppShare}
                className="w-14 h-14 rounded-full border border-gray-200 bg-white flex items-center justify-center text-green-500 hover:border-green-300 transition-all active:scale-90">
                <Share2 size={20} />
              </button>
            </div>

            {cartMsg && (
              <div className={`text-sm font-bold px-4 py-3 rounded-xl ${cartMsg.includes("Added") ? "bg-green-50 text-green-600" : "bg-red-50 text-red-600"}`}>
                {cartMsg}
              </div>
            )}

            {/* Product Meta */}
            <div className="grid grid-cols-2 gap-4 border-t pt-6 text-sm">
              {product.fabric && <div><p className="text-[10px] font-black text-gray-400 uppercase tracking-widest">Fabric</p><p className="font-bold text-gray-900 mt-0.5">{product.fabric}</p></div>}
              {product.occasion && <div><p className="text-[10px] font-black text-gray-400 uppercase tracking-widest">Occasion</p><p className="font-bold text-gray-900 mt-0.5">{product.occasion}</p></div>}
              {product.pattern && <div><p className="text-[10px] font-black text-gray-400 uppercase tracking-widest">Pattern</p><p className="font-bold text-gray-900 mt-0.5">{product.pattern}</p></div>}
              {product.gender && <div><p className="text-[10px] font-black text-gray-400 uppercase tracking-widest">Gender</p><p className="font-bold text-gray-900 mt-0.5">{product.gender}</p></div>}
            </div>
          </div>
        </div>

        {/* Description */}
        {product.description && (
          <div className="mt-16 max-w-3xl">
            <h2 className="text-xs font-black text-gray-400 uppercase tracking-widest mb-4">Description</h2>
            <p className="text-lg text-gray-600 leading-relaxed">{product.description}</p>
          </div>
        )}

        {/* ── User Photos ── */}
        {userPhotos.length > 0 && (
          <div className="mt-16">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-xl font-black text-gray-900">Customer Photos</h2>
              <Link to={`/upload-photos/${id}`} className="text-xs font-black text-pink-600 uppercase tracking-widest underline underline-offset-4">
                Upload Yours
              </Link>
            </div>
            <div className="grid grid-cols-3 sm:grid-cols-5 gap-3">
              {userPhotos.map(photo => (
                <div key={photo.id} className="aspect-square rounded-2xl overflow-hidden bg-gray-100">
                  <img src={photo.photo_url} alt="Customer photo" className="w-full h-full object-cover" />
                </div>
              ))}
            </div>
          </div>
        )}

        {userPhotos.length === 0 && (
          <div className="mt-16">
            <h2 className="text-xl font-black text-gray-900 mb-4">Customer Photos</h2>
            <div className="border-2 border-dashed border-gray-200 rounded-2xl p-10 text-center">
              <Upload size={32} className="mx-auto text-gray-300 mb-3" />
              <p className="text-gray-400 font-medium text-sm">No customer photos yet.</p>
              <Link to={`/upload-photos/${id}`} className="mt-3 inline-block text-xs font-black text-pink-600 uppercase tracking-widest underline underline-offset-4">
                Be the first to upload
              </Link>
            </div>
          </div>
        )}

        {/* ── Reviews ── */}
        <div className="mt-16 mb-10">
          <h2 className="text-xl font-black text-gray-900 mb-6">
            Reviews {reviews.length > 0 && <span className="text-gray-400 font-medium text-base">({reviews.length})</span>}
          </h2>

          {/* Write a Review Form */}
          <div className="bg-gradient-to-br from-pink-50 to-purple-50 rounded-2xl p-6 mb-6 border border-pink-100">
            <h3 className="text-lg font-black text-gray-900 mb-4">Write a Review</h3>
            
            {/* Star Rating Selector */}
            <div className="mb-4">
              <label className="text-xs font-black text-gray-500 uppercase tracking-wider mb-2 block">
                Your Rating *
              </label>
              <div className="flex gap-2">
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
                    <Star 
                      size={32} 
                      className={star <= reviewRating ? "text-yellow-400 fill-yellow-400" : "text-gray-300 fill-gray-300"}
                    />
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
              <label className="text-xs font-black text-gray-500 uppercase tracking-wider mb-2 block">
                Your Review (Optional)
              </label>
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
              className="w-full bg-pink-600 hover:bg-pink-700 text-white font-black py-3 rounded-xl transition-all active:scale-95 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
            >
              {reviewSubmitting ? (
                <>
                  <Loader2 size={18} className="animate-spin" />
                  Submitting...
                </>
              ) : (
                <>
                  <Star size={18} />
                  Submit Review
                </>
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
              <Star size={32} className="mx-auto text-gray-300 mb-3" />
              <p className="text-gray-400 font-medium text-sm">No reviews yet. Be the first to review this product.</p>
            </div>
          ) : (
            <div className="space-y-4">
              {reviews.map(review => (
                <div key={review.id} className="bg-gray-50 rounded-2xl p-5 border border-gray-100">
                  <div className="flex items-center gap-2 mb-2">
                    <div className="flex">
                      {[1,2,3,4,5].map(s => (
                        <Star key={s} size={14} className={s <= review.rating ? "text-yellow-400 fill-yellow-400" : "text-gray-200 fill-gray-200"} />
                      ))}
                    </div>
                    <span className="text-xs text-gray-400 font-medium">
                      {new Date(review.created_at).toLocaleDateString('en-IN')}
                    </span>
                  </div>
                  {review.comment && <p className="text-sm text-gray-700 leading-relaxed">{review.comment}</p>}
                </div>
              ))}
            </div>
          )}
        </div>

      </div>
    </div>
  );
};

export default ProductDetailPage;
