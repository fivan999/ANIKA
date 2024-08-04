from pydantic import BaseModel


class ErrorScheme(BaseModel):
    detail: str
