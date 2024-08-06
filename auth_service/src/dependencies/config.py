from functools import lru_cache

from src.config import DBConfig, JWTConfig, Settings


@lru_cache
def get_settings() -> Settings:
    return Settings()


def get_db_config() -> DBConfig:
    return DBConfig(
        connection_url=(
            f'postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASS}'
            f'@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}'
        )
    )


def get_jwt_config() -> JWTConfig:
    return JWTConfig(
        jwt_secret_key=settings.JWT_SECRET_KEY,
        access_token_expire_minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
        refresh_token_expire_minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES,
    )


settings = get_settings()
db_config = get_db_config()
jwt_config = get_jwt_config()
