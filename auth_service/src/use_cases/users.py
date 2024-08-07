from src.repositories.users import UserRepository
from src.schemes.tokens import AccessAndRefreshTokenScheme, AccessTokenScheme
from src.schemes.users import UserFullScheme, UserLoginScheme
from src.utils.enums import TokenEnum, UserEnum
from src.utils.password import verify_password
from src.utils.tokens import (
    create_access_or_refresh_token,
    get_validated_token_data,
)


class UserUseCase:
    def __init__(self, repository: UserRepository) -> None:
        """
        Initializing of user use case

        Args:
            repository (UserRepository): user repository
        """
        self.repository = repository

    async def get_user_by_username(
        self, username: str
    ) -> tuple[UserEnum, UserFullScheme]:
        """
        Getting a user by username

        Args:
            username (str)

        Returns:
            tuple[UserEnum, UserFullScheme]: Enum with status and user's data
        """
        user_get_status, user_result_data = (
            await self.repository.get_user_by_username(username)
        )
        if user_get_status != UserEnum.USER_EXISTS:
            return user_get_status, None
        return UserEnum.USER_EXISTS, user_result_data

    async def get_user_by_token(
        self, token: str, token_type: str
    ) -> tuple[UserEnum | TokenEnum, UserFullScheme | None]:
        """
        Getting user's data by jwt token

        Args:
            token (str): jwt token
            token_type (str): type of a token (access or refresh)

        Returns:
            tuple[
                UserEnum, UserFullScheme | None
            ]: Enum with getting status and user's data
        """
        token_status, payload = get_validated_token_data(token, token_type)
        if token_status != TokenEnum.TOKEN_IS_VALID:
            return token_status, None
        result_status, result_user = (
            await self.repository.get_user_by_username(payload.get('sub'))
        )
        if result_status == UserEnum.USER_NOT_EXISTS:
            return UserEnum.USER_NOT_EXISTS, None
        return UserEnum.USER_EXISTS, result_user

    async def get_access_and_refresh_token(
        self, user_data: UserLoginScheme
    ) -> tuple[UserEnum, AccessAndRefreshTokenScheme | None]:
        """
        Creating access and refresh token for user

        Args:
            user_data (UserLoginScheme): user's data

        Returns:
            tuple[
                UserEnum, AccessAndRefreshToken | None
            ]: Enum with creating status and tokens
        """
        user_get_status, user_result_data = await self.get_user_by_username(
            user_data.username
        )
        if user_get_status != UserEnum.USER_EXISTS:
            return user_get_status, None
        if not verify_password(
            user_data.password, user_result_data.hashed_password
        ):
            return UserEnum.WRONG_PASSWORD, None

        token_sub = user_result_data.username
        return UserEnum.SUCCESS_LOGIN, AccessAndRefreshTokenScheme(
            access_token=create_access_or_refresh_token(
                sub=token_sub, token_type='access_token'
            ),
            refresh_token=create_access_or_refresh_token(
                sub=token_sub, token_type='refresh_token'
            ),
        )

    async def get_new_access_token_by_refresh_token(
        self, token: str
    ) -> tuple[UserEnum | TokenEnum, AccessTokenScheme | None]:
        """
        Getting a new access token by resresh token

        Args:
            token (str): refresh token

        Returns:
            tuple[
                UserEnum | TokenEnum, AccessTokenScheme | None
            ]: Enum with getting status and access token
        """
        result_status, result_user = await self.get_user_by_token(
            token, 'refresh_token'
        )
        if result_status != UserEnum.USER_EXISTS:
            return result_status, None
        access_token = create_access_or_refresh_token(
            result_user.username, 'access_token'
        )
        return TokenEnum.TOKEN_IS_VALID, AccessTokenScheme(
            access_token=access_token
        )
