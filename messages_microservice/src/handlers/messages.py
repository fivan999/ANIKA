from http.client import responses
from typing import Annotated

from aiohttp.web_response import Response
from fastapi import APIRouter
from fastapi.params import Depends

from src.database.managers import MessagesManager
from src.database.models import Message
from src.depends import get_topic_service, get_webhooks_notifier, get_messages_manager, get_search_engine
from src.schemas.bodies import SearchQuery, SendQuery, SendAllQuery
from src.schemas.exceptions import PermissionsError, TooManyNotifier, TimeOutException
from src.schemas.responses import SearchOutput, SendOutput
from src.utils.topics import TopicService
from src.utils.search import SearchEngine
from src.utils.webhooks import WebhooksNotifier

router = APIRouter(prefix="/messages", tags=["Сообщения"])

@router.post("/search", responses={403: {"description": PermissionsError.detail}, 504: {"description": TimeOutException.detail}})
async def get_messages(data: SearchQuery,
                       search_engine: Annotated[SearchEngine, Depends(get_search_engine)],
                       topic_service: Annotated[TopicService, Depends(get_topic_service)]) -> SearchOutput:
    """Получает сообщения по заданным критериям поиска.

    Args:
        data (SearchQuery): Данные запроса поиска.
        search_engine (SearchEngine): Зависимость для поискового движка.
        topic_service (TopicService): Зависимость для сервиса тем.

    Returns:
        SearchOutput: Результат поиска с найденными сообщениями и уникальными идентификаторами.

    Raises:
        PermissionsError: Исключение, если у пользователя нет разрешений на доступ к указанным темам.
    """
    async with topic_service:
        my_topics = await topic_service.get_my_topics()

        if data.topic_ids:
            for topic_id in data.topic_ids:
                if topic_id not in data.topic_ids:
                    data.remove(topic_id)

            if len(data.topic_ids) == 0:
                raise PermissionsError
        else:
            data.topic_ids = my_topics

    messages, unique_ids = await search_engine.search(topic_ids=data.topic_ids, unique_ids=data.unique_ids,
                                                      match=data.match, sort=data.sort, limit=data.limit)
    search_output = SearchOutput(messages=messages, unique_ids=unique_ids)

    return search_output

@router.post('/send_all', responses={403: {"detail": PermissionsError.detail}, 429: {"detail": TooManyNotifier.detail}})
async def send_all(data: SendAllQuery,
                   topic_service: Annotated[TopicService, Depends(get_topic_service)],
                   messages_manager: Annotated[MessagesManager, Depends(get_messages_manager)],
                   webhooks_notifier: Annotated[WebhooksNotifier, Depends(get_webhooks_notifier)]) -> SendOutput:
    """Отправляет несколько сообщений и уведомляет через вебхуки, если требуется.

    Args:
        data (SendAllQuery): Данные запроса для отправки нескольких сообщений.
        topic_service (TopicService): Зависимость для сервиса тем.
        messages_manager (MessagesManager): Зависимость для менеджера сообщений.
        webhooks_notifier (WebhooksNotifier): Зависимость для уведомителя вебхуков.

    Raises:
        TooManyNotifier: Исключение, если количество уведомлений превышает лимит.
        PermissionsError: Исключение, если у пользователя нет разрешений на доступ к указанной теме.
    """
    if len(data.payloads) > 100 and data.is_notify:
        raise TooManyNotifier

    async with topic_service:
        if not topic_service.has_permission(data.topic_id):
            raise PermissionsError

        urls = await topic_service.get_urls(topic_id=data.topic_id)

    messages = [Message(unique_id=message.unique_id,
                        topic_id=data.topic_id,
                        payload=message.payload) for message in data.payloads]

    await messages_manager.create_all_messages(messages)

    webhooks_count = 0
    if data.is_notify:
        for message in messages:
            async with webhooks_notifier:

                webhooks_count += await webhooks_notifier.notify(message, *urls)
    return SendOutput(webhooks_count=webhooks_count)
@router.post('/send', responses={403: {"description": PermissionsError.detail}})
async def send_message(data: SendQuery,
                       topic_service: Annotated[TopicService, Depends(get_topic_service)],
                       messages_manager: Annotated[MessagesManager, Depends(get_messages_manager)],
                       webhooks_notifier: Annotated[WebhooksNotifier, Depends(get_webhooks_notifier)]) -> SearchOutput:
    """Отправляет одно сообщение и уведомляет через вебхуки, если требуется.

    Args:
        data (SendQuery): Данные запроса для отправки сообщения.
        topic_service (TopicService): Зависимость для сервиса тем.
        messages_manager (MessagesManager): Зависимость для менеджера сообщений.
        webhooks_notifier (WebhooksNotifier): Зависимость для уведомителя вебхуков.

    Raises:
        PermissionsError: Исключение, если у пользователя нет разрешений на доступ к указанной теме.
    """
    async with topic_service:
        if not topic_service.has_permission(data.topic_id):
            raise PermissionsError

        urls = await topic_service.get_urls(topic_id=data.topic_id)

    message = Message(unique_id=data.unique_id,
                      topic_id=data.topic_id,
                      payload=data.payload)

    await messages_manager.create_message(message)

    webhooks_count = 0
    if data.is_notify:
        async with webhooks_notifier:
            webhooks_count = await webhooks_notifier.notify(message, *urls)
    return SearchOutput(webhooks_count=webhooks_count)
