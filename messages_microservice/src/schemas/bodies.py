from typing import Any, Optional, List

from fastapi import Body
from pydantic import BaseModel


class SearchQuery(BaseModel):
    """Модель для запроса поиска сообщений.

    Атрибуты:
        limit (Optional[int]): Максимальное количество результатов.
        topic_ids (Optional[List[int]]): Список идентификаторов тем для поиска.
        unique_ids (Optional[List[int]]): Список уникальных идентификаторов сообщений для поиска.
        match (Optional[dict]): Критерии для сопоставления.
        sort (Optional[dict]): Параметры сортировки.
    """
    limit: Optional[int] = None
    topic_ids: Optional[List[int]] = None
    unique_ids: Optional[List[int]] = None
    match: Optional[dict] = None
    sort: Optional[dict] = None

class SendQuery(BaseModel):
    """Модель для запроса отправки одного сообщения.

    Атрибуты:
        topic_id (int): Идентификатор темы.
        unique_id (Optional[int]): Уникальный идентификатор сообщения.
        payload (Any): Содержимое сообщения.
        is_notify (Optional[bool]): Флаг, указывающий, нужно ли отправлять уведомление.
    """
    topic_id: int
    unique_id: Optional[int] = None
    payload: Any = Body(None)
    is_notify: Optional[bool] = None

class Payload(BaseModel):
    """Модель для описания полезной нагрузки сообщения.

    Атрибуты:
        payload (dict): Содержимое сообщения.
        unique_id (Optional[int]): Уникальный идентификатор сообщения.
    """
    payload: dict
    unique_id: Optional[int] = None

class SendAllQuery(BaseModel):
    """Модель для запроса отправки нескольких сообщений.

    Атрибуты:
        topic_id (int): Идентификатор темы.
        payloads (List[Payload]): Список полезных нагрузок сообщений.
        is_notify (Optional[bool]): Флаг, указывающий, нужно ли отправлять уведомления.
    """
    topic_id: int
    payloads: List[Payload]
    is_notify: Optional[bool] = None
