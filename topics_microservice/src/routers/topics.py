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
    Возвращает список всех топиков, к которым у партнера есть доступ
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
    Возвращает список всех топиков, к которым у партнера есть доступ
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
    Возвращает информацию о топике
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
    Создает новый топик
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
    Изменяет информацию о топике
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
    Удаляет топик
    """
    deleted_topic = await crud_topics.delete_topic(
        topic_id=topic_id,
        db=db,
        current_partner_id=current_partner_id,
    )
    if not deleted_topic:
        raise HTTPException(status_code=404, detail='Topic not found')
    return deleted_topic
