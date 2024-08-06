from typing import Generator

import pytest
import pytest_asyncio
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import Session, sessionmaker
from testcontainers.postgres import PostgresContainer

from tests.utils.db import clear_db_tables, recreate_db_tables


@pytest.fixture(scope='session')
def postgres_container() -> Generator[PostgresContainer, None, None]:
    """
    creates test postgres container and yields it

    Yields:
        Generator[
            PostgresContainer, None, None
        ]: generator with postgres container
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
def db_engine(
    postgres_container: PostgresContainer,
) -> Engine:
    """
    creates sync db engine and recreates database

    Args:
        postgres_container (PostgresContainer): test postgres container

    Returns:
        Engine: engine objects
    """
    engine = create_engine(
        url=postgres_container.get_connection_url().replace(
            'asyncpg', 'psycopg2'
        ),
        echo=True,
    )
    recreate_db_tables(engine)
    return engine


@pytest.fixture(scope='session')
def db_sessionmaker(
    db_engine: Engine,
) -> sessionmaker:
    """
    fixture for getting sync sessionmaker

    Args:
        db_engine (Engine)

    Returns:
        async_sessionmaker
    """
    db_sessionmaker = sessionmaker(
        db_engine, autoflush=False, autocommit=False, expire_on_commit=False
    )
    return db_sessionmaker


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
def db_session(
    db_sessionmaker: sessionmaker,
) -> Generator[Session, None, None]:
    """
    fixture that creates a session and clears a database

    Args:
        db_sessionmaker (sessionmaker)

    Yields:
        Generator[Session, None, None]: generator that yields session obj
    """
    session = db_sessionmaker()
    try:
        yield session
    finally:
        session.close()
        clear_db_tables(db_sessionmaker)
