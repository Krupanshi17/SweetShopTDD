import React, { useContext } from "react";
import { CartContext } from "../context/CartContext";

export default function Cart() {
  const {
    cartItems,
    removeFromCart,
    updateQuantity,
    totalPrice,
    clearCart,
  } = useContext(CartContext);

  return (
    <div className="p-6 bg-background min-h-screen max-w-4xl mx-auto">
      <h1 className="text-3xl font-bold mb-6">Your Cart</h1>

      {cartItems.length === 0 ? (
        <p>Your cart is empty.</p>
      ) : (
        <>
          <table className="w-full border-collapse mb-6">
            <thead>
              <tr className="bg-primaryDark text-accentCTA">
                <th className="p-2 text-left">Sweet</th>
                <th className="p-2 text-left">Price</th>
                <th className="p-2 text-left">Quantity</th>
                <th className="p-2 text-left">Total</th>
                <th className="p-2 text-left">Actions</th>
              </tr>
            </thead>
            <tbody>
              {cartItems.map((item) => (
                <tr key={item.id} className="border-b">
                  <td className="p-2">{item.name}</td>
                  <td className="p-2">₹{item.price}</td>
                  <td className="p-2">
                    <input
                      type="number"
                      min="1"
                      value={item.quantity}
                      onChange={(e) =>
                        updateQuantity(item.id, parseInt(e.target.value))
                      }
                      className="w-16 border rounded px-1"
                    />
                  </td>
                  <td className="p-2">₹{item.price * item.quantity}</td>
                  <td className="p-2">
                    <button
                      onClick={() => removeFromCart(item.id)}
                      className="text-red-600 hover:underline"
                    >
                      Remove
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>

          <div className="flex justify-between items-center font-bold text-lg">
            <span>Total Price: ₹{totalPrice}</span>
            <button
              onClick={clearCart}
              className="bg-primaryDark text-accentCTA px-4 py-2 rounded hover:bg-secondary"
            >
              Clear Cart
            </button>
          </div>
        </>
      )}
    </div>
  );
}
