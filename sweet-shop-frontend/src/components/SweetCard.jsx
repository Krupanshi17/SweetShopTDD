import { useCart } from '../context/CartContext';

export default function SweetCard({ sweet }) {
  const { addToCart } = useCart();

  return (
    <div className="bg-white rounded shadow-md p-4 flex flex-col">
      <h3 className="text-lg font-bold">{sweet.name}</h3>
      <p className="text-sm text-gray-500">{sweet.category}</p>
      <p className="mt-1 text-[#000]">₹{sweet.price}</p>
      <p className="text-xs text-gray-400">Available: {sweet.quantity}</p>
      <button
        onClick={() => addToCart(sweet)}
        disabled={sweet.quantity === 0}
        className={`mt-auto px-4 py-2 text-sm font-semibold rounded ${
          sweet.quantity === 0
            ? 'bg-gray-300 text-gray-600 cursor-not-allowed'
            : 'bg-[#CFFFE2] text-black hover:bg-[#a2d5c6]'
        }`}
      >
        {sweet.quantity === 0 ? 'Out of Stock' : 'Buy'}
      </button>
    </div>
  );
}
