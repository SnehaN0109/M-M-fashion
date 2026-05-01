import { useState, useContext } from "react";
import { useNavigate, Link } from "react-router-dom";
import { CartContext } from "../context/CartContext";
import { ShoppingBag, Trash2, Plus, Minus, ArrowRight, ShieldCheck, Truck, RefreshCw, Sparkles } from "lucide-react";

const CartPage = () => {
  const navigate = useNavigate();
  const { cartItems, removeFromCart, updateQuantity } = useContext(CartContext);
  const [coupon, setCoupon] = useState("");
  const [discountAmount, setDiscountAmount] = useState(0);

  const totalMRP = cartItems.reduce((total, item) => total + (item.price || 0) * (item.cartQuantity || 1), 0);
  const deliveryCharge = totalMRP > 999 || totalMRP === 0 ? 0 : 99;
  const finalTotal = totalMRP - discountAmount + deliveryCharge;

  if (cartItems.length === 0) {
    return (
      <div className="min-h-[80vh] flex flex-col items-center justify-center bg-white px-6">
        <div className="bg-gray-50 p-10 rounded-[50px] text-center max-w-md shadow-inner">
           <div className="w-24 h-24 bg-white rounded-full flex items-center justify-center mx-auto mb-8 shadow-xl">
              <ShoppingBag size={40} className="text-gray-300" />
           </div>
           <h1 className="text-4xl font-black text-gray-900 tracking-tighter mb-4">Your bag is empty.</h1>
           <p className="text-gray-500 font-medium mb-12">Looks like you haven't discovered your signature style yet.</p>
           <Link to="/products" className="inline-flex items-center gap-3 px-12 py-5 bg-gray-900 text-white font-black rounded-full hover:bg-black transition shadow-2xl active:scale-95">
             START EXPLORING <ArrowRight size={20} />
           </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-[#fafafa] min-h-screen">
      <div className="bg-white pt-16 pb-20 border-b border-gray-100">
        <div className="max-w-7xl mx-auto px-6 text-center">
           <span className="text-xs font-black text-pink-600 uppercase tracking-widest mb-4 block">Review Order</span>
           <h1 className="text-5xl font-black text-gray-900 tracking-tighter italic">Shopping Bag <span className="text-pink-600">.</span></h1>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-6 py-16 grid lg:grid-cols-12 gap-16">
        {/* Items List */}
        <div className="lg:col-span-8 space-y-8">
          {cartItems.map((item, index) => (
            <div key={index} className="bg-white rounded-[40px] p-8 shadow-sm border border-gray-100 flex flex-col md:flex-row gap-8 group transition-all hover:shadow-md">
              <div className="w-full md:w-48 aspect-[3/4] rounded-3xl overflow-hidden bg-gray-50 relative">
                <img src={item.image_url || (item.images && item.images[0]) || "https://via.placeholder.com/300"} alt={item.name} className="w-full h-full object-cover" />
                <div className="absolute top-4 left-4">
                   <div className="bg-white/90 backdrop-blur-sm p-2 rounded-full shadow-sm">
                      <Sparkles size={14} className="text-pink-600" />
                   </div>
                </div>
              </div>

              <div className="flex-1 flex flex-col">
                <div className="flex justify-between items-start mb-4">
                  <div>
                    <span className="text-[10px] font-black text-pink-600 uppercase tracking-widest block mb-1">{item.category}</span>
                    <h2 className="text-2xl font-black text-gray-900 tracking-tight group-hover:text-pink-600 transition-colors uppercase italic">{item.name}</h2>
                  </div>
                  <button onClick={() => removeFromCart(item.id, item.activeVariant?.id)} className="w-10 h-10 rounded-full flex items-center justify-center text-gray-400 hover:text-red-600 hover:bg-red-50 transition">
                    <Trash2 size={20} />
                  </button>
                </div>

                <div className="grid grid-cols-2 gap-4 mb-8">
                   <div className="bg-gray-50 px-4 py-2 rounded-2xl flex flex-col">
                      <span className="text-[9px] font-black text-gray-400 uppercase tracking-widest">Shade</span>
                      <span className="text-xs font-bold text-gray-800">{item.activeVariant?.color || "Default"}</span>
                   </div>
                   <div className="bg-gray-50 px-4 py-2 rounded-2xl flex flex-col">
                      <span className="text-[9px] font-black text-gray-400 uppercase tracking-widest">Size</span>
                      <span className="text-xs font-bold text-gray-800">{item.activeVariant?.size || "One Size"}</span>
                   </div>
                </div>

                <div className="mt-auto flex items-center justify-between border-t border-gray-50 pt-6">
                   <div className="flex items-center bg-gray-100 p-1.5 rounded-2xl">
                     <button onClick={() => updateQuantity(item.id, item.activeVariant?.id, Math.max(1, item.cartQuantity - 1))} className="w-10 h-10 flex items-center justify-center bg-white rounded-xl shadow-sm hover:text-pink-600 transition"><Minus size={16} /></button>
                     <span className="w-12 text-center font-black text-lg">{item.cartQuantity}</span>
                     <button onClick={() => updateQuantity(item.id, item.activeVariant?.id, item.cartQuantity + 1)} className="w-10 h-10 flex items-center justify-center bg-white rounded-xl shadow-sm hover:text-pink-600 transition"><Plus size={16} /></button>
                   </div>
                   <div className="text-right">
                      <p className="text-[10px] font-black text-gray-400 uppercase tracking-widest">Total</p>
                      <p className="text-2xl font-black text-gray-900 italic">₹{(item.price * item.cartQuantity).toLocaleString()}</p>
                   </div>
                </div>
              </div>
            </div>
          ))}
          
          <Link to="/products" className="flex items-center gap-3 text-sm font-black text-gray-400 uppercase tracking-widest hover:text-pink-600 transition py-4">
             <ArrowRight size={18} className="rotate-180" /> Continue Curating
          </Link>
        </div>

        {/* Recap Panel */}
        <div className="lg:col-span-4 lg:sticky lg:top-24 h-fit">
          <div className="bg-gray-900 text-white rounded-[40px] p-10 shadow-2xl relative overflow-hidden">
            <div className="absolute top-0 right-0 p-12 opacity-10 blur-3xl pointer-events-none">
               <div className="w-64 h-64 bg-pink-500 rounded-full" />
            </div>

            <h2 className="text-3xl font-black tracking-tighter italic mb-10 relative z-10">Order Recap</h2>

            <div className="space-y-6 text-sm relative z-10">
              <div className="flex justify-between items-center text-gray-400">
                <span className="font-bold uppercase tracking-widest text-[10px]">Subtotal ({cartItems.length})</span>
                <span className="font-black text-white">₹{totalMRP.toLocaleString()}</span>
              </div>
              <div className="flex justify-between items-center text-gray-400">
                <span className="font-bold uppercase tracking-widest text-[10px]">Shipping</span>
                <span className={deliveryCharge === 0 ? "text-green-400 font-black uppercase" : "text-white font-black"}>
                   {deliveryCharge === 0 ? "Complimentary" : `₹${deliveryCharge}`}
                </span>
              </div>
              {discountAmount > 0 && (
                <div className="flex justify-between items-center text-green-400">
                  <span className="font-bold uppercase tracking-widest text-[10px]">Privilege Discount</span>
                  <span className="font-black">-₹{discountAmount.toLocaleString()}</span>
                </div>
              )}
            </div>

            <hr className="my-10 border-gray-800 relative z-10" />

            <div className="flex justify-between items-end mb-12 relative z-10">
               <div>
                 <p className="text-[10px] font-bold text-gray-500 uppercase tracking-[0.2em] mb-1">Total Balance</p>
                 <p className="text-5xl font-black tracking-tighter italic">₹{finalTotal.toLocaleString()}</p>
               </div>
            </div>

            <button className="w-full bg-pink-600 hover:bg-pink-700 text-white py-6 rounded-full font-black text-lg shadow-xl active:scale-95 transition-all relative z-10 group flex items-center justify-center gap-4">
              SECURE CHECKOUT
              <ArrowRight size={24} className="group-hover:translate-x-2 transition-transform" />
            </button>

            <div className="mt-12 grid grid-cols-3 gap-4 text-[8px] font-black text-gray-500 uppercase tracking-widest text-center opacity-70 relative z-10">
               <div className="space-y-2 flex flex-col items-center">
                 <ShieldCheck size={20} className="mb-1 text-gray-400" />
                 Secure
               </div>
               <div className="space-y-2 flex flex-col items-center">
                 <Truck size={20} className="mb-1 text-gray-400" />
                 Express
               </div>
               <div className="space-y-2 flex flex-col items-center">
                 <RefreshCw size={20} className="mb-1 text-gray-400" />
                 Returns
               </div>
            </div>
          </div>
          
          <div className="mt-8 bg-white rounded-3xl p-6 border border-gray-100 shadow-sm flex flex-col gap-4">
             <span className="text-[10px] font-black text-gray-400 uppercase tracking-widest">Privilege Code</span>
             <div className="flex gap-2">
               <input 
                 type="text" 
                 placeholder="Enter Code" 
                 className="flex-1 bg-gray-50 border-none rounded-xl px-4 py-3 text-sm focus:ring-2 ring-pink-500"
                 value={coupon}
                 onChange={(e) => setCoupon(e.target.value)}
               />
               <button onClick={() => { if(coupon === "FIRST10") setDiscountAmount(totalMRP*0.1); else alert("Invalid Code"); }} className="px-6 py-3 bg-gray-100 font-bold rounded-xl hover:bg-pink-600 hover:text-white transition">Apply</button>
             </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default CartPage;