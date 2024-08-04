import pytest
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.users import User
from src.utils.password import get_hashed_password


@pytest.fixture(scope='function')
async def user1(async_session: AsyncSession) -> User:
    """
    fixture to create test user1

    Args:
        async_session (AsyncSession): async session obj

    Returns:
        User: user model
    """
    user_create_query = (
        insert(User)
        .values(
            {
                'username': 'user1',
                'email': 'user1@example.com',
                'hashed_password': get_hashed_password('password1'),
                'partner_id': 1,
            }
        )
        .returning(User)
    )
    user_obj = await async_session.execute(user_create_query)
    user_obj = user_obj.scalar()
    await async_session.commit()
    await async_session.close()
    return user_obj
