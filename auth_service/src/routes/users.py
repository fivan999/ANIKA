from typing import Annotated

from fastapi import APIRouter, Body, HTTPException, status, Response

from src.dependencies.users import CurrentUserDep, UserUseCaseDep
from src.schemes.errors import ErrorScheme
from src.schemes.tokens import AccessAndRefreshTokenScheme, AccessTokenScheme
from src.schemes.users import (
    UserAuthorizationScheme,
    UserLoginScheme,
    UserShowScheme,
)
from src.utils.enums import TokenEnum, UserEnum


auth_router = APIRouter(prefix='/auth', tags=['Auth'])


@auth_router.post(
    '/token',
    status_code=status.HTTP_200_OK,
    responses={
        200: {'description': 'Refresh and access token'},
        403: {'description': 'Invalid user data', 'model': ErrorScheme},
    },
)
async def user_login(
    user_data: UserLoginScheme, user_use_case: UserUseCaseDep
) -> AccessAndRefreshTokenScheme:
    result_status, result_data = (
        await user_use_case.get_access_and_refresh_token(user_data)
    )
    if result_status != UserEnum.SUCCESS_LOGIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=result_status.value
        )
    return result_data


@auth_router.post(
    '/refresh',
    status_code=status.HTTP_200_OK,
    responses={
        200: {'description': 'New access token'},
        403: {'description': 'Invalid refresh token', 'model': ErrorScheme},
    },
)
async def get_new_access_token(
    refresh_token: Annotated[str, Body(embed=True)],
    user_use_case: UserUseCaseDep,
) -> AccessTokenScheme:
    result_status, token = (
        await user_use_case.get_new_access_token_by_refresh_token(
            refresh_token
        )
    )
    if result_status != TokenEnum.TOKEN_IS_VALID:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=result_status.value,
        )
    return token


@auth_router.get(
    '/authorization',
    status_code=status.HTTP_200_OK,
    responses={
        200: {'description': 'User data'},
        401: {'description': 'Unauthorized', 'model': ErrorScheme},
    },
)
async def get_user_id_and_partner_id(
    current_user: CurrentUserDep, response: Response
) -> UserAuthorizationScheme:
    response.headers['X-User-Id'] = str(current_user.id)
    response.headers['X-Partner-Id'] = str(current_user.partner_id)
    return UserAuthorizationScheme(
        user_id=current_user.id, partner_id=current_user.partner_id
    )


@auth_router.get(
    '/me',
    status_code=status.HTTP_200_OK,
    responses={
        200: {'description': 'User data'},
        401: {'description': 'Unauthorized', 'model': ErrorScheme},
    },
)
async def get_current_user(current_user: CurrentUserDep) -> UserShowScheme:
    return current_user
