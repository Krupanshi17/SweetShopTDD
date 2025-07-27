# Sweet Shop

A full-stack Sweet Shop Management System with a FastAPI backend and a React frontend. This project features user authentication, role-based access control, sweet inventory management, cart functionality, and a responsive, modern UI.

---

## Table of Contents

- [Features](#features)  
- [Technologies](#technologies)  
- [Quick Start](#quick-start)  
- [Backend](#backend)  
- [Frontend](#frontend)  
- [Project Structure](#project-structure)  
- [Default Admin Account](#default-admin-account)  
- [License](#license)  

---

## Features

- JWT-based user authentication with role-based access (User/Admin)  
- Admin CRUD operations for sweets (add, update, delete, restock)  
- Users can browse sweets, search by name/category, and manage a cart  
- Responsive UI with TailwindCSS and toast notifications  
- Secure API calls with Axios and JWT token interception  
- Protected routes on frontend to restrict access based on login and role  

---

## Technologies

- **Backend:** Python, FastAPI, MongoDB, Pydantic, JWT  
- **Frontend:** React, React Router v6, Axios, TailwindCSS, React Toastify  
- **Tools:** Vite, PostCSS, ESLint  

---

## Quick Start

### Prerequisites

- Python 3.8+  
- Node.js 18+  
- MongoDB (local or cloud)  

---

## Backend

### Setup & Run

1. Clone the repository and navigate to the backend folder:
   ```bash
   git clone <repository-url>
   cd sweetshop/backend
   
2. Create and activate a virtual environment:
   python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

3. Install dependencies:
   pip install -r requirements.txt
4. Create a .env file with environment variables:

   MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=sweetshop
JWT_SECRET_KEY=your-secret-key
JWT_ALGORITHM=HS256
ADMIN_SECRET=YourAdminSecretHere

5. Run the backend server:
   uvicorn app.main:app --reload
   API will be available at: http://localhost:8000

Interactive API docs:

Swagger UI: http://localhost:8000/docs

ReDoc: http://localhost:8000/redoc

**Frontend**

**Setup & Run**

1.Navigate to the frontend folder:

   cd sweetshop/frontend
   
2.Install dependencies:
   npm install
   
3. Create a .env file in the frontend root with:
   VITE_API_BASE_URL=http://localhost:8000/api
4. Start the frontend development server:
    npm run dev
    Frontend will be available at: http://localhost:5173

**Project Structure**

sweetshop/
├── backend/
│   ├── app/
│   ├── tests/
│   ├── requirements.txt
│   ├── .env
│   └── README_BACKEND.md
├── frontend/
│   ├── src/
│   ├── public/
│   ├── package.json
│   ├── postcss.config.cjs
│   ├── tailwind.config.js
│   ├── .env
│   └── README_FRONTEND.md
└── README.md

**Default Admin Account**
On backend startup, a default admin user is created:

Email: admin@sweetshop.com

Password: AdminSecret123

License
This project is licensed under the MIT License.


