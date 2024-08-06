import pytest
from sqlalchemy.orm import Session

from src.models.users import User
from src.utils.password import get_hashed_password


@pytest.fixture(scope='function')
def user1(db_session: Session) -> User:
    """
    fixture to create test user1

    Args:
        async_session (AsyncSession): async session obj

    Returns:
        User: user model
    """
    user_obj = User(
        username='user1',
        email='user1@example.com',
        hashed_password=get_hashed_password('password1'),
        partner_id=1,
    )
    with db_session.begin():
        db_session.add(user_obj)
        db_session.commit()
        db_session.refresh(user_obj)
        yield user_obj
