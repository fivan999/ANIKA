from typing import Optional

from pydantic import BaseModel


class Message(BaseModel):
    _id: Optional[int] = None
    unique_id: Optional[int]
    topic_id: int
    payload: dict