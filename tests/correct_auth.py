import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

@pytest.mark.asyncio
async def test_register_login_and_errors():
    """
    End-to-end test for user registration, login, and validation error scenarios.
    Covers:
    - Successful registration
    - Duplicate registration failure
    - Successful login
    - Missing fields validation
    - Empty body validation
    """
    transport = ASGITransport(app=app)

    # Create a single HTTP client for all requests
    async with AsyncClient(transport=transport, base_url="http://test") as ac:

        #  Test successful registration
        reg_response = await ac.post("/api/auth/register", json={
            "email": "test@example.com",
            "password": "Secret123"
        })
        assert reg_response.status_code == 201, f"Register failed: {reg_response.json()}"
        assert "access_token" in reg_response.json(), "Access token missing after registration"

        #  Test duplicate registration (should fail)
        duplicate_response = await ac.post("/api/auth/register", json={
            "email": "test@example.com",  # Same email as before
            "password": "AnotherPass"
        })
        assert duplicate_response.status_code == 400, "Expected 400 for duplicate registration"
        assert duplicate_response.json()["detail"] == "Email already registered"

        # Test successful login with correct credentials
        login_response = await ac.post("/api/auth/login", json={
            "email": "test@example.com",
            "password": "Secret123"
        })
        assert login_response.status_code == 200, "Expected 200 on successful login"
        assert "access_token" in login_response.json(), "Access token missing after login"

        # Test registration with missing password field
        missing_password_response = await ac.post("/api/auth/register", json={
            "email": "missingpass@example.com"
        })
        assert missing_password_response.status_code == 422, "Expected 422 for missing password"

        # Test registration with missing email field
        missing_email_response = await ac.post("/api/auth/register", json={
            "password": "SomePassword"
        })
        assert missing_email_response.status_code == 422, "Expected 422 for missing email"

        #  Test login with empty body
        empty_login = await ac.post("/api/auth/login", json={})
        assert empty_login.status_code == 422, "Expected 422 for empty login body"

        #  Test registration with empty body
        empty_register = await ac.post("/api/auth/register", json={})
        assert empty_register.status_code == 422, "Expected 422 for empty registration body"
