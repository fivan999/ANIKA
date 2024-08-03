import json
from typing import List, Optional, Any

from src.database.managers import MessagesManager
from src.schemas.exceptions import PermissionsError
from src.schemas.responses import MessageOutput


class SearchEngine:
    def __init__(self, messages_manager: MessagesManager):
        self._messages_manager = messages_manager

    async def search(self, topic_ids: Optional[List[int]], unique_ids: Optional[List[int]] = None,
                     match: Optional[dict] = None, sort: Optional[dict] = None, limit: Optional[int] = None) -> dict[
                                                                                                                    str,
                                                                                                                    list[
                                                                                                                        Any]] | \
                                                                                                                tuple[
                                                                                                                    list[
                                                                                                                        MessageOutput], Any]:

        pipeline = [{"$match": {"topic_id": {"$in": topic_ids}}}]

        if unique_ids:
            pipeline.append({"$match": {"unique_id": {"$in": unique_ids}}})

        if match:
            if '$where' in json.dumps(match):
                raise PermissionsError
            pipeline.append({"$match": match})

        if sort:
            if '$where' in json.dumps(sort):
                raise PermissionsError
            pipeline.append({"$sort": sort})

        if limit:
            pipeline.append({"$limit": limit})

        pipeline.append({
            "$group": {
                "_id": None,
                "messages": {"$push": "$$ROOT"},
                "unique_ids": {"$addToSet": "$unique_id"}
            }
        })

        result = await self._messages_manager.aggregate_messages(pipeline=pipeline)
        if not result:
            return {"messages": [], "unique_ids": []}

        aggregation_result = result[0]
        messages = [MessageOutput(**data) for data in aggregation_result["messages"]]
        unique_ids = aggregation_result["unique_ids"]

        return messages, unique_ids