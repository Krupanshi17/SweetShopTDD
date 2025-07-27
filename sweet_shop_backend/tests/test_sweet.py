import pytest
from httpx import AsyncClient
from httpx._transports.asgi import ASGITransport
from app.main import app
import uuid

def generate_unique_email():
    """
    Generate a unique email address for testing to avoid conflicts.
    This ensures each test registers a distinct user, avoiding state clashes.
    """
    return f"user_{uuid.uuid4()}@example.com"

async def get_auth_headers(ac: AsyncClient) -> dict:
    """
    Helper function to register and login a user to get valid JWT auth headers.
    Promotes DRY by reusing authentication steps in multiple tests.
    
    :param ac: AsyncClient instance to perform HTTP calls.
    :return: Dict containing Authorization header with Bearer token.
    """
    email = generate_unique_email()
    password = "Secret123"

    # Register user for test isolation
    await ac.post("/api/auth/register", json={
        "email": email,
        "password": password
    })

    # Login to obtain access token
    login_response = await ac.post("/api/auth/login", json={
        "email": email,
        "password": password
    })
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

@pytest.mark.asyncio
async def test_create_sweet_unauthorized():
    """
    Test creating a sweet with invalid auth token results in unauthorized response.
    Assertion deliberately fails to simulate failure scenario.
    """
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
    """
    Test fetching all sweets returns a list.
    Assertion deliberately fails by expecting wrong status code and type.
    """
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/api/sweets")
    assert response.status_code == 999  # Fail on purpose
    assert isinstance(response.json(), dict)  # Force fail (should be list)

@pytest.mark.asyncio
async def test_search_sweets_success():
    """
    Test searching sweets with filters returns a list.
    Assertion deliberately fails by expecting wrong status code and type.
    """
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
    """
    Test successful sweet creation with valid authorization.
    Assertions deliberately fail on status code and response content.
    """
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
    """
    Test updating an existing sweet.
    Assertions deliberately fail on status and updated data verification.
    """
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
    """
    Test deleting an existing sweet.
    Assertions deliberately fail on status and response message.
    """
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
    """
    Test restocking a sweet increases quantity.
    Assertions deliberately fail on status and quantity.
    """
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
