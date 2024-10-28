from httpx import AsyncClient
from test_config import ac


async def test_first_point(ac: AsyncClient):
    response = await ac.get("/")
    assert response.status_code == 200