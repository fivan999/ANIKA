from typing import Optional, List

from pydantic import BaseModel, Field


class MessageOutput(BaseModel):
    topic_id: int
    payload: dict
    unique_id: Optional[int] = None


class SearchOutput(BaseModel):
    messages: list[MessageOutput] = Field(default_factory=list)
    unique_ids: List[int] = Field(default_factory=list)
