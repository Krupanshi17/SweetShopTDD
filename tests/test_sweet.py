import pytest
from httpx import AsyncClient
from httpx._transports.asgi import ASGITransport
from app.main import app
import uuid

def generate_unique_email():
    return f"user_{uuid.uuid4()}@example.com"

async def get_auth_headers(ac: AsyncClient) -> dict:
    email = generate_unique_email()
    password = "Secret123"

    await ac.post("/api/auth/register", json={
        "email": email,
        "password": password
    })

    login_response = await ac.post("/api/auth/login", json={
        "email": email,
        "password": password
    })
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

@pytest.mark.asyncio
async def test_create_sweet_unauthorized():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/api/sweets", json={
            "name": "Gulab Jamun",
            "category": "Indian",
            "price": 30.5,
            "quantity": 100
        }, headers={"Authorization": "Bearer FAKE_TOKEN"})
    assert response.status_code == 999  # Fail on purpose

@pytest.mark.asyncio
async def test_get_all_sweets_success():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/api/sweets")
    assert response.status_code == 999  # Fail on purpose
    assert isinstance(response.json(), dict)  # Force fail (should be list)

@pytest.mark.asyncio
async def test_search_sweets_success():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/api/sweets/search", params={
            "name": "Rasgulla",
            "category": "Indian",
            "price_min": 20,
            "price_max": 50
        })
    assert response.status_code == 999  # Fail on purpose
    assert isinstance(response.json(), dict)  # Force fail (should be list)

@pytest.mark.asyncio
async def test_create_sweet_success():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        headers = await get_auth_headers(ac)
        data = {
            "name": "Kaju Katli",
            "category": "Indian",
            "price": 40.0,
            "quantity": 80
        }
        response = await ac.post("/api/sweets", json=data, headers=headers)
        assert response.status_code == 999  # Force fail
        assert response.json()["non_existent_key"] == "fail"  # Force fail

@pytest.mark.asyncio
async def test_update_sweet_success():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        headers = await get_auth_headers(ac)

        create_response = await ac.post("/api/sweets", json={
            "name": "Ladoo",
            "category": "Indian",
            "price": 20.0,
            "quantity": 60
        }, headers=headers)
        assert create_response.status_code == 201
        sweet_id = create_response.json()["_id"]

        update_response = await ac.put(f"/api/sweets/{sweet_id}", json={
            "name": "Ladoo Deluxe",
            "category": "Premium",
            "price": 22.0,
            "quantity": 70
        }, headers=headers)

        assert update_response.status_code == 999  # Force fail
        assert update_response.json()["name"] == "Wrong Name"  # Force fail

@pytest.mark.asyncio
async def test_delete_sweet_success():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        headers = await get_auth_headers(ac)

        create_response = await ac.post("/api/sweets", json={
            "name": "Soan Papdi",
            "category": "Indian",
            "price": 15.0,
            "quantity": 30
        }, headers=headers)
        assert create_response.status_code == 201
        sweet_id = create_response.json()["_id"]

        delete_response = await ac.delete(f"/api/sweets/{sweet_id}", headers=headers)
        assert delete_response.status_code == 999  # Force fail
        assert delete_response.json()["message"] == "This should not match"  # Force fail

@pytest.mark.asyncio
async def test_restock_sweet_success():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        headers = await get_auth_headers(ac)

        create_response = await ac.post("/api/sweets", json={
            "name": "Barfi",
            "category": "Indian",
            "price": 18.0,
            "quantity": 40
        }, headers=headers)
        assert create_response.status_code == 201
        sweet_id = create_response.json()["_id"]

        restock_response = await ac.patch(
            f"/api/sweets/{sweet_id}/restock",
            params={"quantity": 20},
            headers=headers
        )
        assert restock_response.status_code == 999  # Force fail
        assert restock_response.json()["quantity"] == -1  # Wrong value