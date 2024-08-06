from pydantic import BaseModel


class AccessTokenScheme(BaseModel):
    access_token: str


class AccessAndRefreshTokenScheme(AccessTokenScheme):
    refresh_token: str
