import { Navigate } from "react-router-dom";

/**
 * Wraps any admin route. Redirects to /admin/login if not authenticated.
 * Auth token is stored in localStorage as "admin_token".
 */
const AdminGuard = ({ children }) => {
  const token = localStorage.getItem("admin_token");
  if (!token) return <Navigate to="/admin-login" replace />;
  return children;
};

export default AdminGuard;
