#  Sweet Shop Frontend

The Sweet Shop Frontend is a modern and responsive React + TailwindCSS application that connects to a FastAPI backend to provide a full-featured e-commerce-like experience. It supports user authentication, role-based access control, cart functionality, and sweet inventory management with an intuitive UI tailored for both users and administrators.

##  Features

###  User Management
- Secure JWT-based authentication
- Registration and Login flows with form validation
- Role-based access control:
  - Users can browse sweets and manage their cart
  - Admins can manage sweets (add, update, delete, restock)

###  Sweet Inventory
- Fetch all sweets with pagination (optional)
- Search and filter sweets by name or category
- View sweet details with quantity and price
- Admins can perform:
  - Create new sweets
  - Edit existing sweets
  - Delete sweets
  - Restock inventory

###  Cart System
- Add sweets to cart (with quantity control)
- Modify quantity or remove items
- Persistent cart using local storage

###  Responsive UI
- Mobile-first layout using TailwindCSS
- Adaptive design for tablets and desktops
- Clean e-commerce inspired UI

###  Real-Time Feedback
- Toast notifications powered by React Toastify
- Feedback for login, logout, cart actions, CRUD ops, etc.

##  Quick Start

###  Prerequisites
- Node.js v18+
- npm or yarn
- A running Sweet Shop Backend API

###  Setup

1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-username/sweet-shop-frontend.git
   cd sweet-shop-frontend
   ```

2. **Install Dependencies**
   ```bash
   npm install
   # or
   yarn
   ```

3. **Environment Configuration**
   Create a `.env` file in the project root:
   ```env
   VITE_API_BASE_URL=http://localhost:8000/api
   ```

4. **Run the Development Server**
   ```bash
   npm run dev
   ```

5. **Access the App**
   Open http://localhost:5173 in your browser.

##  API Integration

All requests are made through a centralized Axios instance configured to automatically attach the JWT token for authenticated endpoints.

```js
// src/services/axiosInstance.js
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

##  API Endpoints Used

###  Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/register` | Register a new user |
| POST | `/auth/login` | Login with credentials |

###  Sweets
| Method | Endpoint | Role | Description |
|--------|----------|------|-------------|
| GET | `/sweets/` | Public | Fetch all sweets |
| GET | `/sweets/search?name=&category=` | Public | Search/filter sweets |
| POST | `/sweets/` | Admin only | Add a new sweet |
| PUT | `/sweets/{id}` | Admin only | Update sweet details |
| DELETE | `/sweets/{id}` | Admin only | Delete a sweet |
| PATCH | `/sweets/{id}/restock` | Admin only | Restock quantity |

## Project Structure

```
sweet-shop-frontend/
├── public/                      # Static assets
├── src/
│   ├── assets/                  # Images, icons, etc.
│   ├── components/              # Reusable UI components (Navbar, SweetCard, etc.)
│   ├── context/                 # React contexts (AuthContext, CartContext)
│   ├── pages/                   # Application pages (Login, Register, Cart, AdminPanel, etc.)
│   ├── routes/                  # Route setup and ProtectedRoute logic
│   ├── services/                # API logic and Axios configuration
│   ├── App.jsx                  # Main app component with layout
│   ├── main.jsx                 # React entry point
│   └── index.css                # Tailwind and global styles
├── .env                         # Environment config
├── tailwind.config.js           # TailwindCSS configuration
├── postcss.config.cjs           # PostCSS setup
├── package.json                 # Scripts and dependencies
└── README.md                    # Project documentation
```

##  Scripts

| Command | Description |
|---------|-------------|
| `npm run dev` | Start development server |
| `npm run build` | Build the app for production |
| `npm run preview` | Preview the production build |
| `npm run lint` | Run linter to check for issues |

##  Default Admin Credentials

Use the following credentials to log in as an admin:

```
Email:    admin@sweetshop.com  
Password: AdminSecret123
```

*These must match the credentials registered in the backend.*

##  Future Improvements

- Add pagination to sweet listing
- Order history and user profile page
- Payment integration (Stripe or Razorpay)
- Theme switcher (light/dark mode)
- Admin analytics dashboard