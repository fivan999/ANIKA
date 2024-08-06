from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.users import User
from src.schemes.users import UserFullScheme
from src.utils.enums import UserEnum


class UserRepository:
    def __init__(self, session: AsyncSession) -> None:
        """initializing of user repository

        Args:
            session (AsyncSession): async database session object
        """
        self.session = session

    async def get_user_by_username(
        self, username: str
    ) -> tuple[UserEnum, UserFullScheme | None]:
        """
        get user by his username

        Args:
            username (str)

        Returns:
            tuple[
                UserEnum, UserFullScheme | None
            ]: User data and enum status of getting user
        """
        user_query = select(User).where(User.username == username)
        user_result = await self.session.execute(user_query)
        user_obj = user_result.scalar()
        if user_obj is None:
            return UserEnum.USER_NOT_EXISTS, None
        return UserEnum.USER_EXISTS, UserFullScheme(**user_obj.__dict__)
