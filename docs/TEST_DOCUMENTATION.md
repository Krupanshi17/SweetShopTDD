# 🍬 Sweet Shop API - Test Documentation

## ✅ Test Overview

The test suite is designed to ensure both correctness and robustness of the Sweet Shop API. It includes:

* Happy path tests to verify correct functionality
* Negative tests to validate error handling, data validation, and access control

Tests are written using `pytest`, `pytest-asyncio`, and `httpx.AsyncClient` for FastAPI’s async endpoints.

---

## 🗂️ Test File Structure

```
tests/
├── conftest.py            # Shared fixtures and utilities
├── test_auth.py           # ❌ Failing authentication tests (negative tests)
├── correct_auth.py        # ✅ Passing authentication tests (happy paths)
├── test_sweets.py         # ❌ Failing sweet management tests
├── correct_sweets.py      # ✅ Passing sweet management tests
└── pytest.ini             # Pytest config
```

---

## 🧪 Test Execution

### 🔹 Run All Tests

```bash
pytest
```

### 🔹 Run by File Type

```bash
# Run all passing tests
pytest tests/correct_auth.py tests/correct_sweets.py

# Run all failing/negative tests
pytest tests/test_auth.py tests/test_sweets.py
```

### 🔹 Run Verbosely or with Coverage

```bash
pytest -v                          # Verbose output
pytest --cov=app                   # Coverage report
pytest --cov=app --cov-report=html  # HTML report
```

### 🔹 Run Specific Test

```bash
pytest tests/correct_auth.py::test_register_user_success
```

---

## 🧱 Test Philosophy: File Separation

| File                | Purpose                                | Expected Outcome |
| ------------------- | -------------------------------------- | ---------------- |
| `correct_auth.py`   | Valid auth flows                       | ✅ Should pass    |
| `test_auth.py`      | Invalid or edge-case auth scenarios    | ❌ Should fail    |
| `correct_sweets.py` | Valid sweet CRUD operations (admin)    | ✅ Should pass    |
| `test_sweets.py`    | Unauthorized, invalid sweet operations | ❌ Should fail    |

This separation helps isolate **production-ready behavior** from **validation/error handling logic**.

---

## 🔐 Authentication Tests

### ✅ `correct_auth.py` - Happy Path

* Register with valid email/password
* Login with correct credentials
* Prevent duplicate registration (handled error)
* Token returned on success

### ❌ `test_auth.py` - Fail Scenarios

* Missing email or password on registration
* Login with wrong credentials
* Empty request body
* Incorrect content-type
* Invalid role or secret for admin

#### Example: Passing Test

```python
@pytest.mark.asyncio
async def test_register_user_success():
    res = await client.post("/api/auth/register", json={
        "email": "user@example.com",
        "password": "Secret123"
    })
    assert res.status_code == 201
    assert "access_token" in res.json()
```

#### Example: Failing Test

```python
@pytest.mark.asyncio
async def test_register_missing_email():
    res = await client.post("/api/auth/register", json={
        "password": "Secret123"
    })
    assert res.status_code == 422
```

---

## 🍬 Sweet Management Tests

### ✅ `correct_sweets.py` - Happy Path (Admin only)

* Create, update, delete, and restock sweets
* Fetch all sweets (public)
* Search sweets (public)

### ❌ `test_sweets.py` - Error Paths

* Unauthorized sweet creation (no token)
* Create with missing fields or bad data
* Update with invalid ID
* Delete non-existent sweet
* Restock with negative value
* Access admin routes with user role

#### Example: Passing Sweet Creation

```python
@pytest.mark.asyncio
async def test_create_sweet_success(client):
    headers = await get_auth_headers(client, is_admin=True)
    res = await client.post("/api/sweets/", json={
        "name": "Kaju Katli",
        "category": "Dry",
        "price": 40.0,
        "quantity": 50
    }, headers=headers)
    assert res.status_code == 201
```

#### Example: Failing Unauthorized Access

```python
@pytest.mark.asyncio
async def test_create_sweet_unauthorized(client):
    res = await client.post("/api/sweets/", json={
        "name": "Jalebi", "category": "Fried", "price": 10, "quantity": 20
    })
    assert res.status_code == 401
```

---

## 🧪 Test Utilities

### Unique Email Generator

```python
import uuid

def generate_unique_email():
    return f"user_{uuid.uuid4()}@example.com"
```

### Auth Header Helper

```python
async def get_auth_headers(client: AsyncClient, is_admin: bool = True) -> dict:
    email = generate_unique_email()
    password = "Secret123"
    role = "admin" if is_admin else "user"
    admin_secret = "YourAdminSecretHere" if is_admin else None

    await client.post("/api/auth/register", json={
        "email": email, "password": password,
        "role": role, "admin_secret": admin_secret
    })

    res = await client.post("/api/auth/login", data={
        "username": email,
        "password": password
    }, headers={"Content-Type": "application/x-www-form-urlencoded"})

    token = res.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
```

---

## 🎯 Test Best Practices

* ✅ Use isolated test data (e.g. `generate_unique_email`)
* ✅ Independent, self-contained test functions
* ✅ Clear status code and response assertions
* ✅ Cover both successful and failure paths

---

## 📊 Coverage Goals

### ✅ Already Covered

* Authentication flows (register/login)
* Role-based access (admin vs user)
* Public and admin sweet endpoints
* Validation errors
* Auth header checks

### 🔄 Suggested Additions

* JWT expiration handling
* Invalid token formats
* Database connectivity issues
* Performance/load simulation
* Concurrency (race conditions on restock)

---

## 🐞 Debugging Tips

```bash
# Show print logs and verbose output
pytest -v -s

# Control traceback length
pytest --tb=short
pytest --tb=long

# Generate coverage report
pytest --cov=app --cov-report=html
# Then open: htmlcov/index.html
```

---

## ✅ Conclusion

This structured testing approach ensures:

* Clean separation of working features and validation checks
* Higher confidence during refactors
* Easy CI integration
* Realistic test scenarios using async & JWT

Stay consistent with this format to improve test reliability and maintainability across the Sweet Shop API backend.
