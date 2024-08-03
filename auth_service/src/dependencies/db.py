from typing import Annotated, AsyncGenerator

from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker


async def get_async_sessionmaker(request: Request) -> async_sessionmaker:
    """
    Getting db sessions' factory from request state

    Args:
        request (Request): fastapi request object

    Returns:
        async_sessionmaker: db sessions' factory
    """
    return request.app.state.async_sessionmaker


async def get_session(
    async_sessionmaker: Annotated[
        async_sessionmaker, Depends(get_async_sessionmaker)
    ]
) -> AsyncGenerator:
    """
    Getting db session

    Args:
        async_sessionmaker (Annotated[
            async_sessionmaker, Depends
        ]): db sessions' factory

    Yields:
        Iterator[AsyncGenerator]: async session object
    """
    async with async_sessionmaker() as session:
        yield session


DatabaseDep = Annotated[AsyncSession, Depends(get_session)]
