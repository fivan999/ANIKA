from typing import Annotated

from fastapi import Depends, HTTPException, status

from src.dependencies.db import DatabaseDep
from src.dependencies.tokens import JWTTokenDep
from src.repositories.users import UserRepository
from src.schemes.users import UserFullScheme
from src.use_cases.users import UserUseCase
from src.utils.enums import UserEnum


async def get_user_repository(db: DatabaseDep) -> UserRepository:
    return UserRepository(db)


UserRepositoryDep = Annotated[UserRepository, Depends(get_user_repository)]


async def get_user_use_case(user_repository: UserRepositoryDep) -> UserUseCase:
    return UserUseCase(user_repository)


UserUseCaseDep = Annotated[UserUseCase, Depends(get_user_use_case)]


async def get_current_user_by_access_token(
    token: JWTTokenDep, user_use_case: UserUseCaseDep
) -> UserFullScheme:
    """
    Getting user's data from jwt token

    Args:
        token (JWTTokenDep): jwt token
        user_use_case (UserUseCaseDep): user's use case

    Raises:
        HTTPException: user does not exists

    Returns:
        UserFullScheme: scheme with user's data
    """
    result_status, result_user = await user_use_case.get_user_by_token(
        token, 'access_token'
    )
    if result_status != UserEnum.USER_EXISTS:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=result_status.value,
        )
    return result_user


CurrentUserDep = Annotated[
    UserFullScheme, Depends(get_current_user_by_access_token)
]
