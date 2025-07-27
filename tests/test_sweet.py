import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
import uuid

def generate_unique_email() -> str:
    """
    Generate a unique email address for testing to avoid conflicts.
    This helps isolate tests by ensuring unique user registration.
    """
    return f"user_{uuid.uuid4()}@example.com"

@pytest.fixture(scope="function")
async def client():
    """
    Async HTTP client fixture using ASGI transport.
    Provides a test client bound to the FastAPI app for each test function.
    """
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

async def get_auth_headers(ac: AsyncClient) -> dict:
    """
    Helper function to register a new user and obtain JWT authorization headers.
    
    :param ac: AsyncClient instance for making requests.
    :return: Dict with 'Authorization' header containing Bearer token.
    """
    email = generate_unique_email()
    password = "Secret123"

    # Register user
    await ac.post("/api/auth/register", json={"email": email, "password": password})
    
    # Login to get access token
    login_response = await ac.post("/api/auth/login", json={"email": email, "password": password})
    assert login_response.status_code == 200, "Login failed during auth header generation"
    token = login_response.json()["access_token"]
    
    return {"Authorization": f"Bearer {token}"}

@pytest.mark.asyncio
async def test_create_sweet_unauthorized(client: AsyncClient):
    """
    Verify that creating a sweet with an invalid token returns 401 Unauthorized.
    """
    response = await client.post(
        "/api/sweets",
        json={"name": "Gulab Jamun", "category": "Indian", "price": 30.5, "quantity": 100},
        headers={"Authorization": "Bearer FAKE_TOKEN"}
    )
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_get_all_sweets_success(client: AsyncClient):
    """
    Verify that fetching all sweets returns 200 OK and the response is a list.
    """
    response = await client.get("/api/sweets")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

@pytest.mark.asyncio
async def test_search_sweets_success(client: AsyncClient):
    """
    Verify searching sweets with filters returns 200 OK and a list of results.
    """
    params = {"name": "Rasgulla", "category": "Indian", "price_min": 20, "price_max": 50}
    response = await client.get("/api/sweets/search", params=params)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

@pytest.mark.asyncio
async def test_create_sweet_success(client: AsyncClient):
    """
    Verify successful sweet creation with valid authorization returns 201 Created.
    """
    headers = await get_auth_headers(client)
    data = {"name": "Kaju Katli", "category": "Indian", "price": 40.0, "quantity": 80}
    response = await client.post("/api/sweets", json=data, headers=headers)
    assert response.status_code == 201
    json_resp = response.json()
    assert json_resp["name"] == data["name"]
    assert json_resp["category"] == data["category"]

@pytest.mark.asyncio
async def test_update_sweet_success(client: AsyncClient):
    """
    Verify updating an existing sweet updates and returns the new data.
    """
    headers = await get_auth_headers(client)
    # Create sweet first
    create_resp = await client.post("/api/sweets", json={
        "name": "Ladoo", "category": "Indian", "price": 20.0, "quantity": 60
    }, headers=headers)
    assert create_resp.status_code == 201
    sweet_id = create_resp.json()["_id"]

    # Update sweet
    update_data = {"name": "Ladoo Deluxe", "category": "Premium", "price": 22.0, "quantity": 70}
    update_resp = await client.put(f"/api/sweets/{sweet_id}", json=update_data, headers=headers)
    assert update_resp.status_code == 200
    assert update_resp.json()["name"] == update_data["name"]

@pytest.mark.asyncio
async def test_delete_sweet_success(client: AsyncClient):
    """
    Verify deleting an existing sweet returns 204 No Content.
    """
    headers = await get_auth_headers(client)
    # Create sweet
    create_resp = await client.post("/api/sweets", json={
        "name": "Soan Papdi", "category": "Indian", "price": 15.0, "quantity": 30
    }, headers=headers)
    assert create_resp.status_code == 201
    sweet_id = create_resp.json()["_id"]

    # Delete sweet
    delete_resp = await client.delete(f"/api/sweets/{sweet_id}", headers=headers)
    assert delete_resp.status_code == 204

@pytest.mark.asyncio
async def test_restock_sweet_success(client: AsyncClient):
    """
    Verify restocking a sweet increases its quantity correctly.
    """
    headers = await get_auth_headers(client)
    # Create sweet
    create_resp = await client.post("/api/sweets", json={
        "name": "Barfi", "category": "Indian", "price": 18.0, "quantity": 40
    }, headers=headers)
    assert create_resp.status_code == 201
    sweet_id = create_resp.json()["_id"]

    # Restock sweet by 20
    restock_resp = await client.patch(
        f"/api/sweets/{sweet_id}/restock",
        params={"quantity": 20},
        headers=headers
    )
    assert restock_resp.status_code == 200
    assert restock_resp.json()["quantity"] == 60  # 40 + 20
