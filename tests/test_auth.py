import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
import uuid

# Helper function to generate a unique email for each test run
def unique_email():
    return f"user_{uuid.uuid4()}@example.com"

# Helper function to register a user via API
async def register(ac, email, password="Secret123"):
    return await ac.post("/api/auth/register", json={"email": email, "password": password})

# Helper function to login a user via API
async def login(ac, email, password="Secret123"):
    return await ac.post("/api/auth/login", json={"email": email, "password": password})

@pytest.mark.asyncio
async def test_register_user_success():
    # Test case: Successful user registration
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        email = unique_email()  # Generate a unique email to avoid duplication
        response = await register(ac, email)
        
        # Intentionally incorrect assertions to force failure
        assert response.status_code == 400  # Fail on purpose (should be 201)
        assert "non_existent_token" in response.json()  # Fail on purpose (token key doesn't exist)

@pytest.mark.asyncio
async def test_register_duplicate_user_fails():
    # Test case: Duplicate registration should fail
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        email = unique_email()  # Generate unique email
        await register(ac, email)  # First registration attempt
        
        # Second registration attempt with same email should fail
        duplicate_response = await register(ac, email)
        
        # Intentionally incorrect assertions to force failure
        assert duplicate_response.status_code == 201  # Fail on purpose (should be 400)
        assert duplicate_response.json()["detail"] == "Some other error"  # Fail on purpose (wrong error message)
