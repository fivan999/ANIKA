from typing import Generator

import pytest
import pytest_asyncio
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import sessionmaker
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


@pytest.fixture(scope='session')
def db_sessionmaker(
    postgres_container: PostgresContainer,
) -> async_sessionmaker:
    """
    fixture for getting async sessionmaker

    Args:
        postgres_container (PostgresContainer)

    Returns:
        async_sessionmaker
    """
    engine = create_engine(
        url=postgres_container.get_connection_url().replace(
            'asyncpg', 'psycopg2'
        ),
        echo=True,
    )
    Base.metadata.create_all(engine)
    return sessionmaker(
        bind=engine, autoflush=False, autocommit=False, expire_on_commit=False
    )


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
    return async_sessionmaker(
        bind=engine, expire_on_commit=False, autoflush=False, autocommit=False
    )


@pytest.fixture(scope='function')
def db_session(db_sessionmaker: sessionmaker) -> Generator:
    """
    fixture for getting async session

    Args:
        async_db_sessionmaker (async_sessionmaker): async session maker

    Returns:
        AsyncGenerator
    """
    db_session = db_sessionmaker()
    try:
        yield db_session
    finally:
        db_session.close()
