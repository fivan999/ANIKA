import pytest_asyncio
from src.main import app
from httpx import AsyncClient
from testcontainers.postgres import PostgresContainer
from src.config import DBConfig
from fastapi.testclient import TestClient
from src.dependencies.config import get_db_config
from typing import AsyncGenerator


@pytest_asyncio.fixture(scope='function')
async def fastapi_test_client(
    postgres_container: PostgresContainer, mocker
) -> AsyncGenerator:
    """
    fixture for getting async test client

    Args:
        postgres_container (PostgresContainer)

    Returns:
        AsyncClient: async test client
    """
    mocker.patch('src.dependencies.config.get_db_config', return_value=DBConfig(connection_url=postgres_container.get_connection_url()))
    print('------------------')
    print(get_db_config().connection_url)
    print(postgres_container.get_connection_url())
    print('------------------')
    with TestClient(app):
        async with AsyncClient(app=app, base_url='http://test') as client:
            # print(app.state.)
            yield client
