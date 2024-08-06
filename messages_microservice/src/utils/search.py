import json
from typing import List, Optional, Any

from src.database.managers import MessagesManager
from src.schemas.exceptions import PermissionsError
from src.schemas.responses import MessageOutput


class SearchEngine:
    """Поисковый движок для выполнения запросов поиска сообщений.

    Атрибуты:
        _messages_manager (MessagesManager): Менеджер сообщений для взаимодействия с базой данных.
    """

    def __init__(self, messages_manager: MessagesManager):
        """Инициализирует экземпляр SearchEngine с указанным менеджером сообщений.

        Args:
            messages_manager (MessagesManager): Менеджер сообщений для выполнения запросов к базе данных.
        """
        self._messages_manager = messages_manager

    async def search(self, topic_ids: Optional[List[int]], unique_ids: Optional[List[int]] = None,
                     match: Optional[dict] = None, sort: Optional[dict] = None, limit: Optional[int] = None) -> \
            dict[str, list[Any]] | tuple[list[MessageOutput], Any]:
        """Выполняет поиск сообщений по заданным критериям и возвращает результаты поиска.

        Args:
            topic_ids (Optional[List[int]]): Список идентификаторов тем для поиска.
            unique_ids (Optional[List[int]], optional): Список уникальных идентификаторов сообщений для поиска. По умолчанию None.
            match (Optional[dict], optional): Критерии для сопоставления сообщений. По умолчанию None.
            sort (Optional[dict], optional): Параметры сортировки сообщений. По умолчанию None.
            limit (Optional[int], optional): Максимальное количество результатов. По умолчанию None.

        Returns:
            dict[str, list[Any]] | tuple[list[MessageOutput], Any]:
                Словарь с ключами "messages" и "unique_ids", если результат пустой.
                Кортеж, содержащий список объектов MessageOutput и список уникальных идентификаторов, если результат не пустой.

        Raises:
            PermissionsError: Исключение, если в запросе используются небезопасные операторы, такие как '$where'.
        """
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
