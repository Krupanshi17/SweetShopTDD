import pytest

#  This test checks if a user can register successfully
@pytest.mark.asyncio
async def test_register_user(client):
    # Send a POST request to /api/auth/register with email and password
    response = await client.post("/api/auth/register", json={
        "email": "test@example.com",
        "password": "StrongPass123"
    })

    #  This will FAIL if:
    # - The /api/auth/register route doesn't exist (404 Not Found)
    # - Or if the route exists but returns wrong status code (not 201)
    assert response.status_code == 201

    #  This will FAIL if:
    # - The response JSON doesn’t include "access_token"
    #   (i.e., the route returns something else or nothing)
    assert "access_token" in response.json()


#  This test checks if a user can log in successfully
@pytest.mark.asyncio
async def test_login_user(client):
    #  First register the user so we can try logging in
    await client.post("/api/auth/register", json={
        "email": "loginuser@example.com",
        "password": "StrongPass123"
    })

    #  Then send a POST request to /api/auth/login with the same credentials
    response = await client.post("/api/auth/login", json={
        "email": "loginuser@example.com",
        "password": "StrongPass123"
    })

    #  This will FAIL if:
    # - The /api/auth/login route doesn't exist (404 Not Found)
    # - Or the login logic returns wrong status (e.g., 401 Unauthorized)
    assert response.status_code == 200

    #  This will FAIL if:
    # - The login route doesn't return a valid access token
    #   (e.g., missing or incorrect response key)
    assert "access_token" in response.json()
