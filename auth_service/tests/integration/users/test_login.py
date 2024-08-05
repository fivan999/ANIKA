import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from testcontainers.postgres import PostgresContainer

from src.config import DBConfig
from src.main import app
from src.models.users import User


@pytest.mark.asyncio
async def test_success_login(
    postgres_container: PostgresContainer, user1: User, mocker
) -> None:
    mock_get_db_config = mocker.patch('src.dependencies.db.get_db_config')
    mock_get_db_config.return_value = DBConfig(
        connection_url=postgres_container.get_connection_url()
    )
    print('----------------')
    print(postgres_container.get_connection_url())
    print('----------------------')
    with TestClient(app):
        async with AsyncClient(app=app, base_url='http://test') as client:
            response = await client.post(
                url='/auth/token',
                json={'username': 'user1', 'password': 'password1'},
            )
    response_json = response.json()
    assert response.status_code == 200
    assert 'access_token' in response_json
    assert 'refresh_token' in response_json
