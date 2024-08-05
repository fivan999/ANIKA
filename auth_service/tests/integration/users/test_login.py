import pytest
from httpx import AsyncClient
from src.config import DBConfig
from src.dependencies.config import get_db_config


@pytest.mark.asyncio
async def test_success_login(fastapi_test_client: AsyncClient) -> None:
    response = await fastapi_test_client.post(
        url='/auth/token',
        json={'username': 'user1', 'password': 'password1'},
    )
    response_json = response.json()
    assert response.status_code == 200
    assert 'access_token' in response_json
    assert 'refresh_token' in response_json
