import React, { useState, useContext } from "react";
import { Link, NavLink, useNavigate } from "react-router-dom";
import { ShoppingCart, Heart, User, Search, Menu, X, Package } from "lucide-react";
import { WishlistContext } from "../context/WishlistContext";
import { CartContext } from "../context/CartContext";

const Navbar = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const { wishlist } = useContext(WishlistContext);
  const { cartItems } = useContext(CartContext);
  const cartCount = cartItems.reduce((acc, item) => acc + (item.cartQuantity || 1), 0);
  const navigate = useNavigate();

  const navLinks = [
    { title: "Boutique", path: "/products" },
    { title: "Men", path: "/men" },
    { title: "Women", path: "/women" },
    { title: "Ethnic", path: "/ethnic" },
  ];

  return (
    <nav className="bg-white/80 backdrop-blur-md sticky top-0 z-[100] border-b border-gray-100">
      <div className="max-w-7xl mx-auto px-6 h-20 flex items-center justify-between">
        
        {/* Logo */}
        <Link to="/" className="text-2xl font-black text-gray-900 tracking-tighter flex items-center gap-2">
           M&M <span className="text-pink-600">Fashion.</span>
        </Link>

        {/* Desktop Links */}
        <div className="hidden lg:flex items-center gap-8">
           {navLinks.map(link => (
             <NavLink 
               key={link.path} 
               to={link.path} 
               className={({ isActive }) => `text-sm font-bold uppercase tracking-widest transition-colors ${isActive ? "text-pink-600" : "text-gray-500 hover:text-gray-900"}`}
             >
               {link.title}
             </NavLink>
           ))}
        </div>

        {/* Global Search Hint */}
        <div className="hidden md:flex flex-1 max-w-sm mx-12">
           <div className="w-full relative group">
              <input 
                type="text" 
                placeholder="Find styles..." 
                className="w-full bg-gray-50 border-none rounded-full py-2.5 pl-10 text-xs font-bold focus:ring-2 ring-pink-500/20"
                onFocus={() => navigate('/products')}
              />
              <Search className="absolute left-3.5 top-1/2 -translate-y-1/2 text-gray-400 group-focus-within:text-pink-600" size={14} />
           </div>
        </div>

        {/* Actions */}
        <div className="flex items-center gap-6">
           <Link to="/wishlist" className="relative group p-2 rounded-full hover:bg-gray-50 transition">
              <Heart size={20} className="text-gray-600 group-hover:text-pink-600 transition" />
              {wishlist.length > 0 && (
                <span className="absolute top-1 right-1 w-4 h-4 bg-pink-600 text-[8px] font-black text-white flex items-center justify-center rounded-full ring-2 ring-white">
                  {wishlist.length}
                </span>
              )}
           </Link>

           <Link to="/cart" className="relative group p-2 rounded-full hover:bg-gray-50 transition">
              <ShoppingCart size={20} className="text-gray-600 group-hover:text-pink-600 transition" />
              {cartCount > 0 && (
                <span className="absolute top-1 right-1 w-4 h-4 bg-gray-900 text-[8px] font-black text-white flex items-center justify-center rounded-full ring-2 ring-white">
                  {cartCount}
                </span>
              )}
           </Link>

           <Link to="/login" className="hidden sm:flex items-center gap-2 bg-gray-900 text-white px-5 py-2.5 rounded-full text-xs font-black uppercase tracking-widest hover:bg-black transition shadow-lg active:scale-95">
              <User size={14} />
              Login
           </Link>

           {/* Mobile Toggle */}
           <button className="lg:hidden" onClick={() => setIsMenuOpen(!isMenuOpen)}>
              {isMenuOpen ? <X size={24} /> : <Menu size={24} />}
           </button>
        </div>
      </div>

      {/* Mobile Menu */}
      {isMenuOpen && (
        <div className="lg:hidden absolute top-20 inset-x-0 bg-white border-b border-gray-100 p-6 space-y-4 shadow-xl">
           {navLinks.map(link => (
             <Link 
               key={link.path} 
               to={link.path} 
               onClick={() => setIsMenuOpen(false)}
               className="block text-lg font-black text-gray-900 uppercase tracking-tighter"
             >
               {link.title}
             </Link>
           ))}
           <div className="pt-4 border-t flex flex-col gap-4">
              <Link to="/my-orders" onClick={() => setIsOpen(false)} className="text-sm font-bold text-gray-500 uppercase tracking-widest">My Orders</Link>
              <Link to="/login" onClick={() => setIsOpen(false)} className="w-full text-center bg-gray-900 text-white py-4 rounded-2xl font-black uppercase tracking-widest">Login</Link>
           </div>
        </div>
      )}
    </nav>
  );
};

export default Navbar;
