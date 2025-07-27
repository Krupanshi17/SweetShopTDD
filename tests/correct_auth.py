import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
import uuid

def unique_email():
    return f"user_{uuid.uuid4()}@example.com"

async def register_user(ac, email, password="Secret123"):
    """Helper function to register a user."""
    return await ac.post("/api/auth/register", json={"email": email, "password": password})

async def login_user(ac, email, password="Secret123"):
    """Helper function to login a user."""
    return await ac.post("/api/auth/login", json={"email": email, "password": password})

@pytest.mark.asyncio
async def test_register_user_success():
    """Test successful user registration returns 201 and access token."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        email = unique_email()
        response = await register_user(ac, email)
        assert response.status_code == 201, f"Registration failed: {response.json()}"
        assert "access_token" in response.json()

@pytest.mark.asyncio
async def test_register_duplicate_user_fails():
    """Test registering with an already registered email returns 400."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        email = unique_email()
        await register_user(ac, email)
        duplicate_response = await register_user(ac, email)
        assert duplicate_response.status_code == 400
        assert duplicate_response.json()["detail"] == "Email already registered"

@pytest.mark.asyncio
async def test_login_success():
    """Test login with correct credentials returns 200 and access token."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        email = unique_email()
        password = "Secret123"
        await register_user(ac, email, password)
        response = await login_user(ac, email, password)
        assert response.status_code == 200
        assert "access_token" in response.json()

@pytest.mark.asyncio
async def test_login_wrong_password_fails():
    """Test login with wrong password returns 401."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        email = unique_email()
        password = "Secret123"
        await register_user(ac, email, password)
        response = await login_user(ac, email, "WrongPass123")
        assert response.status_code == 401
        assert response.json()["detail"] == "Invalid credentials"

@pytest.mark.asyncio
async def test_login_unregistered_email_fails():
    """Test login with unregistered email returns 401."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await login_user(ac, "notregistered@example.com", "Secret123")
        assert response.status_code == 401
        assert response.json()["detail"] == "Invalid credentials"

@pytest.mark.asyncio
async def test_register_missing_password_fails():
    """Test registration fails with missing password field."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/api/auth/register", json={"email": unique_email()})
        assert response.status_code == 422  # Unprocessable Entity

@pytest.mark.asyncio
async def test_register_missing_email_fails():
    """Test registration fails with missing email field."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/api/auth/register", json={"password": "SomePassword"})
        assert response.status_code == 422

@pytest.mark.asyncio
async def test_login_empty_body_fails():
    """Test login fails with empty request body."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/api/auth/login", json={})
        assert response.status_code == 422

@pytest.mark.asyncio
async def test_register_empty_body_fails():
    """Test registration fails with empty request body."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/api/auth/register", json={})
        assert response.status_code == 422
