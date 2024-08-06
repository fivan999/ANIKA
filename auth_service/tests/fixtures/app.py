from typing import AsyncGenerator

import pytest_asyncio
from fastapi.testclient import TestClient
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import async_sessionmaker

from src.main import app


@pytest_asyncio.fixture
async def fastapi_test_client(
    async_db_sessionmaker: async_sessionmaker,
) -> AsyncGenerator[AsyncClient, None]:
    """
    async fixture that creates an async test client

    Args:
        async_db_sessionmaker (async_sessionmaker)

    Yields:
        AsyncGenerator[
            AsyncClient, None, None
        ]: generator that yields an AsyncClient
    """
    with TestClient(app):
        async with AsyncClient(app=app, base_url='http://test') as client:
            app.state.async_sessionmaker = async_db_sessionmaker
            yield client
