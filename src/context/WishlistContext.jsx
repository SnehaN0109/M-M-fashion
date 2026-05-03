import { createContext, useState, useCallback } from "react";

export const WishlistContext = createContext();

const API = `${import.meta.env.VITE_API_URL}/api`;

const whatsapp = () => localStorage.getItem("whatsapp_number");

export const WishlistProvider = ({ children }) => {
  // wishlist items — shape: [{ id, name, image_url, category, ... }]
  const [wishlist, setWishlist] = useState([]);

  // ── Load from DB (called on login and on mount if logged in) ──────────────
  const loadWishlistForUser = useCallback(async () => {
    const wa = whatsapp();
    if (!wa) {
      setWishlist([]);
      return;
    }
    try {
      const res = await fetch(`${API}/wishlist?whatsapp_number=${encodeURIComponent(wa)}`);
      if (!res.ok) return;
      const data = await res.json();
      setWishlist(data);
    } catch {
      // network error — keep current state
    }
  }, []);

  // ── Add to wishlist ───────────────────────────────────────────────────────
  const addToWishlist = async (product) => {
    // Optimistic update
    setWishlist(prev =>
      prev.some(i => i.id === product.id) ? prev : [...prev, product]
    );

    const wa = whatsapp();
    if (!wa) return; // guest — localStorage only (no DB for guests)

    try {
      await fetch(`${API}/wishlist`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          whatsapp_number: wa,
          product_id: product.id,
        }),
      });
    } catch {
      // silent — optimistic update stays
    }
  };

  // ── Remove from wishlist ──────────────────────────────────────────────────
  const removeFromWishlist = async (productId) => {
    // Optimistic update
    setWishlist(prev => prev.filter(i => i.id !== productId));

    const wa = whatsapp();
    if (!wa) return;

    try {
      await fetch(`${API}/wishlist/${productId}?whatsapp_number=${encodeURIComponent(wa)}`, {
        method: "DELETE",
      });
    } catch {
      // silent
    }
  };

  // ── Clear in-memory state on logout ──────────────────────────────────────
  // DB data is preserved — restored on next login via loadWishlistForUser()
  const clearWishlist = () => {
    setWishlist([]);
  };

  return (
    <WishlistContext.Provider
      value={{
        wishlist,
        addToWishlist,
        removeFromWishlist,
        clearWishlist,
        loadWishlistForUser,
      }}
    >
      {children}
    </WishlistContext.Provider>
  );
};
