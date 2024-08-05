from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base


Base = declarative_base()


async def init_database(database_url: str) -> async_sessionmaker:
    """
    Creating db sessions' factory

    Returns:
        async_sessionmaker: session factory
    """
    engine = create_async_engine(
        database_url,
        echo=True,
    )
    return async_sessionmaker(engine, expire_on_commit=False)
