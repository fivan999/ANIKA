from typing import Optional, List

from aiohttp import ClientSession, BaseConnector


class APIService:
    """Базовый класс для сервисов, взаимодействующих с внешним API.

    Атрибуты:
        _host (str): Хост API.
        _port (int): Порт API.
        _connector (Optional[BaseConnector]): Опциональный объект для настройки соединений (например, для настройки прокси).
        _token (str): Токен аутентификации для доступа к API.

    Методы:
        __aenter__: Инициализирует и открывает клиентскую сессию при входе в контекстный менеджер.
        __aexit__: Закрывает клиентскую сессию при выходе из контекстного менеджера.
        base_url: Формирует базовый URL для запросов.
        headers: Формирует заголовки для запросов.
    """

    def __init__(self, host: str, port: int, token: str, connector: Optional[BaseConnector] = None) -> None:
        """Инициализирует экземпляр APIService.

        Args:
            host (str): Хост API.
            port (int): Порт API.
            token (str): Токен аутентификации.
            connector (Optional[BaseConnector], optional): Опциональный объект для настройки соединений. По умолчанию None.
        """
        self._host = host
        self._port = port
        self._connector = connector
        self._token = token

    async def __aenter__(self):
        """Открывает клиентскую сессию при входе в контекстный менеджер."""
        self._client_session = ClientSession(connector=self._connector, headers=self.headers)

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Закрывает клиентскую сессию при выходе из контекстного менеджера.

        Args:
            exc_type (type): Тип исключения, если оно было выброшено.
            exc_val (BaseException): Значение исключения, если оно было выброшено.
            exc_tb (traceback): Трассировка стека, если исключение было выброшено.
        """
        await self._client_session.close()
        self._client_session = None

    @property
    def base_url(self):
        """Формирует базовый URL для запросов.

        Returns:
            str: Базовый URL в формате '{host}:{port}'.
        """
        return f'{self._host}:{self._port}'

    @property
    def headers(self):
        """Формирует заголовки для запросов.

        Returns:
            dict: Заголовки, включая токен аутентификации.
        """
        headers = {'Authorization': f'Token {self._token}'}
        return headers

class TopicService(APIService):
    """Сервис для работы с темами через API.

    Методы:
        has_permission: Проверяет, есть ли у пользователя разрешение на доступ к теме.
        get_my_topics: Получает список тем, доступных пользователю.
        get_urls: Получает список URL-адресов для подписки на указанную тему.
    """

    async def has_permission(self, topic_id: int) -> bool:
        """Проверяет, есть ли у пользователя разрешение на доступ к указанной теме.

        Args:
            topic_id (int): Идентификатор темы.

        Returns:
            bool: True, если разрешение есть, иначе False.
        """
        response = await self._client_session.get(f'{self.base_url}/permissions/check/{topic_id}')
        return response.status == 200

    async def get_my_topics(self) -> List[int]:
        """Получает список тем, доступных пользователю.

        Returns:
            List[int]: Список идентификаторов доступных тем.
        """
        response = await self._client_session.get(f'{self.base_url}/permissions/my')
        return await response.json()

    async def get_urls(self, topic_id: int) -> List[int]:
        """Получает список URL-адресов для подписки на указанную тему.

        Args:
            topic_id (int): Идентификатор темы.

        Returns:
            List[int]: Список URL-адресов.
        """
        response = await self._client_session.get(f'{self.base_url}/subscriptions/topic/{topic_id}')
        return await response.json()

class MockedTopicService(TopicService):
    """Мок-версия TopicService для тестирования.

    Методы:
        has_permission: Всегда возвращает True.
        get_my_topics: Возвращает фиксированный список тем.
        get_urls: Возвращает фиксированный список URL-адресов.
    """

    def __init__(self):
        """Инициализирует экземпляр MockedTopicService с фиктивными данными."""
        super().__init__(host='mock', port=0, token='mock')

    async def has_permission(self, topic_id: int) -> bool:
        """Всегда возвращает True для тестирования.

        Args:
            topic_id (int): Идентификатор темы.

        Returns:
            bool: Всегда True.
        """
        return True

    async def get_my_topics(self) -> List[int]:
        """Возвращает фиксированный список тем для тестирования.

        Returns:
            List[int]: Фиксированный список тем.
        """
        return [1, 2, 3]

    async def get_urls(self, topic_id: int) -> List[str]:
        """Возвращает фиксированный список URL-адресов для тестирования.

        Args:
            topic_id (int): Идентификатор темы.

        Returns:
            List[str]: Фиксированный список URL-адресов.
        """
        return ['http://localhost:8001/webhook']
