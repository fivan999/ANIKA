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
    token: str
    partner_id: int
    user_id: int

def get_headers(request: Request) -> HeadersInput:

    data = request.headers

    # Передача default параметров на время разработки
    token, partner_id, user_id = data.get('token', '1'), data.get('partner_id', 1), data.get('user_id', 1)

    try:
        input_header = HeadersInput(token=token, partner_id=partner_id, user_id=user_id)
    except ValueError:
        raise HeadersNotFound

    return input_header

def get_topic_service(headers: Annotated[HeadersInput, Depends(get_headers)]) -> TopicService:
    # На время разработки передаём мок-апи
    topic_service = MockedTopicService()
    return topic_service

def get_webhooks_notifier(request: Request) -> WebhooksNotifier:
    web_hooks_notifier = WebhooksNotifier()
    return web_hooks_notifier

def get_mongodb() -> MongoDBRepository:
    return MongoDBRepository(host=config.database.host,
                             port=config.database.port,
                             username=config.database.username,
                             password=config.database.password,
                             db_name=config.database.name)

def get_messages_manager(mongodb: Annotated[MongoDBRepository, Depends(get_mongodb)]) -> MessagesManager:
    return MessagesManager(repository=mongodb)

def get_search_engine(message_manager: Annotated[MessagesManager, Depends(get_messages_manager)]) -> SearchEngine:
    return SearchEngine(messages_manager=message_manager)
