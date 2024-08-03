from typing import Any, Optional, List

from fastapi import Body
from pydantic import BaseModel


class SearchQuery(BaseModel):
    limit: int | None = None

    topic_ids: Optional[List[int]] = None
    unique_ids: Optional[List[int]] = None

    match: Optional[dict] = None
    sort: Optional[dict] = None

class SendQuery(BaseModel):
    topic_id: int
    unique_id: Optional[int] = None
    payload: Any = Body(None)
