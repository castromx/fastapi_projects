import pytest
from httpx import AsyncClient
from test_config import ac


@pytest.mark.asyncio
async def test_first_point(ac: AsyncClient):
    response = await ac.get("/")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_register_user(ac: AsyncClient):
    response = await ac.post(
        "/register/",
        json={"username": "testuser",
                "password": "testpassword",
              "email": "test@example.com"
              })
    assert response.status_code == 307


@pytest.mark.asyncio
async def test_login_user(ac: AsyncClient):
    response = await ac.post(
        "/login/",
        data={"username": "testuser",
              "password": "testpassword"})
    assert response.status_code == 307
