from typing import AsyncGenerator, Generator

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from testcontainers.postgres import PostgresContainer

from src.db.base import Base


@pytest.fixture(scope='session')
def postgres_container() -> Generator:
    """
    getting a postgres db container

    Yields:
        Generator: postgres container obj
    """
    postgres_container = PostgresContainer(
        image='postgres:16-alpine3.19',
        driver='asyncpg',
    )
    try:
        postgres_container.start()
        yield postgres_container
    finally:
        postgres_container.stop()


@pytest_asyncio.fixture(scope='session')
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
        url=postgres_container.get_connection_url(),
        echo=True,
    )
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    return async_sessionmaker(engine, expire_on_commit=False)


@pytest_asyncio.fixture(scope='function')
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
            await session.close()
