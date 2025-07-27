# Sweet Shop API - Developer Guide (Detailed Edition)

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Technology Stack](#technology-stack)
3. [Core Components](#core-components)
4. [Authentication & Authorization](#authentication--authorization)
5. [Database Schemas](#database-schemas)
6. [Environment Setup](#environment-setup)
7. [Running the Application](#running-the-application)
8. [API Design Patterns](#api-design-patterns)
9. [Testing Strategy](#testing-strategy)
10. [Security Considerations](#security-considerations)
11. [Performance Considerations](#performance-considerations)
12. [Deployment Guide](#deployment-guide)
13. [Contributing Guidelines](#contributing-guidelines)

---

## Architecture Overview

The Sweet Shop API implements a clean, scalable, and modular layered architecture:

```
app/
├── main.py            # FastAPI initialization, routes mounting, middleware setup
├── config.py          # Pydantic-based settings from .env
├── database.py        # MongoDB connection using motor
├── constants/         # Centralized constants, enums, messages
├── models/            # MongoDB document models
├── schemas/           # Pydantic models for requests/responses
├── routes/            # FastAPI routers for each module (auth, sweet)
├── services/          # Business logic for user & sweet handling
├── utils/             # Token management, password hashing, guards
└── tests/             # Pytest-based test suite
```

---

## Technology Stack

* **Language**: Python 3.11+
* **Framework**: FastAPI
* **Database**: MongoDB (AsyncIOMotorClient)
* **Auth**: JWT-based authentication
* **Password Hashing**: bcrypt via `passlib`
* **Async HTTP Testing**: httpx + pytest-asyncio
* **Validation**: Pydantic with field constraints
* **Environment Config**: python-dotenv & pydantic

---

## Core Components

### 1. `database.py`

Handles the MongoDB client connection and exposes collections:

```python
client = AsyncIOMotorClient(settings.MONGODB_URL)
database = client[settings.DATABASE_NAME]
user_collection = database.get_collection("users")
sweet_collection = database.get_collection("sweets")
```

### 2. `config.py`

Loads environment variables into a `Settings` object:

```python
class Settings(BaseSettings):
    MONGODB_URL: str
    DATABASE_NAME: str
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ADMIN_SECRET: str
```

### 3. Models (`models/`)

Define MongoDB schemas (not enforced, for dev consistency):

* `user_model.py`
* `sweet_model.py`

### 4. Schemas (`schemas/`)

Pydantic models for request validation and response formatting:

* `UserCreate`, `UserLogin`, `TokenResponse`
* `SweetCreate`, `SweetUpdate`, `SweetResponse`

### 5. Services (`services/`)

Contain business logic:

* `auth_service.py`: Registration, login, admin check, seeding
* `sweet_service.py`: CRUD logic on sweet items

### 6. Routes (`routes/`)

Mounted on `/api/`:

* `/auth`: `/register`, `/login`
* `/sweets`: Public and admin sweet endpoints

### 7. Utils (`utils/`)

* `auth.py`: JWT encoding, decoding
* `hash.py`: Password hash/verify
* `auth_guard.py`: Dependency functions: `verify_token`, `verify_admin`

---

## Authentication & Authorization

### JWT Token Flow

* Encodes: `sub`, `exp`, `iat`
* Issued at login, passed as Bearer token
* Validated for all protected endpoints

### Admin Auth Flow

1. `Authorization: Bearer <token>`
2. JWT decoded, user ID extracted
3. DB fetch user by ID
4. Ensure `user.role == 'admin'`

### Access Control Table

| Route                     | Access Level |
| ------------------------- | ------------ |
| `GET /api/sweets/`        | Public       |
| `GET /api/sweets/search`  | Public       |
| `POST /api/sweets/`       | Admin Only   |
| `PUT /api/sweets/{id}`    | Admin Only   |
| `DELETE /api/sweets/{id}` | Admin Only   |

---

## Database Schemas

### Users Collection

```json
{
  "_id": ObjectId,
  "email": "user@example.com",
  "password": "$2b$12$hashed_pw",
  "role": "user" | "admin",
  "created_at": ISODate
}
```

### Sweets Collection

```json
{
  "_id": ObjectId,
  "name": "Gulab Jamun",
  "category": "Syrup",
  "price": 25.0,
  "quantity": 50,
  "created_at": ISODate,
  "updated_at": ISODate
}
```

---

## Environment Setup

### `.env` Example

```env
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=sweetshop
JWT_SECRET_KEY=YourJWTSecretKey
JWT_ALGORITHM=HS256
ADMIN_SECRET=SuperSecretAdminSeed
```

### Installing Dependencies

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

## Running the Application

### Start Development Server

```bash
uvicorn app.main:app --reload
```

### Run Tests

```bash
pytest
```

### With Coverage

```bash
pytest --cov=app
```

---

## API Design Patterns

### Error Handling

```python
raise HTTPException(status_code=404, detail="Sweet not found")
```

### Response Models

```python
@router.get("/", response_model=List[SweetResponse])
async def get_all_sweets():
    return await sweet_service.get_all_sweets()
```

### Dependency Injection

```python
@router.post("/", dependencies=[Depends(verify_admin)])
async def create_sweet(sweet: SweetCreate):
    return await sweet_service.create_sweet(sweet)
```

---

## Testing Strategy

### Structure

* `tests/conftest.py`: Shared fixtures (auth headers, db cleanup)
* `tests/test_auth.py`: Auth workflows
* `tests/test_sweets.py`: Sweet CRUD scenarios

### Example Test

```python
@pytest.mark.asyncio
async def test_get_sweets():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/api/sweets/")
        assert response.status_code == 200
```

### Auth Helpers

```python
async def get_auth_headers(client: AsyncClient, is_admin=False) -> dict:
    # Register, login, return headers
    return {"Authorization": f"Bearer {token}"}
```

---

## Security Considerations

### Password Security

* Hash: bcrypt (`passlib.hash.bcrypt`)
* Validate using `verify_password`

### JWT Security

* Signed using `JWT_SECRET_KEY`
* Include `exp`, `iat`
* Invalid or expired tokens rejected

### Input Validation

* Pydantic field constraints (e.g. `min_length`, `gt`, `email`)

### CORS Configuration

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## Performance Considerations

### MongoDB Indexing

```js
// Unique email index
user_collection.create_index({"email": 1}, {unique: true})

// Sweets search optimization
sweet_collection.create_index({"name": 1})
sweet_collection.create_index({"category": 1})
sweet_collection.create_index({"price": 1})
```

### Async Operations

* All DB and service calls are non-blocking using `await`

---

## Deployment Guide

### Configuration

* Use `.env` for secrets
* Set debug=False in production
* Configure production DB pool size

### Monitoring

* Add `/health` route for liveness check
* Integrate with logging/monitoring tools (e.g. Prometheus, Sentry)

### Scaling

* Run behind reverse proxy (e.g. Nginx)
* Use Gunicorn or Uvicorn workers
* Consider caching layer (e.g. Redis) for popular data

---

## Contributing Guidelines

### Code Standards

* Use [PEP8](https://peps.python.org/pep-0008/) & type hints
* Structure code into services, routes, schemas, etc.
* Write reusable utility functions

### Testing Requirements

* Use descriptive test names
* Test both success and failure cases
* Maintain 80%+ coverage

### Documentation

* Docstring all public methods
* Update this guide when architecture changes
* Keep `.env.example` in sync

---

## Appendix

* Admin user creation is auto-seeded if no admin exists
* Sweet item `quantity` must always be `>= 0`
* Price must be a positive float

For questions or suggestions, raise a GitHub issue or contact the maintainer.

---

**End of Document**
