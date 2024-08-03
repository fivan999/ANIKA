from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.ext.declarative import declarative_base

from src.config import settings


Base = declarative_base()


async def init_database() -> async_sessionmaker:
    """
    Creating db sessions' factory

    Returns:
        async_sessionmaker: session factory
    """
    engine = create_async_engine(
        url=f'postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASS}'
        f'@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}',
        echo=True,
    )
    return async_sessionmaker(engine, expire_on_commit=False)
