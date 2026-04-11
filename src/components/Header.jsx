import { Link, NavLink, useNavigate } from "react-router-dom";
import { useState, useContext } from "react";
import { WishlistContext } from "../context/WishlistContext";
import { CartContext } from "../context/CartContext";

const Header = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [searchTerm, setSearchTerm] = useState("");
  const { wishlist } = useContext(WishlistContext);
  const { cartItems } = useContext(CartContext);
  const navigate = useNavigate();

  const cartItemCount = cartItems.reduce((total, item) => total + (item.cartQuantity || 1), 0);

  /* ===== Sample Products for Suggestions ===== */
  const products = [
    "Lehenga for Women",
    "Lehenga for Girls",
    "Lehenga Dupatta",
    "Lehenga Choli",
    "Red Garba Dress",
    "Blue Ethnic Kurti",
    "Green Lehenga",
  ];

  /* ===== Filter Suggestions ===== */
  const filteredSuggestions = products.filter((item) =>
    item.toLowerCase().includes(searchTerm.toLowerCase())
  );

  /* ===== Search Submit ===== */
  const handleSearch = () => {
    if (searchTerm.trim() !== "") {
      navigate(`/search?query=${searchTerm}`);
      setSearchTerm("");
    }
  };

  /* ===== When Click Suggestion ===== */
  const handleSelect = (value) => {
    navigate(`/search?query=${value}`);
    setSearchTerm("");
  };

  const navLinkStyle =
    "block py-2 px-3 rounded hover:bg-pink-100 transition";

  const activeStyle =
    "bg-pink-500 text-white";

  const categoryStyle =
    "text-sm font-medium cursor-pointer hover:text-pink-600 transition";

  return (
    <header className="border-b sticky top-0 bg-white z-50 shadow-sm">

      {/* ===== TOP NAVBAR ===== */}
      <div className="max-w-7xl mx-auto px-6 py-4 flex justify-between items-center">

        {/* Logo */}
        <Link to="/" className="text-2xl font-bold text-pink-600">
          garba.shop
        </Link>

        {/* Desktop Menu */}
        <nav className="hidden md:flex gap-4 text-sm font-medium">

          <NavLink to="/" className={({ isActive }) =>
            `${navLinkStyle} ${isActive ? activeStyle : ""}`
          }>Home</NavLink>

          <NavLink to="/products" className={({ isActive }) =>
            `${navLinkStyle} ${isActive ? activeStyle : ""}`
          }>Products</NavLink>

          <NavLink
            to="/cart"
            className={({ isActive }) =>
              `${navLinkStyle} ${isActive ? activeStyle : ""} relative`
            }
          >
            Cart
            {cartItemCount > 0 && (
              <span className="absolute -top-2 -right-3 bg-red-500 text-white text-xs px-2 py-0.5 rounded-full">
                {cartItemCount}
              </span>
            )}
          </NavLink>

          <NavLink
            to="/wishlist"
            className={({ isActive }) =>
              `${navLinkStyle} ${isActive ? activeStyle : ""} relative`
            }
          >
            Wishlist
            {wishlist.length > 0 && (
              <span className="absolute -top-2 -right-3 bg-red-500 text-white text-xs px-2 py-0.5 rounded-full">
                {wishlist.length}
              </span>
            )}
          </NavLink>

          <NavLink to="/my-orders" className={({ isActive }) =>
            `${navLinkStyle} ${isActive ? activeStyle : ""}`
          }>My Orders</NavLink>

          <NavLink to="/upload-photos" className={({ isActive }) =>
            `${navLinkStyle} ${isActive ? activeStyle : ""}`
          }>Upload Photos</NavLink>

          <NavLink to="/about-us" className={({ isActive }) =>
            `${navLinkStyle} ${isActive ? activeStyle : ""}`
          }>About</NavLink>

          <NavLink to="/contact-us" className={({ isActive }) =>
            `${navLinkStyle} ${isActive ? activeStyle : ""}`
          }>Contact</NavLink>

          <NavLink to="/login" className={({ isActive }) =>
            `${navLinkStyle} ${isActive ? activeStyle : ""}`
          }>Login</NavLink>

        </nav>

        {/* Mobile Button */}
        <button
          className="md:hidden text-2xl"
          onClick={() => setIsOpen(!isOpen)}
        >
          ☰
        </button>
      </div>

      {/* ===== SEARCH BAR WITH DROPDOWN ===== */}
      <div className="w-full flex justify-center py-4 bg-gray-50 border-t relative">
        <div className="w-[90%] md:w-2/3 relative">
          <input
            type="text"
            placeholder="Search by product, fabric, occasion..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleSearch()}
            className="w-full px-5 py-3 rounded-full border border-gray-300 focus:outline-none focus:ring-2 focus:ring-pink-500 transition"
          />

          {searchTerm && filteredSuggestions.length > 0 && (
            <div className="absolute w-full bg-white border mt-2 rounded-lg shadow-lg z-50 max-h-60 overflow-y-auto">
              {filteredSuggestions.map((item, index) => (
                <div
                  key={index}
                  onClick={() => handleSelect(item)}
                  className="px-4 py-2 hover:bg-pink-100 cursor-pointer transition"
                >
                  {item}
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* ===== CATEGORY BAR ===== */}
      <div className="w-full bg-white border-t">
        <div className="max-w-7xl mx-auto px-6 py-3 flex justify-center gap-8 overflow-x-auto">
          <Link to="/men" className={categoryStyle}>Men</Link>
          <Link to="/women" className={categoryStyle}>Women</Link>
          <Link to="/kids" className={categoryStyle}>Kids</Link>
          <Link to="/ethnic" className={categoryStyle}>Ethnic</Link>
          <Link to="/western" className={categoryStyle}>Western</Link>
          <Link to="/party-wear" className={categoryStyle}>Party Wear</Link>
        </div>
      </div>

      {/* ===== MOBILE MENU ===== */}
      {isOpen && (
        <div className="md:hidden bg-white border-t px-6 py-4 space-y-2 text-sm">

          <NavLink to="/" onClick={() => setIsOpen(false)} className={navLinkStyle}>Home</NavLink>
          <NavLink to="/products" onClick={() => setIsOpen(false)} className={navLinkStyle}>Products</NavLink>
          
          <NavLink
            to="/cart"
            onClick={() => setIsOpen(false)}
            className="relative block py-2 px-3 rounded hover:bg-pink-100 transition"
          >
            Cart
            {cartItemCount > 0 && (
              <span className="ml-2 bg-red-500 text-white text-xs px-2 py-0.5 rounded-full">
                {cartItemCount}
              </span>
            )}
          </NavLink>

          <NavLink
            to="/wishlist"
            onClick={() => setIsOpen(false)}
            className="relative block py-2 px-3 rounded hover:bg-pink-100 transition"
          >
            Wishlist
            {wishlist.length > 0 && (
              <span className="ml-2 bg-red-500 text-white text-xs px-2 py-0.5 rounded-full">
                {wishlist.length}
              </span>
            )}
          </NavLink>

          <NavLink to="/my-orders" onClick={() => setIsOpen(false)} className={navLinkStyle}>My Orders</NavLink>
          <NavLink to="/upload-photos" onClick={() => setIsOpen(false)} className={navLinkStyle}>Upload Photos</NavLink>
          <NavLink to="/about-us" onClick={() => setIsOpen(false)} className={navLinkStyle}>About</NavLink>
          <NavLink to="/contact-us" onClick={() => setIsOpen(false)} className={navLinkStyle}>Contact</NavLink>
          <NavLink to="/login" onClick={() => setIsOpen(false)} className={navLinkStyle}>Login</NavLink>

        </div>
      )}

    </header>
  );
};

export default Header;