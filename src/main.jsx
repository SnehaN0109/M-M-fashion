import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'
import './index.css'
import { WishlistProvider } from './context/WishlistContext'
import { DomainProvider } from './context/DomainContext'
import { CartProvider } from './context/CartContext'
import 'aos/dist/aos.css'
import AOS from 'aos'

AOS.init({ duration: 800, once: true })

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