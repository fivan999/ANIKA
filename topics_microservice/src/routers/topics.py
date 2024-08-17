from fastapi import APIRouter, HTTPException
from fastapi.param_functions import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src import schemas
from src.crud import crud_topics
from src.database import get_db
from src.depends import get_current_partner_id

topic_router = APIRouter(prefix='/topics', tags=['Topics'])


@topic_router.get('')
async def get_topics(
    partner_id: int | None = None,
    limit: int = 100,
    skip: int = 0,
    db: AsyncSession = Depends(get_db),
    current_partner_id: int = Depends(get_current_partner_id),
) -> list[schemas.Topic]:
    """
    Получить список всех доступных тем.

    Параметры:
    - **partner_id**: (необязательно) Фильтр по идентификатору партнера. Если указан, вернет только темы, связанные с этим партнером.
    - **limit**: (по умолчанию: 100) Ограничение на количество возвращаемых записей.
    - **skip**: (по умолчанию: 0) Количество записей, которые нужно пропустить в результате.

    Возвращает:
    - Список объектов тем.

    Пример использования:
    - GET `/topics?limit=50&skip=10` — получить 50 тем, начиная с 10-й.
    """
    return await crud_topics.get_topics(
        db=db,
        current_partner_id=current_partner_id,
        partner_id=partner_id,
        limit=limit,
        skip=skip,
    )


@topic_router.get('/my')
async def get_my_topics(
    limit: int = 100,
    skip: int = 0,
    db: AsyncSession = Depends(get_db),
    current_partner_id: int = Depends(get_current_partner_id),
) -> list[schemas.Topic]:
    """
    Получить список тем, созданных текущим пользователем (партнером).

    Параметры:
    - **limit**: (по умолчанию: 100) Ограничение на количество возвращаемых записей.
    - **skip**: (по умолчанию: 0) Количество записей, которые нужно пропустить в результате.

    Возвращает:
    - Список объектов тем, созданных текущим пользователем.

    Пример использования:
    - GET `/topics/my?limit=50&skip=10` — получить 50 собственных тем, начиная с 10-й.
    """
    return await crud_topics.get_my_topics(
        db=db,
        current_partner_id=current_partner_id,
        limit=limit,
        skip=skip,
    )


@topic_router.get(
    '/{topic_id}',
    responses={404: {'description': 'Topic not found'}},
)
async def get_topic(
    topic_id: int,
    db: AsyncSession = Depends(get_db),
    current_partner_id: int = Depends(get_current_partner_id),
) -> schemas.Topic:
    """
    Получить информацию о конкретной теме по её идентификатору.

    Параметры:
    - **topic_id**: Идентификатор темы, которую необходимо получить.

    Возвращает:
    - Объект темы.

    Ошибки:
    - **404**: Тема с указанным идентификатором не найдена.

    Пример использования:
    - GET `/topics/123` — получить тему с идентификатором 123.
    """
    topic = await crud_topics.get_topic_by_id(
        topic_id=topic_id,
        db=db,
        current_partner_id=current_partner_id,
    )
    if not topic:
        raise HTTPException(status_code=404, detail='Topic not found')
    return topic


@topic_router.post('/create')
async def create_topic(
    topic: schemas.TopicCreate,
    db: AsyncSession = Depends(get_db),
    current_partner_id: int = Depends(get_current_partner_id),
) -> schemas.Topic:
    """
    Создать новую тему.

    Параметры:
    - **topic**: Данные для создания новой темы. Включает такие поля, как название и описание.

    Возвращает:
    - Объект созданной темы.

    Пример использования:
    - POST `/topics/create` с телом запроса:
      ```json
      {
        "title": "Новая тема",
        "description": "Описание новой темы"
      }
      ```
    """
    return await crud_topics.create_topic(
        topic=topic,
        db=db,
        current_partner_id=current_partner_id,
    )


@topic_router.patch('/{topic_id}')
async def edit_topic(
    topic_id: int,
    new_topic: schemas.TopicUpdate,
    db: AsyncSession = Depends(get_db),
    current_partner_id: int = Depends(get_current_partner_id),
) -> schemas.Topic:
    """
    Обновить информацию о существующей теме.

    Параметры:
    - **topic_id**: Идентификатор темы, которую нужно обновить.
    - **new_topic**: Новые данные для обновления темы.

    Возвращает:
    - Обновленный объект темы.

    Ошибки:
    - **404**: Тема с указанным идентификатором не найдена.

    Пример использования:
    - PATCH `/topics/123` с телом запроса:
      ```json
      {
        "title": "Обновленное название"
      }
      ```
    """
    updated_topic = await crud_topics.edit_topic(
        topic_id=topic_id,
        new_topic=new_topic,
        db=db,
        current_partner_id=current_partner_id,
    )
    if not updated_topic:
        raise HTTPException(status_code=404, detail='Topic not found')
    return updated_topic


@topic_router.delete(
    '/{topic_id}',
    responses={403: {'description': 'Permission denied'}},
)
async def delete_topic(
    topic_id: int,
    db: AsyncSession = Depends(get_db),
    current_partner_id: int = Depends(get_current_partner_id),
) -> schemas.Topic:
    """
    Удалить тему по её идентификатору.

    Параметры:
    - **topic_id**: Идентификатор темы, которую нужно удалить.

    Возвращает:
    - Объект удаленной темы.

    Ошибки:
    - **404**: Тема с указанным идентификатором не найдена.
    - **403**: Отказано в доступе на удаление темы (если пользователь не является владельцем).

    Пример использования:
    - DELETE `/topics/123` — удалить тему с идентификатором 123.
    """
    deleted_topic = await crud_topics.delete_topic(
        topic_id=topic_id,
        db=db,
        current_partner_id=current_partner_id,
    )
    if not deleted_topic:
        raise HTTPException(status_code=404, detail='Topic not found')
    return deleted_topic
