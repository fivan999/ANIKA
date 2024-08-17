<<<<<<< HEAD:auth_service/src/config.py
from dataclasses import dataclass
from functools import lru_cache
from typing import Annotated

from fastapi import Depends
=======
import logging

>>>>>>> origin/data-name-id:topics_microservice/src/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
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


<<<<<<< HEAD:auth_service/src/config.py
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
=======
settings = Settings()

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
>>>>>>> origin/data-name-id:topics_microservice/src/config.py
