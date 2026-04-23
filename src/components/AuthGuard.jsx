import { Navigate, useLocation } from "react-router-dom";

/**
 * Wraps protected routes. Redirects to /login if user is not logged in.
 * Passes the current path as redirectTo so user returns after login.
 */
const AuthGuard = ({ children }) => {
  const location = useLocation();
  const token = localStorage.getItem("auth_token");
  const whatsapp = localStorage.getItem("whatsapp_number");

  if (!token || !whatsapp) {
    return <Navigate to="/login" state={{ redirectTo: location.pathname }} replace />;
  }

  return children;
};

export default AuthGuard;
