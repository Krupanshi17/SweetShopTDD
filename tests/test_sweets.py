import pytest

@pytest.mark.asyncio
async def test_create_sweet(client):
    # TODO: Implement auth & token logic
    headers = {"Authorization": "Bearer fake-token"}
    response = await client.post("/api/sweets", json={
        "name": "Ladoo", "category": "Festival", "price": 20, "quantity": 100
    }, headers=headers)
    assert response.status_code == 201

@pytest.mark.asyncio
async def test_get_sweets(client):
    headers = {"Authorization": "Bearer fake-token"}
    response = await client.get("/api/sweets", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)
