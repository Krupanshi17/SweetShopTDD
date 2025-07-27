import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
import uuid

def generate_unique_email():
    """Generate a unique email address for testing to avoid conflicts."""
    return f"user_{uuid.uuid4()}@example.com"

@pytest.fixture(scope="function")
async def client():
    """Create an AsyncClient with ASGI transport for the app."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

async def get_auth_headers(ac: AsyncClient) -> dict:
    """
    Register a new user and login to get auth headers with JWT token.
    """
    email = generate_unique_email()
    password = "Secret123"

    await ac.post("/api/auth/register", json={"email": email, "password": password})
    login_response = await ac.post("/api/auth/login", json={"email": email, "password": password})
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

@pytest.mark.asyncio
async def test_create_sweet_unauthorized(client):
    """
    Test creating a sweet with an invalid token returns 401 Unauthorized.
    """
    response = await client.post("/api/sweets", json={
        "name": "Gulab Jamun",
        "category": "Indian",
        "price": 30.5,
        "quantity": 100
    }, headers={"Authorization": "Bearer FAKE_TOKEN"})

    assert response.status_code == 401  # Unauthorized due to invalid token

@pytest.mark.asyncio
async def test_get_all_sweets_success(client):
    """
    Test fetching all sweets returns 200 OK and a list of sweets.
    """
    response = await client.get("/api/sweets")
    assert response.status_code == 200
    assert isinstance(response.json(), list)  # Response should be a list of sweets

@pytest.mark.asyncio
async def test_search_sweets_success(client):
    """
    Test searching sweets with filters returns 200 OK and a list.
    """
    response = await client.get("/api/sweets/search", params={
        "name": "Rasgulla",
        "category": "Indian",
        "price_min": 20,
        "price_max": 50
    })
    assert response.status_code == 200
    assert isinstance(response.json(), list)

@pytest.mark.asyncio
async def test_create_sweet_success(client):
    """
    Test successful sweet creation with valid auth returns 201 Created.
    """
    headers = await get_auth_headers(client)
    data = {
        "name": "Kaju Katli",
        "category": "Indian",
        "price": 40.0,
        "quantity": 80
    }
    response = await client.post("/api/sweets", json=data, headers=headers)
    assert response.status_code == 201
    json_resp = response.json()
    assert json_resp["name"] == data["name"]
    assert json_resp["category"] == data["category"]

@pytest.mark.asyncio
async def test_update_sweet_success(client):
    """
    Test updating an existing sweet returns 200 OK and updated data.
    """
    headers = await get_auth_headers(client)
    create_resp = await client.post("/api/sweets", json={
        "name": "Ladoo",
        "category": "Indian",
        "price": 20.0,
        "quantity": 60
    }, headers=headers)
    assert create_resp.status_code == 201
    sweet_id = create_resp.json()["_id"]

    update_resp = await client.put(f"/api/sweets/{sweet_id}", json={
        "name": "Ladoo Deluxe",
        "category": "Premium",
        "price": 22.0,
        "quantity": 70
    }, headers=headers)
    assert update_resp.status_code == 200
    assert update_resp.json()["name"] == "Ladoo Deluxe"

@pytest.mark.asyncio
async def test_delete_sweet_success(client):
    """
    Test deleting an existing sweet returns 204 No Content.
    """
    headers = await get_auth_headers(client)
    create_resp = await client.post("/api/sweets", json={
        "name": "Soan Papdi",
        "category": "Indian",
        "price": 15.0,
        "quantity": 30
    }, headers=headers)
    assert create_resp.status_code == 201
    sweet_id = create_resp.json()["_id"]

    delete_resp = await client.delete(f"/api/sweets/{sweet_id}", headers=headers)
    assert delete_resp.status_code == 204  # No content on successful delete

@pytest.mark.asyncio
async def test_restock_sweet_success(client):
    """
    Test restocking a sweet increases quantity and returns updated sweet.
    """
    headers = await get_auth_headers(client)
    create_resp = await client.post("/api/sweets", json={
        "name": "Barfi",
        "category": "Indian",
        "price": 18.0,
        "quantity": 40
    }, headers=headers)
    assert create_resp.status_code == 201
    sweet_id = create_resp.json()["_id"]

    restock_resp = await client.patch(
        f"/api/sweets/{sweet_id}/restock",
        params={"quantity": 20},
        headers=headers
    )
    assert restock_resp.status_code == 200
    assert restock_resp.json()["quantity"] == 60  # 40 + 20
