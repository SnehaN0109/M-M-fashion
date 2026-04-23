import { useState } from "react";
import { Globe } from "lucide-react";

const DOMAINS = [
  { key: "garba.shop",  label: "garba.shop",  badge: "B2C" },
  { key: "ttd.in",      label: "ttd.in",      badge: "B2B" },
  { key: "maharashtra", label: "maharashtra", badge: "B2B" },
];

const DevDomainSwitcher = () => {
  const [open, setOpen] = useState(false);
  const current = localStorage.getItem("test_domain") || "garba.shop";
  const currentDomain = DOMAINS.find(d => d.key === current) || DOMAINS[0];

  // Hide on production — only show on localhost
  if (window.location.hostname !== "localhost") return null;

  const switchDomain = (key) => {
    localStorage.setItem("test_domain", key);
    window.location.reload();
  };

  return (
    <div className="fixed bottom-5 right-5 z-[9999] flex flex-col items-end gap-2">
      {open && (
        <div className="bg-white border border-gray-200 rounded-2xl shadow-xl overflow-hidden w-48">
          <p className="text-[10px] font-black text-gray-400 uppercase tracking-widest px-4 pt-3 pb-1">
            Switch Domain
          </p>
          {DOMAINS.map(({ key, label, badge }) => (
            <button
              key={key}
              onClick={() => switchDomain(key)}
              className={`w-full flex items-center justify-between px-4 py-2.5 text-sm font-bold transition hover:bg-gray-50 ${
                current === key ? "text-pink-600 bg-pink-50" : "text-gray-700"
              }`}
            >
              <span>{label}</span>
              <span className={`text-[10px] font-black px-2 py-0.5 rounded-full ${
                badge === "B2C" ? "bg-pink-100 text-pink-600" : "bg-indigo-100 text-indigo-600"
              }`}>
                {badge}
              </span>
            </button>
          ))}
        </div>
      )}

      <button
        onClick={() => setOpen(o => !o)}
        className="flex items-center gap-2 bg-gray-900 text-white text-xs font-black px-4 py-2.5 rounded-full shadow-lg hover:bg-gray-700 transition"
      >
        <Globe size={14} />
        {currentDomain.label}
      </button>
    </div>
  );
};

export default DevDomainSwitcher;
