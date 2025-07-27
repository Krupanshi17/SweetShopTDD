
# Sweet Shop Frontend

A React-based modern frontend for managing a Sweet Shop with user authentication, role-based access, cart management, and responsive UI built with TailwindCSS.

## Features

- **User Authentication**: JWT-based login/registration system
- **Role-based Access**: Admin and user roles with protected routes
- **Sweet Management**: Browse sweets for users; CRUD operations for Admin
- **Cart Functionality**: Add, update, and remove sweets from cart
- **Search & Filter**: Search sweets by name or category
- **Responsive Design**: Mobile-friendly layout using TailwindCSS
- **Toast Notifications**: Real-time feedback for actions (React Toastify)

---

## Quick Start

### Prerequisites

- Node.js 18+
- npm or yarn
- Sweet Shop API backend running (see backend README)

---

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd sweet-shop-frontend
```

2. Install dependencies:
```bash
npm install
```

3. Configure environment variables:
Create a `.env` file in the root directory and add:
```
VITE_API_BASE_URL=http://localhost:8000/api
```

4. Run the application:
```bash
npm run dev
```

The frontend will be available at `http://localhost:5173`

---

## API Integration Details

The application uses **Axios** for all API calls with JWT authentication. Axios instance is configured in `src/services/axiosInstance.js`:

```javascript
import axios from "axios";

const API = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
});

API.interceptors.request.use((req) => {
  const token = localStorage.getItem("token");
  if (token) {
    req.headers.Authorization = `Bearer ${token}`;
  }
  return req;
});

export default API;
```

### Endpoints Used:

- **Auth**
  - POST `/auth/login` – User login
  - POST `/auth/register` – User registration
- **Sweets**
  - GET `/sweets/` – Fetch all sweets
  - GET `/sweets/search?name=&category=` – Search sweets
  - POST `/sweets/` – Add sweet (Admin only)
  - PUT `/sweets/{id}` – Update sweet (Admin only)
  - DELETE `/sweets/{id}` – Delete sweet (Admin only)
  - PATCH `/sweets/{id}/restock` – Restock sweet (Admin only)

---

## Project Structure

```
sweet-shop-frontend/
├── src/
│   ├── assets/            # Images & icons
│   ├── components/        # Navbar, SweetCard, Modal
│   ├── context/           # AuthContext, CartContext
│   ├── pages/             # Login, Register, Dashboard, Cart, Admin
│   ├── routes/            # AppRoutes and ProtectedRoute
│   ├── services/          # Axios instance & API helpers
│   ├── App.jsx            # Main App component
│   ├── main.jsx           # Entry point
│   └── index.css          # TailwindCSS imports
├── public/                # Static files
├── postcss.config.cjs     # PostCSS configuration
├── tailwind.config.js     # TailwindCSS configuration
├── package.json           # Dependencies and scripts
└── README.md              # This file
```

---

## Scripts

```bash
npm run dev       # Start development server
npm run build     # Build for production
npm run preview   # Preview production build
npm run lint      # Lint project files
```

---

## Default Admin Account

Use the same admin credentials as the backend:
- **Email**: admin@sweetshop.com
- **Password**: AdminSecret123

---

## License

This project is licensed under the MIT License.
