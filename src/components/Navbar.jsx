import React, { useState, useContext, useEffect } from "react";
import { Link, NavLink, useNavigate } from "react-router-dom";
import { ShoppingCart, Heart, User, Search, Menu, X, Package, LogOut } from "lucide-react";
import { WishlistContext } from "../context/WishlistContext";
import { CartContext } from "../context/CartContext";

const Navbar = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [scrolled, setScrolled] = useState(false);
  const { wishlist, clearWishlist } = useContext(WishlistContext);
  const { cartItems, resetCart } = useContext(CartContext);
  const cartCount = cartItems.reduce((acc, item) => acc + (item.cartQuantity || 1), 0);
  const navigate = useNavigate();

  // Shadow on scroll — only adds/removes a class, zero logic change
  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 10);
    window.addEventListener("scroll", onScroll, { passive: true });
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  const isLoggedIn = !!localStorage.getItem("auth_token");

  const handleLogout = () => {
    clearWishlist();
    resetCart();
    localStorage.removeItem("auth_token");
    localStorage.removeItem("user_id");
    localStorage.removeItem("phone_number");
    localStorage.removeItem("whatsapp_number");
    localStorage.removeItem("email");
    setIsMenuOpen(false);
    navigate("/login");
  };

  const navLinks = [
    { title: "Boutique", path: "/products" },
    { title: "Men", path: "/men" },
    { title: "Women", path: "/women" },
    { title: "Ethnic", path: "/ethnic" },
  ];

  return (
    <nav className="bg-white border-b border-gray-200 sticky top-0 z-[100]">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 h-14 flex items-center gap-4">

        {/* Logo */}
        <Link to="/" className="flex-shrink-0 text-lg font-bold text-gray-900 mr-2">
          M&M <span className="text-pink-600">Fashion</span>
        </Link>

        {/* Search */}
        <div className="hidden md:flex flex-1 max-w-md">
          <div className="w-full relative">
            <input
              type="text"
              placeholder="Search for products, brands and more"
              className="w-full border border-gray-300 rounded py-1.5 pl-3 pr-9 text-sm text-gray-700 placeholder-gray-400 focus:outline-none focus:border-blue-500"
              onFocus={() => navigate('/products')}
            />
            <button className="absolute right-0 top-0 h-full px-3 bg-blue-500 rounded-r flex items-center justify-center">
              <Search size={14} className="text-white" />
            </button>
          </div>
        </div>

        {/* Nav Links */}
        <div className="hidden lg:flex items-center gap-6 ml-4">
          {navLinks.map(link => (
            <NavLink
              key={link.path}
              to={link.path}
              className={({ isActive }) =>
                `text-sm font-medium transition-colors ${isActive ? "text-blue-600" : "text-gray-700 hover:text-blue-600"}`
              }
            >
              {link.title}
            </NavLink>
          ))}
        </div>

        {/* Right Icons */}
        <div className="flex items-center gap-4 ml-auto">

          {/* Wishlist */}
          <Link to="/wishlist" className="relative flex flex-col items-center gap-0.5 group">
            <Heart size={20} className="text-gray-700 group-hover:text-blue-600 transition-colors" />
            <span className="text-[10px] text-gray-600 hidden sm:block">Wishlist</span>
            {wishlist.length > 0 && (
              <span className="absolute -top-1 -right-1 w-4 h-4 bg-red-500 text-[8px] font-bold text-white flex items-center justify-center rounded-full">
                {wishlist.length}
              </span>
            )}
          </Link>

          {/* Cart */}
          <Link to="/cart" className="relative flex flex-col items-center gap-0.5 group">
            <ShoppingCart size={20} className="text-gray-700 group-hover:text-blue-600 transition-colors" />
            <span className="text-[10px] text-gray-600 hidden sm:block">Cart</span>
            {cartCount > 0 && (
              <span className="absolute -top-1 -right-1 w-4 h-4 bg-red-500 text-[8px] font-bold text-white flex items-center justify-center rounded-full">
                {cartCount}
              </span>
            )}
          </Link>

          {/* Login / Logout */}
          {isLoggedIn ? (
            <button
              onClick={handleLogout}
              className="flex flex-col items-center gap-0.5 group"
            >
              <LogOut size={20} className="text-gray-700 group-hover:text-red-500 transition-colors" />
              <span className="text-[10px] text-gray-600 hidden sm:block">Logout</span>
            </button>
          ) : (
            <Link to="/login" className="flex flex-col items-center gap-0.5 group">
              <User size={20} className="text-gray-700 group-hover:text-blue-600 transition-colors" />
              <span className="text-[10px] text-gray-600 hidden sm:block">Login</span>
            </Link>
          )}

          {/* Mobile Toggle */}
          <button className="lg:hidden p-1" onClick={() => setIsMenuOpen(!isMenuOpen)}>
            {isMenuOpen ? <X size={22} className="text-gray-700" /> : <Menu size={22} className="text-gray-700" />}
          </button>
        </div>
      </div>

      {/* Mobile Menu */}
      {isMenuOpen && (
        <div className="lg:hidden bg-white border-t border-gray-200 px-4 py-3 space-y-1">
          {/* Mobile Search */}
          <div className="relative mb-3">
            <input
              type="text"
              placeholder="Search products..."
              className="w-full border border-gray-300 rounded py-2 pl-3 pr-9 text-sm focus:outline-none focus:border-blue-500"
              onFocus={() => { navigate('/products'); setIsMenuOpen(false); }}
            />
            <Search size={14} className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400" />
          </div>
          {navLinks.map(link => (
            <Link
              key={link.path}
              to={link.path}
              onClick={() => setIsMenuOpen(false)}
              className="block py-2 px-1 text-sm text-gray-700 hover:text-blue-600 border-b border-gray-100 last:border-0"
            >
              {link.title}
            </Link>
          ))}
          <Link to="/my-orders" onClick={() => setIsMenuOpen(false)} className="block py-2 px-1 text-sm text-gray-700 hover:text-blue-600 border-b border-gray-100">My Orders</Link>
          <Link to="/wishlist" onClick={() => setIsMenuOpen(false)} className="block py-2 px-1 text-sm text-gray-700 hover:text-blue-600 border-b border-gray-100">Wishlist</Link>
          {isLoggedIn ? (
            <button onClick={handleLogout} className="block w-full text-left py-2 px-1 text-sm text-red-600">
              Logout
            </button>
          ) : (
            <Link to="/login" onClick={() => setIsMenuOpen(false)} className="block py-2 px-1 text-sm text-blue-600 font-medium">
              Login / Sign Up
            </Link>
          )}
        </div>
      )}
    </nav>
  );
};

export default Navbar;
