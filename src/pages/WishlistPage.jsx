import { useContext } from "react";
import { WishlistContext } from "../context/WishlistContext";
import ProductCard from "../components/ProductCard";
import { HeartOff, Sparkles } from "lucide-react";
import { Link } from "react-router-dom";

const WishlistPage = () => {
  const { wishlist } = useContext(WishlistContext);

  return (
    <div className="bg-[#fafafa] min-h-screen pb-20">
      {/* Header */}
      <div className="bg-white pt-16 pb-20 border-b border-gray-100 mb-12">
        <div className="max-w-7xl mx-auto px-6 text-center">
           <span className="text-xs font-black text-pink-600 uppercase tracking-widest mb-4 block">Your Collection</span>
           <h1 className="text-5xl font-black text-gray-900 tracking-tighter">Saved Styles <span className="text-pink-600">.</span></h1>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-6">
        {wishlist.length === 0 ? (
          <div className="max-w-md mx-auto text-center py-20 space-y-8 bg-white rounded-[40px] shadow-sm border border-gray-100 p-10">
             <div className="w-20 h-20 bg-gray-50 rounded-full flex items-center justify-center mx-auto text-gray-300">
                <HeartOff size={40} />
             </div>
             <div>
                <h3 className="text-2xl font-black text-gray-900 mb-2">Longing for style?</h3>
                <p className="text-gray-500 font-medium">Your wishlist is currently waiting for its first masterpiece.</p>
             </div>
             <Link 
               to="/products" 
               className="inline-flex items-center gap-3 px-10 py-4 bg-gray-900 text-white font-bold rounded-2xl shadow-xl hover:bg-black transition active:scale-95"
             >
               <Sparkles size={18} />
               Explore Boutique
             </Link>
          </div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-8">
            {wishlist.map((product) => (
              <ProductCard key={product.id} product={product} />
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default WishlistPage;