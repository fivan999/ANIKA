import pytest
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import async_sessionmaker

from src.main import app


@pytest.fixture(scope='session')
async def fastapi_application(
    async_db_sessionmaker: async_sessionmaker,
) -> FastAPI:
    """
    fixture for getting fastapi application

    Args:
        async_db_sessionmaker (async_sessionmaker)

    Returns:
        FastAPI: fastapi application object
    """
    app.state.async_sessionmaker = async_db_sessionmaker
    return app
