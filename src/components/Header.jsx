import { Link, NavLink, useNavigate } from "react-router-dom";
import { useState, useContext, useEffect } from "react";
import { WishlistContext } from "../context/WishlistContext";
import { CartContext } from "../context/CartContext";
import { useDomain } from "../context/DomainContext";
import { ShoppingCart, Heart, Search, Menu, X, User, LogOut, Package } from "lucide-react";
const Header = () => {
  const [menuOpen, setMenuOpen] = useState(false);
  const [searchTerm, setSearchTerm] = useState("");
  const [searchFocused, setSearchFocused] = useState(false);
  const [suggestions, setSuggestions] = useState([]);
  const { wishlist, clearWishlist } = useContext(WishlistContext);
  const { cartItems, resetCart } = useContext(CartContext);
  const { brandName, tagline, isB2B } = useDomain();
  const navigate = useNavigate();

  const cartCount = cartItems.reduce((t, i) => t + (i.cartQuantity || 1), 0);
  const isLoggedIn = !!localStorage.getItem("auth_token");

  const handleLogout = () => {
    // 1. Clear in-memory state for this user — other users' data stays in localStorage
    clearWishlist();
    resetCart();
    // 2. Remove auth keys
    localStorage.removeItem("auth_token");
    localStorage.removeItem("user_id");
    localStorage.removeItem("whatsapp_number");
    navigate("/login");
  };

  const handleSearch = (e) => {
    e.preventDefault();
    if (searchTerm.trim()) {
      navigate(`/search?query=${encodeURIComponent(searchTerm.trim())}`);
      setSearchTerm("");
      setSearchFocused(false);
      setSuggestions([]);
    }
  };

  useEffect(() => {
    if (searchTerm.trim().length > 1) {
      const fetchSuggestions = async () => {
        try {
          const res = await fetch(`${import.meta.env.VITE_API_URL}/api/products/?search=${encodeURIComponent(searchTerm.trim())}`);
          if (res.ok) {
            const data = await res.json();
            setSuggestions(data.slice(0, 5));
          }
        } catch { /* ignore */ }
      };
      const debounce = setTimeout(fetchSuggestions, 300);
      return () => clearTimeout(debounce);
    } else {
      setSuggestions([]);
    }
  }, [searchTerm]);

  const navLink = ({ isActive }) =>
    `text-sm font-bold transition-colors ${isActive ? "text-pink-600" : "text-gray-600 hover:text-pink-600"}`;

  const categories = [
    { label: "Men", to: "/men" },
    { label: "Women", to: "/women" },
    { label: "Kids", to: "/kids" },
    { label: "Ethnic", to: "/ethnic" },
    { label: "Western", to: "/western" },
    { label: "Party Wear", to: "/party-wear" },
  ];

  return (
    <header className="sticky top-0 z-50 bg-white border-b shadow-sm">

      {/* ── Main bar ── */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 h-16 flex items-center gap-4">

        {/* Logo / Brand */}
        <Link to="/" className="flex-shrink-0 flex flex-col leading-tight">
          <span className="text-xl font-black text-pink-600 tracking-tight">{brandName}</span>
          {tagline && <span className="text-[10px] text-gray-400 font-medium hidden sm:block">{tagline}</span>}
        </Link>

        {/* Search — desktop */}
        <form onSubmit={handleSearch} className="hidden md:flex flex-1 max-w-xl mx-auto relative">
          <input
            type="text"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            onFocus={() => setSearchFocused(true)}
            onBlur={() => setTimeout(() => setSearchFocused(false), 150)}
            placeholder="Search products, fabrics, occasions..."
            className="w-full pl-5 pr-12 py-2.5 rounded-full border border-gray-200 bg-gray-50 text-sm focus:outline-none focus:ring-2 focus:ring-pink-400 focus:bg-white transition"
          />
          <button type="submit" className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-pink-600">
            <Search size={18} />
          </button>
          
          {searchFocused && suggestions.length > 0 && (
            <div className="absolute top-full mt-2 w-full bg-white border border-gray-100 rounded-2xl shadow-xl overflow-hidden py-2 z-50">
              {suggestions.map((p) => (
                <div 
                  key={p.id} 
                  onMouseDown={() => { navigate(`/products/${p.id}`); setSearchFocused(false); setSearchTerm(""); setSuggestions([]); }}
                  className="px-5 py-3 hover:bg-gray-50 cursor-pointer flex items-center gap-3 transition"
                >
                  {p.image_url && <img src={p.image_url} alt="" className="w-10 h-12 object-cover rounded-md" />}
                  <div>
                    <p className="text-sm font-bold text-gray-900">{p.name}</p>
                    <p className="text-xs text-gray-400 uppercase tracking-widest">{p.category}</p>
                  </div>
                </div>
              ))}
            </div>
          )}
        </form>

        {/* Right icons */}
        <div className="ml-auto flex items-center gap-1 sm:gap-2">

          {/* Search icon — mobile */}
          <button
            className="md:hidden p-2 rounded-xl hover:bg-gray-100 text-gray-600"
            onClick={() => navigate("/search")}
          >
            <Search size={20} />
          </button>

          {/* My Orders */}
          <Link to="/my-orders" className="hidden sm:flex items-center gap-1.5 px-3 py-2 rounded-xl hover:bg-gray-100 text-gray-600 hover:text-pink-600 transition" title="My Orders">
            <Package size={18} />
            <span className="text-xs font-bold hidden lg:inline">Orders</span>
          </Link>

          {/* Wishlist */}
          <Link to="/wishlist" className="relative p-2 rounded-xl hover:bg-gray-100 text-gray-600 hover:text-pink-600 transition">
            <Heart size={20} />
            {wishlist.length > 0 && (
              <span className="absolute -top-0.5 -right-0.5 w-4 h-4 bg-pink-600 text-white text-[10px] font-black rounded-full flex items-center justify-center">
                {wishlist.length > 9 ? "9+" : wishlist.length}
              </span>
            )}
          </Link>

          {/* Cart */}
          <Link to="/cart" className="relative p-2 rounded-xl hover:bg-gray-100 text-gray-600 hover:text-pink-600 transition">
            <ShoppingCart size={20} />
            {cartCount > 0 && (
              <span className="absolute -top-0.5 -right-0.5 w-4 h-4 bg-pink-600 text-white text-[10px] font-black rounded-full flex items-center justify-center">
                {cartCount > 9 ? "9+" : cartCount}
              </span>
            )}
          </Link>

          {/* Account / Logout */}
          {isLoggedIn ? (
            <button onClick={handleLogout} className="p-2 rounded-xl hover:bg-gray-100 text-gray-600 hover:text-red-500 transition" title="Logout">
              <LogOut size={20} />
            </button>
          ) : (
            <Link to="/login" className="p-2 rounded-xl hover:bg-gray-100 text-gray-600 hover:text-pink-600 transition">
              <User size={20} />
            </Link>
          )}

          {/* Hamburger */}
          <button
            className="md:hidden p-2 rounded-xl hover:bg-gray-100 text-gray-600"
            onClick={() => setMenuOpen(!menuOpen)}
          >
            {menuOpen ? <X size={20} /> : <Menu size={20} />}
          </button>
        </div>
      </div>

      {/* ── Category bar — desktop ── */}
      <div className="hidden md:block border-t bg-white">
        <div className="max-w-7xl mx-auto px-6 flex items-center gap-1 h-10 overflow-x-auto">
          {categories.map(({ label, to }) => (
            <NavLink key={to} to={to}
              className={({ isActive }) =>
                `px-4 py-1.5 rounded-full text-xs font-black uppercase tracking-widest transition whitespace-nowrap ${
                  isActive ? "bg-pink-600 text-white" : "text-gray-500 hover:text-pink-600 hover:bg-pink-50"
                }`
              }
            >
              {label}
            </NavLink>
          ))}
          {/* B2B badge */}
          {isB2B && (
            <span className="ml-auto text-[10px] font-black px-3 py-1 bg-indigo-100 text-indigo-700 rounded-full uppercase tracking-widest">
              B2B Wholesale
            </span>
          )}
        </div>
      </div>

      {/* ── Mobile menu ── */}
      {menuOpen && (
        <div className="md:hidden border-t bg-white px-4 py-4 space-y-1">
          {/* Mobile search */}
          <form onSubmit={handleSearch} className="flex gap-2 mb-3">
            <input
              type="text"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              placeholder="Search..."
              className="flex-1 border rounded-xl px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-pink-400"
            />
            <button type="submit" className="px-4 py-2 bg-pink-600 text-white rounded-xl text-sm font-bold">Go</button>
          </form>

          {/* Nav links */}
          {[
            { label: "Home", to: "/" },
            { label: "Products", to: "/products" },
            { label: "My Orders", to: "/my-orders" },
            { label: "Wishlist", to: "/wishlist" },
            { label: "Login", to: "/login" },
          ].map(({ label, to }) => (
            <NavLink key={to} to={to} onClick={() => setMenuOpen(false)}
              className={({ isActive }) =>
                `block px-4 py-2.5 rounded-xl text-sm font-bold transition ${
                  isActive ? "bg-pink-50 text-pink-600" : "text-gray-700 hover:bg-gray-50"
                }`
              }
            >
              {label}
            </NavLink>
          ))}

          {/* Categories */}
          <div className="pt-2 border-t mt-2">
            <p className="text-[10px] font-black text-gray-400 uppercase tracking-widest px-4 mb-2">Categories</p>
            <div className="flex flex-wrap gap-2 px-2">
              {categories.map(({ label, to }) => (
                <Link key={to} to={to} onClick={() => setMenuOpen(false)}
                  className="px-3 py-1.5 bg-gray-100 rounded-full text-xs font-bold text-gray-700 hover:bg-pink-50 hover:text-pink-600 transition"
                >
                  {label}
                </Link>
              ))}
            </div>
          </div>
        </div>
      )}
    </header>
  );
};

export default Header;
