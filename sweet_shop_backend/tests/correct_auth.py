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

        # First user registration
        email1 = "user1@example.com"
        reg_response1 = await ac.post("/api/auth/register", json={
            "email": email1,
            "password": "Secret123"
        })
        assert reg_response1.status_code == 201, f"Register failed: {reg_response1.json()}"
        assert "access_token" in reg_response1.json(), "Access token missing after registration"

        # Duplicate registration with same email (should fail)
        duplicate_response = await ac.post("/api/auth/register", json={
            "email": email1,  
            "password": "AnotherPass"
        })
        assert duplicate_response.status_code == 400, "Expected 400 for duplicate registration"
        assert duplicate_response.json()["detail"] == "Email already registered"

        # Second user registration for login test
        email2 = "user2@example.com"
        reg_response2 = await ac.post("/api/auth/register", json={
            "email": email2,
            "password": "Secret123"
        })
        assert reg_response2.status_code == 201, f"Register failed: {reg_response2.json()}"

        # Test successful login with second user using form data
        login_response = await ac.post(
            "/api/auth/login",
            data={
                "username": email2,  # OAuth2 expects 'username'
                "password": "Secret123"
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
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

        # Test login with empty body
        empty_login = await ac.post("/api/auth/login", json={})
        assert empty_login.status_code == 422, "Expected 422 for empty login body"

        # Test registration with empty body
        empty_register = await ac.post("/api/auth/register", json={})
        assert empty_register.status_code == 422, "Expected 422 for empty registration body"
