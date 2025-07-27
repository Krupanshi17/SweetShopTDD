import React, { useContext, useEffect, useState } from "react";
import { AuthContext } from "../context/AuthContext";
import axios from "axios";
import { toast } from "react-toastify";

export default function Admin() {
  const { user, token, logout } = useContext(AuthContext);
  const [sweets, setSweets] = useState([]);
  const [loading, setLoading] = useState(true);

  // Modal state
  const [showModal, setShowModal] = useState(false);
  const [modalType, setModalType] = useState("add"); // "add" or "edit"
  const [currentSweet, setCurrentSweet] = useState(null);

  // Form state
  const [formData, setFormData] = useState({
    name: "",
    category: "",
    price: "",
    quantity: "",
  });

  useEffect(() => {
    fetchSweets();
  }, []);

  const fetchSweets = async () => {
    try {
      setLoading(true);
      const res = await axios.get("/api/sweets/", {
        headers: { Authorization: `Bearer ${token}` },
      });
      setSweets(res.data);
    } catch (err) {
      toast.error("Failed to fetch sweets");
    } finally {
      setLoading(false);
    }
  };

  const openAddModal = () => {
    setModalType("add");
    setFormData({ name: "", category: "", price: "", quantity: "" });
    setShowModal(true);
  };

  const openEditModal = (sweet) => {
    setModalType("edit");
    setCurrentSweet(sweet);
    setFormData({
      name: sweet.name,
      category: sweet.category,
      price: sweet.price,
      quantity: sweet.quantity,
    });
    setShowModal(true);
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleAdd = async (e) => {
    e.preventDefault();
    try {
      await axios.post(
        "/api/sweets/",
        {
          name: formData.name,
          category: formData.category,
          price: Number(formData.price),
          quantity: Number(formData.quantity),
        },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      toast.success("Sweet added");
      setShowModal(false);
      fetchSweets();
    } catch {
      toast.error("Failed to add sweet");
    }
  };

  const handleEdit = async (e) => {
    e.preventDefault();
    try {
      await axios.put(
        `/api/sweets/${currentSweet.id}`,
        {
          name: formData.name,
          category: formData.category,
          price: Number(formData.price),
          quantity: Number(formData.quantity),
        },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      toast.success("Sweet updated");
      setShowModal(false);
      fetchSweets();
    } catch {
      toast.error("Failed to update sweet");
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm("Delete this sweet?")) return;
    try {
      await axios.delete(`/api/sweets/${id}`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      toast.success("Sweet deleted");
      fetchSweets();
    } catch {
      toast.error("Failed to delete sweet");
    }
  };

  const handleRestock = async (id) => {
    const qty = prompt("Enter restock quantity:");
    const quantity = Number(qty);
    if (!quantity || quantity <= 0) {
      toast.error("Invalid quantity");
      return;
    }
    try {
      await axios.patch(
        `/api/sweets/${id}/restock`,
        { quantity },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      toast.success("Sweet restocked");
      fetchSweets();
    } catch {
      toast.error("Failed to restock");
    }
  };

  return (
    <div className="p-6 bg-background min-h-screen max-w-5xl mx-auto">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-3xl font-bold text-primaryDark">Admin Dashboard</h1>
        <button
          onClick={logout}
          className="bg-primaryDark text-accentCTA px-4 py-2 rounded hover:bg-secondary"
        >
          Logout
        </button>
      </div>

      <button
        onClick={openAddModal}
        className="mb-4 bg-accentCTA px-4 py-2 rounded hover:bg-secondary"
      >
        Add Sweet
      </button>

      {loading ? (
        <p>Loading sweets...</p>
      ) : sweets.length === 0 ? (
        <p>No sweets found.</p>
      ) : (
        <table className="w-full border-collapse">
          <thead>
            <tr className="bg-primaryDark text-accentCTA">
              <th className="p-2">Name</th>
              <th className="p-2">Category</th>
              <th className="p-2">Price</th>
              <th className="p-2">Quantity</th>
              <th className="p-2">Actions</th>
            </tr>
          </thead>
          <tbody>
            {sweets.map((sweet) => (
              <tr key={sweet.id} className="border-b">
                <td className="p-2">{sweet.name}</td>
                <td className="p-2">{sweet.category}</td>
                <td className="p-2">₹{sweet.price}</td>
                <td className="p-2">{sweet.quantity}</td>
                <td className="p-2 space-x-2">
                  <button
                    onClick={() => openEditModal(sweet)}
                    className="bg-secondary text-primaryDark px-2 py-1 rounded"
                  >
                    Edit
                  </button>
                  <button
                    onClick={() => handleDelete(sweet.id)}
                    className="bg-red-600 text-white px-2 py-1 rounded"
                  >
                    Delete
                  </button>
                  <button
                    onClick={() => handleRestock(sweet.id)}
                    className="bg-accentCTA px-2 py-1 rounded"
                  >
                    Restock
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}

      {/* Modal */}
      {showModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <form
            onSubmit={modalType === "add" ? handleAdd : handleEdit}
            className="bg-white p-6 rounded shadow-lg max-w-md w-full"
          >
            <h2 className="text-2xl font-bold mb-4">
              {modalType === "add" ? "Add Sweet" : "Edit Sweet"}
            </h2>

            <input
              name="name"
              value={formData.name}
              onChange={handleInputChange}
              placeholder="Name"
              className="w-full border p-2 mb-4 rounded"
              required
            />
            <input
              name="category"
              value={formData.category}
              onChange={handleInputChange}
              placeholder="Category"
              className="w-full border p-2 mb-4 rounded"
              required
            />
            <input
              name="price"
              type="number"
              min="0"
              value={formData.price}
              onChange={handleInputChange}
              placeholder="Price"
              className="w-full border p-2 mb-4 rounded"
              required
            />
            <input
              name="quantity"
              type="number"
              min="0"
              value={formData.quantity}
              onChange={handleInputChange}
              placeholder="Quantity"
              className="w-full border p-2 mb-4 rounded"
              required
            />

            <div className="flex justify-end space-x-4">
              <button
                type="button"
                onClick={() => setShowModal(false)}
                className="px-4 py-2 rounded border"
              >
                Cancel
              </button>
              <button
                type="submit"
                className="bg-primaryDark text-accentCTA px-4 py-2 rounded hover:bg-secondary"
              >
                {modalType === "add" ? "Add" : "Update"}
              </button>
            </div>
          </form>
        </div>
      )}
    </div>
  );
}
