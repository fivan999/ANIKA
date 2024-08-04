import os
from typing import AsyncGenerator

import pytest
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from testcontainers.postgres import PostgresContainer


@pytest.fixture(scope='session')
def postgres_container() -> PostgresContainer:
    """
    fixture for getting a postgres container for testing

    Returns:
        PostgresContainer
    """
    postgres_container = PostgresContainer(
        image='postgres:16-alpine3.19',
        username='postgres',
        password='postgres',
        port=5433,
        dbname='postgres',
        driver='postgresql+asyncpg',
    )
    if os.name == 'nt':
        postgres_container.get_container_host_ip = lambda: 'localhost'
    return postgres_container


@pytest.fixture(scope='session')
async def async_db_sessionmaker(
    postgres_container: PostgresContainer,
) -> async_sessionmaker:
    """
    fixture for getting async sessionmaker

    Args:
        postgres_container (PostgresContainer)

    Returns:
        async_sessionmaker
    """
    engine = create_async_engine(
        url='postgresql+asyncpg://postgres:postgres'
        '@localhost:5433/postgres',
        echo=True,
    )
    return async_sessionmaker(engine, expire_on_commit=False)


@pytest.fixture(scope='function')
async def async_session(
    async_db_sessionmaker: async_sessionmaker,
) -> AsyncGenerator:
    """
    fixture for getting async session

    Args:
        async_db_sessionmaker (async_sessionmaker): async session maker

    Returns:
        AsyncGenerator
    """
    async with async_db_sessionmaker() as session:
        try:
            yield session
        finally:
            session.close()
