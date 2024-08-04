from enum import Enum


class UserEnum(Enum):
    USER_EXISTS = 'user exists'
    WRONG_PASSWORD = 'wrong password'
    USER_NOT_EXISTS = 'user not exists'
    SUCCESS_LOGIN = 'success login'


class TokenEnum(Enum):
    INVALID_TOKEN = 'invalid token'
    TOKEN_EXPIRED = 'token expired'
    TOKEN_IS_VALID = 'token is valid'
