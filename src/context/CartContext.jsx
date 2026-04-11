import React, { createContext, useState, useEffect } from "react";

export const CartContext = createContext();

export const CartProvider = ({ children }) => {
  const [cartItems, setCartItems] = useState(() => {
    const localData = localStorage.getItem("cartItems");
    return localData ? JSON.parse(localData) : [];
  });

  useEffect(() => {
    localStorage.setItem("cartItems", JSON.stringify(cartItems));
  }, [cartItems]);

  const addToCart = (product) => {
    setCartItems((prev) => {
      // Find if this exact product AND variant already exist in the cart
      const existing = prev.find(
        (item) =>
          item.id === product.id &&
          item.activeVariant?.id === product.activeVariant?.id
      );
      
      if (existing) {
        // Just increase the quantity of the existing stack
        return prev.map((item) =>
          item.id === product.id &&
          item.activeVariant?.id === product.activeVariant?.id
            ? {
                ...item,
                cartQuantity: item.cartQuantity + (product.cartQuantity || 1),
              }
            : item
        );
      }
      
      // If it's a completely new variant or product, append it with a unique cartId
      return [
        ...prev,
        { ...product, cartId: Date.now() + Math.random(), cartQuantity: product.cartQuantity || 1 },
      ];
    });
  };

  const removeFromCart = (productId, variantId) => {
    setCartItems((prev) =>
      prev.filter(
        (item) =>
          !(item.id === productId && item.activeVariant?.id === variantId)
      )
    );
  };

  const updateQuantity = (productId, variantId, newQuantity) => {
    if (newQuantity < 1) return;
    setCartItems((prev) =>
      prev.map((item) =>
        item.id === productId && item.activeVariant?.id === variantId
          ? { ...item, cartQuantity: newQuantity }
          : item
      )
    );
  };

  const clearCart = () => setCartItems([]);

  return (
    <CartContext.Provider
      value={{ cartItems, addToCart, removeFromCart, updateQuantity, clearCart }}
    >
      {children}
    </CartContext.Provider>
  );
};
