from typing import Annotated

from fastapi import APIRouter
from fastapi.params import Depends

from src.database.managers import MessagesManager
from src.database.models import Message
from src.depends import get_topic_service, get_webhooks_notifier, get_messages_manager, get_search_engine
from src.schemas.bodies import SearchQuery, SendQuery
from src.schemas.exceptions import PermissionsError
from src.schemas.responses import SearchOutput
from src.utils.topics import TopicService
from src.utils.search import SearchEngine
from src.utils.webhooks import WebhooksNotifier

router = APIRouter(prefix="/messages", tags=["Сообщения"])

@router.post("/search")
async def get_messages(data: SearchQuery,
                       search_engine: Annotated[SearchEngine, Depends(get_search_engine)],
                       topic_service: Annotated[TopicService, Depends(get_topic_service)]) -> SearchOutput:

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


@router.post('/send')
async def send_message(data: SendQuery,
                       topic_service: Annotated[TopicService, Depends(get_topic_service)],
                       messages_manager: Annotated[MessagesManager, Depends(get_messages_manager)],
                       webhooks_notifier: Annotated[WebhooksNotifier, Depends(get_webhooks_notifier)]):
    async with topic_service:
        if not topic_service.has_permission(data.topic_id):
            raise PermissionsError

        urls = await topic_service.get_urls(topic_id=data.topic_id)

    message = Message(unique_id = data.unique_id,
                      topic_id = data.topic_id,
                      payload = data.payload)

    await messages_manager.create_message(message)

    async with webhooks_notifier:
        await webhooks_notifier.notify(message, *urls)
