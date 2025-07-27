import { Link } from "react-router-dom";

export default function Navbar() {
  return (
    <nav className="bg-primaryDark text-white flex justify-between px-6 py-3">
      <h1 className="font-lobster text-2xl">SweetShop</h1>
      <div className="flex gap-4">
        <Link to="/dashboard" className="hover:text-accentCTA">
          Dashboard
        </Link>
        <Link to="/cart" className="hover:text-accentCTA">
          Cart
        </Link>
        <Link to="/admin" className="hover:text-accentCTA">
          Admin
        </Link>
        <Link to="/login" className="hover:text-accentCTA">
          Logout
        </Link>
      </div>
    </nav>
  );
}
