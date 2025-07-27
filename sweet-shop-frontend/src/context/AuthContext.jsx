import React, { createContext, useState, useEffect } from "react";
import { jwtDecode } from "jwt-decode";
import { useNavigate } from "react-router-dom";

export const AuthContext = createContext();

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const storedToken = localStorage.getItem("token");
    if (storedToken) {
      try {
        const decoded = jwtDecode(storedToken);
        setUser(decoded);
        setToken(storedToken);
        if (decoded.role === "admin") navigate("/admin", { replace: true });
        else navigate("/dashboard", { replace: true });
      } catch {
        logout();
      }
    } else {
      navigate("/login", { replace: true });
    }
  }, []);

  const login = (jwtToken) => {
    try {
      const decoded = jwtDecode(jwtToken);
      setUser(decoded);
      setToken(jwtToken);
      localStorage.setItem("token", jwtToken);
      if (decoded.role === "admin") navigate("/admin", { replace: true });
      else navigate("/dashboard", { replace: true });
    } catch {
      alert("Invalid token");
    }
  };

  const logout = () => {
    setUser(null);
    setToken(null);
    localStorage.removeItem("token");
    navigate("/login", { replace: true });
  };

  const isAuthenticated = !!token;

  return (
    <AuthContext.Provider value={{ user, token, login, logout, isAuthenticated }}>
      {children}
    </AuthContext.Provider>
  );
}
