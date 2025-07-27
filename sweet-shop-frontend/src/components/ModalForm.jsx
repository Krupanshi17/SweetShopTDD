import { useState, useEffect } from 'react';

export default function ModalForm({ isOpen, onClose, onSubmit, initialData }) {
  const [formData, setFormData] = useState({
    name: '',
    category: '',
    price: '',
    quantity: '',
  });

  useEffect(() => {
    if (initialData) {
      setFormData({
        name: initialData.name || '',
        category: initialData.category || '',
        price: initialData.price || '',
        quantity: initialData.quantity || '',
      });
    }
  }, [initialData]);

  const handleChange = (e) =>
    setFormData({ ...formData, [e.target.name]: e.target.value });

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(formData);
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 z-40 flex items-center justify-center">
      <div className="bg-white p-6 rounded-md shadow-md w-full max-w-md relative">
        <h2 className="text-xl font-bold mb-4">
          {initialData ? 'Edit Sweet' : 'Add New Sweet'}
        </h2>
        <form onSubmit={handleSubmit} className="space-y-4">
          <input
            name="name"
            placeholder="Name"
            className="w-full border p-2"
            value={formData.name}
            onChange={handleChange}
            required
          />
          <input
            name="category"
            placeholder="Category"
            className="w-full border p-2"
            value={formData.category}
            onChange={handleChange}
            required
          />
          <input
            name="price"
            type="number"
            placeholder="Price"
            className="w-full border p-2"
            value={formData.price}
            onChange={handleChange}
            required
          />
          <input
            name="quantity"
            type="number"
            placeholder="Quantity"
            className="w-full border p-2"
            value={formData.quantity}
            onChange={handleChange}
            required
          />
          <div className="flex justify-end gap-2">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 border border-gray-400 rounded"
            >
              Cancel
            </button>
            <button
              type="submit"
              className="px-4 py-2 bg-[#CFFFE2] text-black rounded hover:bg-[#A2D5C6]"
            >
              Save
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
