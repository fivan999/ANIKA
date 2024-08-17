from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.ext.declarative import declarative_base

from src.config import settings

url = (
    f'postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASS}'
    f'@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}'
)

engine = create_async_engine(url=url, echo=True)
SessionLocal = async_sessionmaker(engine, expire_on_commit=False)
Base = declarative_base()


async def get_db():
    async with SessionLocal() as db:
        try:
            yield db
        finally:
            await db.close()
