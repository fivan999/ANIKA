from pydantic import BaseModel, EmailStr


class UserShowScheme(BaseModel):
    id: int
    username: str
    email: EmailStr
    partner_id: int


class UserFullScheme(UserShowScheme):
    hashed_password: str


class UserAuthorizationScheme(BaseModel):
    user_id: int
    partner_id: int


class UserLoginScheme(BaseModel):
    username: str
    password: str
