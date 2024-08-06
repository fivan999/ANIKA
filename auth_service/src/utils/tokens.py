import datetime
from typing import Annotated

import jwt
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import ExpiredSignatureError, PyJWTError

from src.dependencies.config import jwt_config
from src.utils.enums import TokenEnum


def create_access_or_refresh_token(
    sub: str, token_type: str
) -> str:
    """
    Creating a jwt token with

    Args:
        sub (str): useful data
        token_type (str): type of a token (access or refresh)

    Returns:
        str: jwt token
    """
    data_to_encode = {'sub': sub, 'token_type': token_type}
    creation_time = datetime.datetime.now(datetime.timezone.utc)
    data_to_encode['iat'] = creation_time
    if token_type == 'access_token':
        data_to_encode['exp'] = creation_time + datetime.timedelta(
            minutes=jwt_config.access_token_expire_minutes
        )
    elif token_type == 'refresh_token':
        data_to_encode['exp'] = creation_time + datetime.timedelta(
            minutes=jwt_config.refresh_token_expire_minutes
        )
    return jwt.encode(
        data_to_encode, jwt_config.jwt_secret_key, algorithm='HS256'
    )


def decode_jwt_token(token: str) -> dict:
    """
    Getting payload of a jwt token

    Args:
        token (str): jwt token

    Returns:
        dict: payload
    """
    payload = jwt.decode(
        token, jwt_config.jwt_secret_key, algorithms=['HS256']
    )
    return payload


def get_validated_token_data(
    token: str, expected_token_type: str
) -> tuple[TokenEnum, dict | None]:
    """
    Validate jwt token and get payload

    Args:
        token (str): jwt token
        expected_token_type (str): type of a token (access or refresh)

    Returns:
        tuple[TokenEnum, dict | None]: Enum with status and payload
    """
    try:
        payload = decode_jwt_token(token)
    except ExpiredSignatureError:
        return TokenEnum.TOKEN_EXPIRED, None
    except PyJWTError:
        return TokenEnum.INVALID_TOKEN, None
    username = payload.get('sub')
    token_type = payload.get('token_type')
    if (
        username is None
        or token_type is None
        or token_type != expected_token_type
    ):
        return TokenEnum.INVALID_TOKEN, None
    return TokenEnum.TOKEN_IS_VALID, payload


def get_jwt_bearer_token(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(HTTPBearer())]
) -> str:
    """
    Getting jwt token from Authorization header

    Args:
        credentials (Annotated[HTTPAuthorizationCredentials, Depends)

    Returns:
        str: jwt token
    """
    return credentials.credentials
