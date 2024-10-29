import pytest
from httpx import AsyncClient
from test_config import ac

@pytest.mark.asyncio
async def test_first_point(ac: AsyncClient):
    response = await ac.get("/")
    assert response.status_code == 200


