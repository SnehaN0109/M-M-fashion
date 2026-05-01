import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Loader2, Lock } from "lucide-react";

const AdminLoginPage = () => {
  const navigate = useNavigate();
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    try {
      const res = await fetch("http://localhost:5000/api/admin/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ password }),
      });
      const data = await res.json();
      if (!res.ok) { setError(data.error || "Invalid password"); return; }
      localStorage.setItem("admin_token", data.token);
      navigate("/admin");
    } catch {
      setError("Could not connect to server.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center px-6">
      <div className="w-full max-w-sm bg-white rounded-3xl shadow-xl p-10 space-y-8">
        <div className="text-center space-y-2">
          <div className="w-14 h-14 bg-pink-50 rounded-2xl flex items-center justify-center mx-auto">
            <Lock size={24} className="text-pink-600" />
          </div>
          <h1 className="text-2xl font-black text-gray-900">Admin Login</h1>
          <p className="text-sm text-gray-400">M&amp;M Fashion Dashboard</p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="text-xs font-black text-gray-400 uppercase tracking-widest block mb-1.5">
              Password
            </label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Enter admin password"
              required
              autoFocus
              className="w-full border border-gray-200 rounded-2xl px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-pink-500"
            />
          </div>

          {error && (
            <p className="text-red-500 text-sm font-bold text-center">{error}</p>
          )}

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-pink-600 hover:bg-pink-700 text-white font-black py-3.5 rounded-2xl flex items-center justify-center gap-2 disabled:opacity-50 transition-all"
          >
            {loading && <Loader2 size={18} className="animate-spin" />}
            {loading ? "Verifying..." : "Login"}
          </button>
        </form>
      </div>
    </div>
  );
};

export default AdminLoginPage;
