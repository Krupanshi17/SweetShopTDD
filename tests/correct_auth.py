import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

@pytest.mark.asyncio
async def test_register_login_and_errors():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # ✅ Register new user
        reg_response = await ac.post("/api/auth/register", json={
            "email": "test1@example.com",
            "password": "Secret123"
        })
        assert reg_response.status_code == 201, f"Register failed: {reg_response.json()}"
        assert "access_token" in reg_response.json()

        # ❌ Register same user again — should fail
        duplicate_response = await ac.post("/api/auth/register", json={
            "email": "test@example.com",  # same as above
            "password": "AnotherPass"
        })
        assert duplicate_response.status_code == 400
        assert duplicate_response.json()["detail"] == "Email already registered"

        # ✅ Correct login
        login_response = await ac.post("/api/auth/login", json={
            "email": "test@example.com",
            "password": "Secret123"
        })
        assert login_response.status_code == 200
        assert "access_token" in login_response.json()

        # ❌ Missing password field during registration
        missing_password_response = await ac.post("/api/auth/register", json={
            "email": "missingpass@example.com"
        })
        assert missing_password_response.status_code == 422  # Unprocessable Entity

        # ❌ Missing email field during registration
        missing_email_response = await ac.post("/api/auth/register", json={
            "password": "SomePassword"
        })
        assert missing_email_response.status_code == 422

        # ❌ Empty request body during login
        empty_login = await ac.post("/api/auth/login", json={})
        assert empty_login.status_code == 422

        # ❌ Empty request body during register
        empty_register = await ac.post("/api/auth/register", json={})
        assert empty_register.status_code == 422