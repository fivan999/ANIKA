import asyncio
from typing import Optional

from aiohttp import ClientSession, BaseConnector

from src.database.models import Message


class WebhooksNotifier:
    """Сервис для отправки уведомлений через вебхуки.

    Атрибуты:
        _client_session (Optional[ClientSession]): Опциональная клиентская сессия для выполнения HTTP-запросов.
        _connector (Optional[BaseConnector]): Опциональный объект для настройки соединений (например, для настройки прокси).
    """

    def __init__(self, connector: Optional[BaseConnector] = None):
        """Инициализирует экземпляр WebhooksNotifier.

        Args:
            connector (Optional[BaseConnector], optional): Опциональный объект для настройки соединений. По умолчанию None.
        """
        self._client_session: Optional[ClientSession] = None
        self._connector = connector

    async def __aenter__(self):
        """Открывает клиентскую сессию при входе в контекстный менеджер."""
        self._client_session = ClientSession(connector=self._connector)

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Закрывает клиентскую сессию при выходе из контекстного менеджера.

        Args:
            exc_type (type): Тип исключения, если оно было выброшено.
            exc_val (BaseException): Значение исключения, если оно было выброшено.
            exc_tb (traceback): Трассировка стека, если исключение было выброшено.
        """
        await self._client_session.close()
        self._client_session = None

    async def _send(self, url: str, message: Message):
        """Отправляет сообщение на указанный URL.

        Args:
            url (str): URL, на который будет отправлено сообщение.
            message (Message): Сообщение для отправки.
        """
        response = await self._client_session.post(url=url, json=message.dict())
        print(response)

    async def notify(self, message: Message, *urls: str):
        """Отправляет уведомление на несколько URL-адресов.

        Args:
            message (Message): Сообщение для отправки.
            *urls (str): Список URL-адресов, на которые будут отправлены уведомления.
        """
        tasks = [self._send(url, message) for url in urls]
        await asyncio.gather(*tasks)
