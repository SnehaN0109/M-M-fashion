import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'
import './index.css'
import { WishlistProvider } from './context/WishlistContext'  // 👈 add this
import { DomainProvider } from './context/DomainContext'
import { CartProvider } from './context/CartContext'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <DomainProvider>
      <WishlistProvider>   {/* 👈 wrap App */}
        <CartProvider>
          <App />
        </CartProvider>
      </WishlistProvider>
    </DomainProvider>
  </React.StrictMode>
)