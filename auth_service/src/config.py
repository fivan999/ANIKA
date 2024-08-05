from dataclasses import dataclass

from pydantic_settings import BaseSettings, SettingsConfigDict
from fastapi import Depends
from typing import Annotated
from functools import lru_cache


class Settings(BaseSettings):
    JWT_SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_MINUTES: int
    DB_NAME: str
    DB_USER: str
    DB_PASS: str
    DB_HOST: str
    DB_PORT: str

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore',
    )


@dataclass
class DBConfig:
    connection_url: str


@dataclass
class JWTConfig:
    jwt_secret_key: str
    access_token_expire_minutes: int
    refresh_token_expire_minutes: int


@lru_cache
def get_settings() -> Settings:
    return Settings()


SettingsDep = Annotated[Settings, Depends(get_settings)]
