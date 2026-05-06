import { useState, useRef } from "react";
import { useParams, Link } from "react-router-dom";
import { Upload, Camera, CheckCircle, Loader2, X } from "lucide-react";

const UploadUserPhotosPage = () => {
  const { productId } = useParams(); // optional — can be passed via route
  const fileInputRef = useRef(null);

  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [review, setReview] = useState("");
  const [rating, setRating] = useState(0);
  const [hoverRating, setHoverRating] = useState(0);
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);
  const [error, setError] = useState("");

  const whatsapp = localStorage.getItem("whatsapp_number");

  const handleFileChange = (e) => {
    const selected = e.target.files[0];
    if (!selected) return;
    const allowed = ["image/jpeg", "image/jpg", "image/png", "image/webp"];
    if (!allowed.includes(selected.type)) {
      setError("Only JPG, PNG, or WEBP images are allowed.");
      return;
    }
    if (selected.size > 5 * 1024 * 1024) {
      setError("File size must be under 5MB.");
      return;
    }
    setFile(selected);
    setPreview(URL.createObjectURL(selected));
    setError("");
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!whatsapp) { setError("Please login with WhatsApp first."); return; }
    if (!file) { setError("Please select a photo."); return; }
    if (!productId) { setError("No product selected. Please go to a product page to upload."); return; }

    setLoading(true);
    setError("");

    const formData = new FormData();
    formData.append("photo", file);
    formData.append("whatsapp_number", whatsapp);

    try {
      const res = await fetch(`${import.meta.env.VITE_API_URL}/api/products/${productId}/photos`, {
        method: "POST",
        body: formData,
      });
      const data = await res.json();
      if (!res.ok) { setError(data.error || "Upload failed."); return; }

      // Optionally submit review too
      if (rating > 0 || review.trim()) {
        await fetch(`${import.meta.env.VITE_API_URL}/api/products/${productId}/reviews`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ rating, comment: review.trim(), whatsapp_number: whatsapp }),
        });
      }

      setSuccess(true);
    } catch {
      setError("Could not connect to server. Try again.");
    } finally {
      setLoading(false);
    }
  };

  if (success) return (
    <div className="min-h-screen flex flex-col items-center justify-center gap-6 px-6 text-center">
      <CheckCircle size={64} className="text-green-500" />
      <h2 className="text-2xl font-black text-gray-900">Photo Uploaded!</h2>
      <p className="text-gray-500 max-w-sm">Your photo is pending admin approval and will appear on the product page soon.</p>
      <Link to={productId ? `/products/${productId}` : "/products"} className="px-8 py-3 bg-pink-600 text-white font-bold rounded-2xl">
        Back to Product
      </Link>
    </div>
  );

  return (
    <div className="max-w-lg mx-auto px-6 py-16">
      <h1 className="text-2xl font-black mb-2">Upload Your Look 📸</h1>
      <p className="text-sm text-gray-400 mb-8">Share how you styled it! Your photo will appear on the product page after review.</p>

      {!whatsapp && (
        <div className="bg-yellow-50 border border-yellow-200 rounded-2xl p-4 mb-6 text-sm text-yellow-700 font-medium">
          You need to <Link to="/whatsapp-login" className="font-black underline">login with WhatsApp</Link> to upload photos.
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-6">

        {/* Photo Upload */}
        <div>
          <label className="text-xs font-black text-gray-400 uppercase tracking-widest block mb-2">Your Photo *</label>
          {preview ? (
            <div className="relative rounded-2xl overflow-hidden aspect-square bg-gray-100">
              <img src={preview} alt="Preview" className="w-full h-full object-cover" />
              <button
                type="button"
                onClick={() => { setFile(null); setPreview(null); }}
                className="absolute top-3 right-3 w-8 h-8 bg-white rounded-full shadow flex items-center justify-center"
              >
                <X size={16} />
              </button>
            </div>
          ) : (
            <button
              type="button"
              onClick={() => fileInputRef.current?.click()}
              className="w-full aspect-square border-2 border-dashed border-gray-200 rounded-2xl flex flex-col items-center justify-center gap-3 hover:border-pink-400 hover:bg-pink-50 transition-all"
            >
              <Camera size={36} className="text-gray-300" />
              <span className="text-sm font-bold text-gray-400">Click to select photo</span>
              <span className="text-xs text-gray-300">JPG, PNG, WEBP · Max 5MB</span>
            </button>
          )}
          <input
            ref={fileInputRef}
            type="file"
            accept="image/jpeg,image/jpg,image/png,image/webp"
            onChange={handleFileChange}
            className="hidden"
          />
        </div>

        {/* Star Rating */}
        <div>
          <label className="text-xs font-black text-gray-400 uppercase tracking-widest block mb-2">Rating (optional)</label>
          <div className="flex gap-2">
            {[1, 2, 3, 4, 5].map((star) => (
              <button
                key={star}
                type="button"
                onClick={() => setRating(star)}
                onMouseEnter={() => setHoverRating(star)}
                onMouseLeave={() => setHoverRating(0)}
                className="text-2xl transition-transform hover:scale-110"
              >
                <span className={(hoverRating || rating) >= star ? "text-yellow-400" : "text-gray-200"}>★</span>
              </button>
            ))}
          </div>
        </div>

        {/* Review Text */}
        <div>
          <label className="text-xs font-black text-gray-400 uppercase tracking-widest block mb-2">Review (optional)</label>
          <textarea
            value={review}
            onChange={(e) => setReview(e.target.value)}
            placeholder="How did you style it? What did you love about it?"
            rows={3}
            className="w-full border border-gray-200 rounded-2xl px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-pink-500 resize-none"
          />
        </div>

        {error && <p className="text-red-500 text-sm font-bold">{error}</p>}

        <button
          type="submit"
          disabled={loading || !file}
          className="w-full bg-pink-600 hover:bg-pink-700 text-white font-black py-4 rounded-2xl flex items-center justify-center gap-2 disabled:opacity-50 transition-all active:scale-95"
        >
          {loading ? <Loader2 size={20} className="animate-spin" /> : <Upload size={20} />}
          {loading ? "Uploading..." : "Submit Photo"}
        </button>
      </form>
    </div>
  );
};

export default UploadUserPhotosPage;
