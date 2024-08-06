from typing import Annotated

from fastapi import Depends
from pydantic import BaseModel
from starlette.requests import Request

from src.config import config
from src.database.managers import MessagesManager
from src.database.repository import MongoDBRepository
from src.schemas.exceptions import HeadersNotFound
from src.utils.search import SearchEngine
from src.utils.topics import TopicService, MockedTopicService
from src.utils.webhooks import WebhooksNotifier


class HeadersInput(BaseModel):
    """Модель данных для заголовков запроса.

    Атрибуты:
        token (str): Токен аутентификации.
        partner_id (int): Идентификатор партнера.
        user_id (int): Идентификатор пользователя.
    """
    token: str
    partner_id: int
    user_id: int


def get_headers(request: Request) -> HeadersInput:
    """Извлекает и возвращает заголовки из запроса в виде объекта HeadersInput.

    Args:
        request (Request): Объект запроса FastAPI.

    Returns:
        HeadersInput: Объект, содержащий заголовки запроса.

    Raises:
        HeadersNotFound: Если значения заголовков не могут быть преобразованы в HeadersInput.
    """
    data = request.headers

    # Передача default параметров на время разработки
    token, partner_id, user_id = data.get('token', '1'), data.get('partner_id', 1), data.get('user_id', 1)

    try:
        input_header = HeadersInput(token=token, partner_id=partner_id, user_id=user_id)
    except ValueError:
        raise HeadersNotFound

    return input_header


def get_topic_service(headers: Annotated[HeadersInput, Depends(get_headers)]) -> TopicService:
    """Создает и возвращает экземпляр TopicService.

    Аргументы:
        headers (HeadersInput): Заголовки запроса, полученные из зависимости get_headers.

    Returns:
        TopicService: Экземпляр TopicService, используется MockedTopicService на время разработки.
    """
    # На время разработки передаём мок-апи
    topic_service = MockedTopicService()
    return topic_service


def get_webhooks_notifier(request: Request) -> WebhooksNotifier:
    """Создает и возвращает экземпляр WebhooksNotifier.

    Аргументы:
        request (Request): Объект запроса FastAPI (не используется в текущей реализации).

    Returns:
        WebhooksNotifier: Экземпляр WebhooksNotifier.
    """
    web_hooks_notifier = WebhooksNotifier()
    return web_hooks_notifier


def get_mongodb() -> MongoDBRepository:
    """Создает и возвращает экземпляр MongoDBRepository.

    Returns:
        MongoDBRepository: Экземпляр MongoDBRepository с параметрами подключения из конфигурации.
    """
    return MongoDBRepository(
        host=config.database.host,
        port=config.database.port,
        username=config.database.username,
        password=config.database.password,
        db_name=config.database.name
    )


def get_messages_manager(mongodb: Annotated[MongoDBRepository, Depends(get_mongodb)]) -> MessagesManager:
    """Создает и возвращает экземпляр MessagesManager.

    Аргументы:
        mongodb (MongoDBRepository): Экземпляр MongoDBRepository, полученный из зависимости get_mongodb.

    Returns:
        MessagesManager: Экземпляр MessagesManager.
    """
    return MessagesManager(repository=mongodb)


def get_search_engine(message_manager: Annotated[MessagesManager, Depends(get_messages_manager)]) -> SearchEngine:
    """Создает и возвращает экземпляр SearchEngine.

    Аргументы:
        message_manager (MessagesManager): Экземпляр MessagesManager, полученный из зависимости get_messages_manager.

    Returns:
        SearchEngine: Экземпляр SearchEngine.
    """
    return SearchEngine(messages_manager=message_manager)
