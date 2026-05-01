import { createContext, useState, useEffect, useCallback } from "react";

export const CartContext = createContext();

const API = `${import.meta.env.VITE_API_URL}/api`;

/** Convert a DB cart row into the shape the rest of the app expects */
const dbRowToItem = (row, priceKey = "price_b2c") => ({
  id: row.product_id,
  name: row.name,
  image_url: row.image_url,
  category: row.category,
  price: row[priceKey] ?? row.price_b2c ?? 0,
  cartQuantity: row.quantity,
  cartId: row.cart_item_id,
  activeVariant: {
    id: row.variant_id,
    color: row.color,
    size: row.size,
    quantity: row.stock,
  },
});

export const CartProvider = ({ children }) => {
  const [cartItems, setCartItems] = useState(() => {
    const wa = localStorage.getItem("whatsapp_number");
    if (!wa) {
      const guestCart = localStorage.getItem("guest_cart");
      if (guestCart) {
        try { return JSON.parse(guestCart); } catch {}
      }
    }
    return [];
  });
  const [cartLoading, setCartLoading] = useState(false);

  const whatsapp = () => localStorage.getItem("whatsapp_number");
  const priceKey = () => {
    const hostname = window.location.hostname;
    let d = "garba.shop"; // default

    if (hostname.includes('ttd.in')) {
      d = 'ttd.in';
    } else if (hostname.includes('garba.shop')) {
      d = 'garba.shop';
    } else if (hostname.includes('maharashtra') || hostname.includes('maha')) {
      d = 'maharashtra';
    } else {
      // localhost fallback
      d = localStorage.getItem("test_domain") || "garba.shop";
    }

    if (d === "ttd.in") return "price_b2b_ttd";
    if (d === "maharashtra") return "price_b2b_maharashtra";
    return "price_b2c";
  };

  // ── Load cart from DB on mount (if logged in) ──────────────────────────────
  const loadCart = useCallback(async () => {
    const wa = whatsapp();
    if (!wa) return;
    setCartLoading(true);
    try {
      const res = await fetch(`${API}/cart?whatsapp_number=${encodeURIComponent(wa)}`);
      if (!res.ok) return;
      const rows = await res.json();
      const pk = priceKey();
      setCartItems(rows.map(r => dbRowToItem(r, pk)));
    } catch {
      // network error — keep cart empty, don't crash
    } finally {
      setCartLoading(false);
    }
  }, []);

  useEffect(() => { loadCart(); }, [loadCart]);

  // Sync guest cart to localStorage
  useEffect(() => {
    const wa = whatsapp();
    if (!wa) {
      localStorage.setItem("guest_cart", JSON.stringify(cartItems));
    }
  }, [cartItems]);

  // ── Add to cart ────────────────────────────────────────────────────────────
  const addToCart = async (product) => {
    const wa = whatsapp();
    const variantId = product.activeVariant?.id;

    // Optimistic update first so UI feels instant
    setCartItems(prev => {
      const existing = prev.find(
        i => i.id === product.id && i.activeVariant?.id === variantId
      );
      if (existing) {
        return prev.map(i =>
          i.id === product.id && i.activeVariant?.id === variantId
            ? { ...i, cartQuantity: i.cartQuantity + (product.cartQuantity || 1) }
            : i
        );
      }
      return [...prev, {
        ...product,
        cartId: Date.now() + Math.random(),
        cartQuantity: product.cartQuantity || 1,
      }];
    });

    // Sync to DB if logged in
    if (wa && variantId) {
      try {
        await fetch(`${API}/cart/add`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            whatsapp_number: wa,
            variant_id: variantId,
            quantity: product.cartQuantity || 1,
          }),
        });
      } catch {
        // silent — cart is still updated in context
      }
    }
  };

  // ── Remove from cart ───────────────────────────────────────────────────────
  const removeFromCart = async (productId, variantId) => {
    // Optimistic update
    setCartItems(prev =>
      prev.filter(i => !(i.id === productId && i.activeVariant?.id === variantId))
    );

    const wa = whatsapp();
    if (wa && variantId) {
      try {
        await fetch(`${API}/cart/remove`, {
          method: "DELETE",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ whatsapp_number: wa, variant_id: variantId }),
        });
      } catch {
        // silent
      }
    }
  };

  // ── Update quantity (now syncs to database) ───────────────────────────────
  const updateQuantity = async (productId, variantId, newQuantity) => {
    if (newQuantity < 1) return;
    
    // Optimistic update - update UI immediately
    setCartItems(prev =>
      prev.map(i =>
        i.id === productId && i.activeVariant?.id === variantId
          ? { ...i, cartQuantity: newQuantity }
          : i
      )
    );

    // Sync to database if logged in
    const wa = whatsapp();
    if (wa && variantId) {
      try {
        const res = await fetch(`${API}/cart/update`, {
          method: "PUT",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            whatsapp_number: wa,
            variant_id: variantId,
            quantity: newQuantity,
          }),
        });
        
        if (!res.ok) {
          const error = await res.json();
          console.error("Failed to update cart quantity:", error);
          // Optionally: revert optimistic update or show error to user
          // For now, we keep the optimistic update even if API fails
        }
      } catch (error) {
        console.error("Network error updating cart quantity:", error);
        // Silent fail - optimistic update remains
      }
    }
  };

  // ── Clear cart (called after order placed) ─────────────────────────────────
  const clearCart = async () => {
    setCartItems([]);
    const wa = whatsapp();
    if (wa) {
      try {
        await fetch(`${API}/cart/clear`, {
          method: "DELETE",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ whatsapp_number: wa }),
        });
      } catch {
        // silent
      }
    }
  };

  return (
    <CartContext.Provider
      value={{ cartItems, cartLoading, addToCart, removeFromCart, updateQuantity, clearCart, loadCart }}
    >
      {children}
    </CartContext.Provider>
  );
};
