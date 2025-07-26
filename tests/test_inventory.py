import pytest

@pytest.mark.asyncio
async def test_purchase_sweet(client):
    headers = {"Authorization": "Bearer fake-token"}
    sweet = await client.post("/api/sweets", json={
        "name": "Gulab Jamun", "category": "Dessert", "price": 10, "quantity": 5
    }, headers=headers)
    sweet_id = sweet.json()["id"]
    response = await client.post(f"/api/sweets/{sweet_id}/purchase", headers=headers)
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_restock_sweet(client):
    headers = {"Authorization": "Bearer fake-token"}
    sweet = await client.post("/api/sweets", json={
        "name": "Kaju Katli", "category": "Premium", "price": 25, "quantity": 10
    }, headers=headers)
    sweet_id = sweet.json()["id"]
    response = await client.post(f"/api/sweets/{sweet_id}/restock", headers=headers)
    assert response.status_code == 200
