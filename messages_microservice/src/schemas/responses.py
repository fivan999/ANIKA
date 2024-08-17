from typing import Optional, List

from pydantic import BaseModel, Field


class MessageOutput(BaseModel):
    """Модель для представления сообщения в выходных данных.

    Атрибуты:
        topic_id (int): Идентификатор темы, к которой относится сообщение.
        payload (dict): Полезная нагрузка сообщения.
        unique_id (Optional[int]): Уникальный идентификатор сообщения. По умолчанию None.
    """
    topic_id: int
    payload: dict
    unique_id: Optional[int] = None


class SearchOutput(BaseModel):
    """Модель для представления результатов поиска сообщений.

    Атрибуты:
        messages (List[MessageOutput]): Список сообщений, соответствующих критериям поиска.
        unique_ids (List[int]): Список уникальных идентификаторов сообщений, соответствующих критериям поиска.
    """
    messages: List[MessageOutput] = Field(default_factory=list)
    unique_ids: List[int] = Field(default_factory=list)


class SendOutput(BaseModel):
    """Модель для представления результатов отправки сообщений.

        Атрибуты:
            messages (List[MessageOutput]): Количество вебхуков, которые были вызваны.
        """
    webhooks_count: int