import asyncio
from typing import Optional

from aiohttp import ClientSession, BaseConnector

from src.database.models import Message


class WebhooksNotifier:
    def __init__(self, connector: Optional[BaseConnector] = None):
        self._client_session: Optional[ClientSession] = None
        self._connector = connector

    async def __aenter__(self):
        self._client_session = ClientSession(connector=self._connector)


    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._client_session.close()
        self._client_session = None

    async def _send(self, url: str, message: Message):
        response = await self._client_session.post(url=url, json=message.dict())
        print(response)
    async def notify(self, message: Message, *urls: str):
        tasks = [self._send(url, message) for url in urls]
        await asyncio.gather(*tasks)
