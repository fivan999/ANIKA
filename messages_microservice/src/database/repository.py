import motor.motor_asyncio
from typing import List, Any, Dict, Optional, Mapping

class MongoDBRepository:
    def __init__(self, host: str, port: int, db_name: str, username: Optional[str] = None, password: Optional[str] = None):
        self._host = host
        self._port = port
        self._db_name = db_name
        self._username = username
        self._password = password
        self._client = motor.motor_asyncio.AsyncIOMotorClient(self.url)
        self._db = self._client[self._db_name]

    @property
    def url(self) -> str:
        if self._username and self._password:
            return f'mongodb://{self._username}:{self._password}@{self._host}:{self._port}'
        return f'mongodb://{self._host}:{self._port}'

    async def create(self, collection: str, document: Dict[str, Any]) -> str:
        result = await self._db[collection].insert_one(document)
        return str(result.inserted_id)

    async def aggregate(self, collection: str, pipeline: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        cursor = self._db[collection].aggregate(pipeline)
        result = []
        async for document in cursor:
            result.append(document)
        return result

    async def find(self, collection: str, query: Dict[str, Any]) -> Optional[Mapping[str, Any]]:
        document = await self._db[collection].find_one(query)
        if document:
            return document
        return None

    async def update(self, collection: str, query: Dict[str, Any], update: Dict[str, Any]) -> int:
        result = await self._db[collection].update_one(query, {'$set': update})
        return result.modified_count

    async def delete(self, collection: str, query: Dict[str, Any]) -> int:
        result = await self._db[collection].delete_one(query)
        return result.deleted_count
