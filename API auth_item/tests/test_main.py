import pytest
from httpx import AsyncClient
from main import app


@pytest.mark.asyncio
async def test_first_point():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_register_user():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/register/",
            json={"username": "testuser",
                  "password": "testpassword",
                  "email": "test@example.com"
                  })
    assert response.status_code == 307


@pytest.mark.asyncio
async def test_login_user():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/login/",
            data={"username": "testuser",
                  "password": "testpassword"})
    assert response.status_code == 307
