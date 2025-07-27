# Sweet Shop API Documentation

## Base URL
```
http://localhost:8000
```

## Authentication
The API uses JWT Bearer token authentication. Include the token in the Authorization header:
```
Authorization: Bearer <your_jwt_token>
```

## Default Admin Account
- **Email**: admin@sweetshop.com
- **Password**: AdminSecret123

---

## Authentication Endpoints

### Register User
**POST** `/api/auth/register`

Register a new user or admin account.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "password123",
  "role": "user",
  "admin_secret": "YourAdminSecretHere"  // Required only for admin role
}
```

**Response (201):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Error Responses:**
- `400`: Email already registered
- `422`: Validation error (missing fields, invalid email format)

---

### Login
**POST** `/api/auth/login`

Login with existing credentials.

**Request Body (Form Data):**
```
username: user@example.com
password: password123
```

**Response (200):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Error Responses:**
- `401`: Invalid credentials
- `422`: Missing username or password

---

## Sweet Management Endpoints

### Get All Sweets
**GET** `/api/sweets/`

Retrieve all sweets in the inventory. **Public endpoint** - no authentication required.

**Response (200):**
```json
[
  {
    "id": "507f1f77bcf86cd799439011",
    "name": "Gulab Jamun",
    "category": "Syrup",
    "price": 25.0,
    "quantity": 50
  },
  {
    "id": "507f1f77bcf86cd799439012",
    "name": "Barfi",
    "category": "Milk",
    "price": 30.0,
    "quantity": 25
  }
]
```

---

### Search Sweets
**GET** `/api/sweets/search`

Search and filter sweets by various criteria. **Public endpoint** - no authentication required.

**Query Parameters:**
- `name` (string, optional): Filter by sweet name
- `category` (string, optional): Filter by category
- `price_min` (float, optional, default: 0): Minimum price
- `price_max` (float, optional, default: 1000): Maximum price

**Example Request:**
```
GET /api/sweets/search?name=Ladoo&category=Fried&price_min=10&price_max=50
```

**Response (200):**
```json
[
  {
    "id": "507f1f77bcf86cd799439013",
    "name": "Boondi Ladoo",
    "category": "Fried",
    "price": 20.0,
    "quantity": 30
  }
]
```

---

### Create Sweet
**POST** `/api/sweets/`

Create a new sweet item. **Admin only** - requires admin authentication.

**Headers:**
```
Authorization: Bearer <admin_jwt_token>
```

**Request Body:**
```json
{
  "name": "Rasgulla",
  "category": "Syrup",
  "price": 15.0,
  "quantity": 100
}
```

**Response (201):**
```json
{
  "id": "507f1f77bcf86cd799439014",
  "name": "Rasgulla",
  "category": "Syrup",
  "price": 15.0,
  "quantity": 100
}
```

**Error Responses:**
- `401`: Invalid or missing token
- `403`: User is not admin
- `422`: Validation error (invalid price, negative quantity, etc.)

---

### Update Sweet
**PUT** `/api/sweets/{sweet_id}`

Update an existing sweet item. **Admin only** - requires admin authentication.

**Headers:**
```
Authorization: Bearer <admin_jwt_token>
```

**Request Body:**
```json
{
  "name": "Updated Rasgulla",
  "price": 18.0,
  "quantity": 80
}
```

**Response (200):**
```json
{
  "id": "507f1f77bcf86cd799439014",
  "name": "Updated Rasgulla",
  "category": "Syrup",
  "price": 18.0,
  "quantity": 80
}
```

**Error Responses:**
- `401`: Invalid or missing token
- `403`: User is not admin
- `404`: Sweet not found

---

### Delete Sweet
**DELETE** `/api/sweets/{sweet_id}`

Delete a sweet item from inventory. **Admin only** - requires admin authentication.

**Headers:**
```
Authorization: Bearer <admin_jwt_token>
```

**Response (200):**
```json
{
  "message": "Sweet deleted"
}
```

**Error Responses:**
- `401`: Invalid or missing token
- `403`: User is not admin
- `404`: Sweet not found

---

### Restock Sweet
**PATCH** `/api/sweets/{sweet_id}/restock`

Add quantity to existing sweet inventory. **Admin only** - requires admin authentication.

**Headers:**
```
Authorization: Bearer <admin_jwt_token>
```

**Query Parameters:**
- `quantity` (int, required): Amount to add to current stock

**Example Request:**
```
PATCH /api/sweets/507f1f77bcf86cd799439014/restock?quantity=50
```

**Response (200):**
```json
{
  "id": "507f1f77bcf86cd799439014",
  "name": "Rasgulla",
  "category": "Syrup",
  "price": 15.0,
  "quantity": 150
}
```

**Error Responses:**
- `401`: Invalid or missing token
- `403`: User is not admin
- `404`: Sweet not found

---

## Error Response Format

All error responses follow this format:
```json
{
  "detail": "Error message description"
}
```

## Status Codes Summary

- `200`: Success
- `201`: Created successfully
- `400`: Bad request (duplicate email, etc.)
- `401`: Unauthorized (invalid/missing token)
- `403`: Forbidden (insufficient permissions)
- `404`: Resource not found
- `422`: Validation error (invalid input data)

## Interactive Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc