import fastapi
import sqlalchemy
import sqlalchemy.ext.asyncio
import sqlalchemy.future

import src.config
import src.models
import src.schemas

logger = src.config.logger


async def get_topic_by_id(
    topic_id: int,
    db: sqlalchemy.ext.asyncio.AsyncSession,
    current_partner_id: int,
) -> src.models.Topic:
    stmt = (
        sqlalchemy.future.select(src.models.Topic)
        .filter(src.models.Topic.id == topic_id)
        .outerjoin(
            src.models.Permission,
            src.models.Permission.topic_id == src.models.Topic.id,
        )
        .where(
            sqlalchemy.or_(
                src.models.Permission.partner_id == current_partner_id,
                src.models.Topic.partner_id == current_partner_id,
            ),
        )
    )
    result = await db.execute(stmt)
    topic = result.scalars().first()

    if not topic:
        logger.error('Topic with id %s not found', topic_id)
        raise fastapi.HTTPException(status_code=404, detail='Topic not found')

    return topic


async def get_topics(
    db: sqlalchemy.ext.asyncio.AsyncSession,
    current_partner_id: int,
    partner_id: int | None = None,
    skip: int = 0,
    limit: int = 100,
):
    stmt = (
        sqlalchemy.future.select(src.models.Topic)
        .outerjoin(
            src.models.Permission,
            src.models.Permission.topic_id == src.models.Topic.id,
        )
        .where(
            sqlalchemy.or_(
                src.models.Permission.partner_id == current_partner_id,
                src.models.Topic.partner_id == current_partner_id,
            ),
        )
        .offset(skip)
        .limit(limit)
    )

    if partner_id is not None:
        stmt = stmt.filter(src.models.Topic.partner_id == partner_id)

    result = await db.execute(stmt)
    return result.scalars().all()


async def get_my_topics(
    db: sqlalchemy.ext.asyncio.AsyncSession,
    current_partner_id: int,
    skip: int = 0,
    limit: int = 100,
):
    stmt = (
        sqlalchemy.future.select(src.models.Topic)
        .filter(src.models.Topic.partner_id == current_partner_id)
        .offset(skip)
        .limit(limit)
    )
    result = await db.execute(stmt)
    return result.scalars().all()


async def create_topic(
    topic: src.schemas.TopicCreate,
    db: sqlalchemy.ext.asyncio.AsyncSession,
    current_partner_id: int,
):
    db_topic = src.models.Topic(
        **topic.model_dump(), partner_id=current_partner_id,
    )
    db.add(db_topic)
    await db.commit()
    await db.refresh(db_topic)
    logger.info(
        'Topic created with id %s by partner %s',
        db_topic.id,
        current_partner_id,
    )
    return db_topic


async def delete_topic(
    topic_id: int,
    db: sqlalchemy.ext.asyncio.AsyncSession,
    current_partner_id: int,
):
    db_topic = await get_topic_by_id(topic_id, db, current_partner_id)
    if db_topic.partner_id != current_partner_id:
        logger.error(
            'Permission denied for deleting topic with id %s by partner %s',
            topic_id,
            current_partner_id,
        )
        raise fastapi.HTTPException(
            status_code=403, detail='Permission denied',
        )

    await db.delete(db_topic)
    await db.commit()
    logger.info(
        'Topic with id %s deleted by partner %s', topic_id, current_partner_id,
    )
    return db_topic


async def edit_topic(
    topic_id: int,
    new_topic: src.schemas.TopicUpdate,
    db: sqlalchemy.ext.asyncio.AsyncSession,
    current_partner_id: int,
):
    db_topic = await get_topic_by_id(topic_id, db, current_partner_id)
    if db_topic.partner_id != current_partner_id:
        logger.error(
            'Permission denied for editing topic with id %s by partner %s',
            topic_id,
            current_partner_id,
        )
        raise fastapi.HTTPException(
            status_code=403, detail='Permission denied',
        )

    for key, value in new_topic.model_dump(exclude_unset=True).items():
        setattr(db_topic, key, value)

    await db.commit()
    await db.refresh(db_topic)
    logger.info(
        'Topic with id %s edited by partner %s', topic_id, current_partner_id,
    )
    return db_topic
