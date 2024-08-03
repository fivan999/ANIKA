from typing import Optional, List

from aiohttp import ClientSession, BaseConnector


class APIService:
    def __init__(self, host: str, port: int, token: str, connector: Optional[BaseConnector] = None) -> None:
        self._host = host
        self._port = port
        self._connector = connector
        self._token = token

    async def __aenter__(self):
        self._client_session = ClientSession(connector=self._connector, headers=self.headers)

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._client_session.close()
        self._client_session = None

    @property
    def base_url(self):
        return f'{self._host}:{self._port}'

    @property
    def headers(self):
        headers = {'Authorization': f'Token {self._token}'}
        return headers

class TopicService(APIService):
    async def has_permission(self, topic_id: int) -> bool:
            response = await self._client_session.get(f'{self.base_url}/permissions/check/{topic_id}')
            return response.status == 200

    async def get_my_topics(self) -> List[int]:
        response = await self._client_session.get(f'{self.base_url}/permissions/my')
        return await response.json()

    async def get_urls(self, topic_id: int) -> List[int]:
        response = await self._client_session.get(f'{self.base_url}/subscriptions/topic/{topic_id}')
        return await response.json()

class MockedTopicService(TopicService):
    def __init__(self):
        super().__init__(host='mock', port=0, token='mock')
    async def has_permission(self, topic_id: int) -> bool:
        return True

    async def get_my_topics(self) -> List[int]:
        return [1, 2, 3]

    async def get_urls(self, topic_id: int) -> list[str]:
        return []
    