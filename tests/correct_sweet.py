# tests/test_sweets.py

import pytest
import pytest_asyncio
from httpx import AsyncClient
from httpx._transports.asgi import ASGITransport
from app.main import app
import uuid

# Helper to generate unique email for testing
def generate_unique_email():
    return f"user_{uuid.uuid4()}@example.com"

# Fixture to create an AsyncClient instance for tests
@pytest_asyncio.fixture(scope="function")
async def client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac

# Helper function to get authorization headers (admin or user)
async def get_auth_headers(ac: AsyncClient, is_admin: bool = True) -> dict:
    email = "admin@example.com"
    password = "AdminSecret123"
    role = "admin" if is_admin else "user"
    admin_secret = "YourAdminSecretHere" if is_admin else None

    # Register user (admin if is_admin=True)
    await ac.post("/api/auth/register", json={
        "email": email,
        "password": password,
        "role": role,
        "admin_secret": admin_secret
    })

    # Login using form data for token retrieval
    res = await ac.post("/api/auth/login", data={
        "username": email,
        "password": password
    }, headers={"Content-Type": "application/x-www-form-urlencoded"})

    # Ensure login succeeded
    assert res.status_code == 200, f"Login failed: {res.text}"
    token = res.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

# Test fetching all sweets successfully
@pytest.mark.asyncio
async def test_get_all_sweets_success(client):
    res = await client.get("/api/sweets/")
    assert res.status_code == 200

# Test searching sweets by name
@pytest.mark.asyncio
async def test_search_sweets_success(client):
    res = await client.get("/api/sweets/search", params={"name": "Ladoo"})
    assert res.status_code == 200

# Test creating a new sweet successfully
@pytest.mark.asyncio
async def test_create_sweet_success(client):
    headers = await get_auth_headers(client)
    res = await client.post("/api/sweets/", json={
        "name": "Barfi", "category": "Milk", "price": 25.0, "quantity": 100
    }, headers=headers)
    assert res.status_code == 201
    assert res.json()["name"] == "Barfi"

# Test updating an existing sweet
@pytest.mark.asyncio
async def test_update_sweet_success(client):
    headers = await get_auth_headers(client)

    # Create sweet first
    res = await client.post("/api/sweets/", json={
        "name": "Jalebi", "category": "Fried", "price": 20, "quantity": 50
    }, headers=headers)
    sweet_id = res.json()["_id"]

    # Update sweet details
    update_res = await client.put(f"/api/sweets/{sweet_id}", json={
        "name": "Jalebi Updated", "price": 22
    }, headers=headers)
    assert update_res.status_code == 200
    assert update_res.json()["name"] == "Jalebi Updated"

# Test deleting a sweet
@pytest.mark.asyncio
async def test_delete_sweet_success(client):
    headers = await get_auth_headers(client)

    # Create sweet first
    res = await client.post("/api/sweets/", json={
        "name": "Rasgulla", "category": "Syrup", "price": 15, "quantity": 80
    }, headers=headers)
    sweet_id = res.json()["_id"]

    # Delete the sweet
    del_res = await client.delete(f"/api/sweets/{sweet_id}", headers=headers)
    assert del_res.status_code == 200  # Expecting success response
    assert del_res.json() == {"message": "Sweet deleted"}

# Test restocking a sweet
@pytest.mark.asyncio
async def test_restock_sweet_success(client):
    headers = await get_auth_headers(client)

    # Create sweet first
    res = await client.post("/api/sweets/", json={
        "name": "Gulab Jamun", "category": "Syrup", "price": 30, "quantity": 10
    }, headers=headers)
    sweet_id = res.json()["_id"]

    # Restock sweet quantity
    restock_res = await client.patch(f"/api/sweets/{sweet_id}/restock", params={"quantity": 20}, headers=headers)
    assert restock_res.status_code == 200
    assert restock_res.json()["quantity"] == 30
