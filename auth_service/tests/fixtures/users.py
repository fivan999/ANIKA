import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.orm import Session

from src.models.users import User
from src.utils.password import get_hashed_password


@pytest.fixture(scope='function')
def user1(db_session: Session) -> User:
    """
    fixture to create test user1

    Args:
        db_session (Session): sync session obj

    Returns:
        User: user model
    """
    user_obj = User(
        username='user1',
        email='user1@example.com',
        hashed_password=get_hashed_password('password1'),
        partner_id=1,
    )
    db_session.add(user_obj)
    db_session.commit()
    db_session.refresh(user_obj)
    return user_obj


@pytest_asyncio.fixture(scope='function')
async def access_and_refresh_token1(
    fastapi_test_client: AsyncClient, user1: User
) -> str:
    """
    fixture to get access_token for user1

    Args:
        fastapi_test_client (AsyncClient): async test client
        user1 (User): user1 obj

    Returns:
        str: access token
    """
    response = await fastapi_test_client.post(
        url='/auth/token',
        json={'username': 'user1', 'password': 'password1'},
    )
    return response.json()
