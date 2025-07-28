# tests/test_sweets.py

import pytest
import pytest_asyncio
from httpx import AsyncClient
from httpx._transports.asgi import ASGITransport
from app.main import app
import uuid
import asyncio
import pytest

@pytest.fixture(scope="function")
def anyio_backend():
    return 'asyncio'

@pytest.fixture(scope="function")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()

def generate_unique_email():
    return f"user_{uuid.uuid4()}@example.com"

@pytest.fixture
async def client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac

async def get_auth_headers(ac: AsyncClient, is_admin: bool = True) -> dict:
    email = "test123@example.com"
    password = "Secret123"
    role = "user" if is_admin else "user"
    admin_secret = "superadmincode" if is_admin else None

    res = await ac.post("/api/auth/register", json={
        "email": email,
        "password": password,
        "role": role,
        "admin_secret": admin_secret
    })

    assert res.status_code in (200, 201), f"Register failed: {res.text}"

    token = res.json().get("access_token")
    print(f"Generated token: {token}")
    assert token, "No access_token in register response"
    assert token is not None, "No access_token in register response"

    return {"Authorization": f"Bearer {token}"}


@pytest.mark.asyncio
async def test_get_all_sweets_success(client):
    res = await client.get("/api/sweets/")
    assert res.status_code == 200


@pytest.mark.asyncio
async def test_search_sweets_success(client):
    res = await client.get("/api/sweets/search", params={"name": "Ladoo"})
    assert res.status_code == 200


@pytest.mark.asyncio
async def test_create_sweet_success(client):
    headers = await get_auth_headers(client)
    res = await client.post("/api/sweets/", json={
        "name": "Barfi", "category": "Milk", "price": 25.0, "quantity": 100
    }, headers=headers)
    assert res.status_code == 201
    assert res.json()["name"] == "Barfi"


@pytest.mark.asyncio
async def test_update_sweet_success(client):
    headers = await get_auth_headers(client)

    res = await client.post("/api/sweets/", json={
        "name": "Jalebi", "category": "Fried", "price": 20, "quantity": 50
    }, headers=headers)
    sweet_id = res.json()["_id"]

    update_res = await client.put(f"/api/sweets/{sweet_id}", json={
        "name": "Jalebi Updated", "price": 22
    }, headers=headers)
    assert update_res.status_code == 200
    assert update_res.json()["name"] == "Jalebi Updated"


@pytest.mark.asyncio
async def test_delete_sweet_success(client):
    headers = await get_auth_headers(client)

    res = await client.post("/api/sweets/", json={
        "name": "Rasgulla", "category": "Syrup", "price": 15, "quantity": 80
    }, headers=headers)
    sweet_id = res.json()["_id"]

    del_res = await client.delete(f"/api/sweets/{sweet_id}", headers=headers)
    assert del_res.status_code == 200  # instead of 204
    assert del_res.json() == {"message": "Sweet deleted"}

@pytest.mark.asyncio
async def test_restock_sweet_success(client):
    headers = await get_auth_headers(client)

    # Create a sweet first
    res = await client.post("/api/sweets/", json={
        "name": "Gulab Jamun", "category": "Syrup", "price": 30, "quantity": 10
    }, headers=headers)
    assert res.status_code == 201
    sweet_id = res.json()["_id"]

    # Restock the sweet
    restock_res = await client.patch(
        f"/api/sweets/{sweet_id}/restock", 
        params={"quantity": 20}, 
        headers=headers
    )
    assert restock_res.status_code == 200
    updated_sweet = restock_res.json()
    assert updated_sweet["quantity"] == 30
    assert updated_sweet["name"] == "Gulab Jamun"
