from typing import List, Dict, Any

from src.database.models import Message
from src.database.repository import MongoDBRepository


class MessagesManager:
    def __init__(self, repository: MongoDBRepository):
        self._repository = repository

    async def create_message(self, message: Message) -> str:
        document = message.dict(by_alias=True)
        return await self._repository.create('messages', document)

    async def aggregate_messages(self, pipeline: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        return await self._repository.aggregate('messages', pipeline)
