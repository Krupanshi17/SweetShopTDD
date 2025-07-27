import React, { useContext, useEffect, useState } from "react";
import { AuthContext } from "../context/AuthContext";
import { CartContext } from "../context/CartContext";
import axios from "axios";

export default function Dashboard() {
  const { user, logout, token } = useContext(AuthContext);
  const { addToCart } = useContext(CartContext);

  const [sweets, setSweets] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState("");

  useEffect(() => {
    fetchSweets();
  }, []);

  const fetchSweets = async () => {
    try {
      setLoading(true);
      const response = await axios.get("/api/sweets/", {
        headers: { Authorization: `Bearer ${token}` },
      });
      setSweets(response.data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const filteredSweets = sweets.filter(
    (s) =>
      s.name.toLowerCase().includes(search.toLowerCase()) ||
      s.category.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="p-6 bg-background min-h-screen">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold text-primaryDark">
          Welcome, {user?.username || "User"}!
        </h1>
        <button
          onClick={logout}
          className="bg-primaryDark text-accentCTA px-4 py-2 rounded hover:bg-secondary"
        >
          Logout
        </button>
      </div>

      <input
        type="text"
        placeholder="Search sweets by name or category..."
        value={search}
        onChange={(e) => setSearch(e.target.value)}
        className="w-full max-w-md p-2 border rounded mb-6"
      />

      {loading ? (
        <div>Loading sweets...</div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {filteredSweets.length ? (
            filteredSweets.map((sweet) => (
              <div key={sweet.id} className="bg-white p-4 rounded shadow">
                <h2 className="font-bold text-lg">{sweet.name}</h2>
                <p>Category: {sweet.category}</p>
                <p>Price: ₹{sweet.price}</p>
                <p>Quantity: {sweet.quantity}</p>
                <button
                  disabled={sweet.quantity === 0}
                  onClick={() => addToCart(sweet)}
                  className={`mt-2 w-full py-1 rounded font-semibold ${
                    sweet.quantity === 0
                      ? "bg-gray-400 cursor-not-allowed"
                      : "bg-accentCTA hover:bg-secondary"
                  }`}
                >
                  Buy
                </button>
              </div>
            ))
          ) : (
            <p>No sweets found.</p>
          )}
        </div>
      )}
    </div>
  );
}
