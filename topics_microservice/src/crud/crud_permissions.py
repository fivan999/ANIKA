import fastapi
import sqlalchemy.ext.asyncio
import sqlalchemy.future

import src.config
import src.crud.crud_partners
import src.crud.crud_topics
import src.main
import src.models
import src.schemas

logger = src.config.logger


async def check_permission(
    topic_id: int,
    db: sqlalchemy.ext.asyncio.AsyncSession,
    current_partner_id: int,
) -> None:
    topic = await src.crud.crud_topics.get_topic_by_id(
        topic_id,
        db,
        current_partner_id,
    )

    if not topic:
        logger.error('Topic with id %s not found', topic_id)
        raise fastapi.HTTPException(status_code=404, detail='Topic not found')

    if topic.partner_id != current_partner_id:
        logger.warning(
            'Unauthorized access attempt by partner %s to topic %s',
            current_partner_id,
            topic_id,
        )
        raise fastapi.HTTPException(
            status_code=403,
            detail='You are not authorized to access this topic',
        )


async def get_permission_by_id(
    permission_id: int,
    db: sqlalchemy.ext.asyncio.AsyncSession,
) -> src.models.Permission:
    result = await db.execute(
        sqlalchemy.future.select(src.models.Permission).filter(
            src.models.Permission.id == permission_id,
        ),
    )
    permission = result.scalars().first()

    if not permission:
        logger.error('Permission with id %s not found', permission_id)
        raise fastapi.HTTPException(
            status_code=404,
            detail='Permission not found',
        )

    return permission


async def get_permissions_by_topic_id(
    topic_id: int,
    db: sqlalchemy.ext.asyncio.AsyncSession,
) -> list[src.models.Permission]:
    result = await db.execute(
        sqlalchemy.future.select(src.models.Permission).filter(
            src.models.Permission.topic_id == topic_id,
        ),
    )
    return result.scalars().all()


async def get_permissions(
    db: sqlalchemy.ext.asyncio.AsyncSession,
    current_partner_id: int,
    skip: int = 0,
    limit: int = 100,
) -> list[src.models.Permission]:
    result = await db.execute(
        sqlalchemy.future.select(src.models.Permission)
        .filter(src.models.Permission.partner_id == current_partner_id)
        .offset(skip)
        .limit(limit),
    )
    return result.scalars().all()


async def create_permission(
    permission: src.schemas.PermissionCreate,
    db: sqlalchemy.ext.asyncio.AsyncSession,
    current_partner_id: int,
) -> src.models.Permission:
    result = await db.execute(
        sqlalchemy.future.select(src.models.Permission).filter(
            src.models.Permission.topic_id == permission.topic_id,
            src.models.Permission.partner_id == current_partner_id,
        ),
    )
    permission_ = result.scalars().first()
    if permission_:
        logger.error(
            'Permission for topic %s and partner %s already exists',
            permission.topic_id,
            current_partner_id,
        )
        raise fastapi.HTTPException(
            status_code=400,
            detail='Permission already exists',
        )
    await src.crud.crud_partners.check_partner_is_exists(
        permission.partner_id, db,
    )
    await check_permission(permission.topic_id, db, current_partner_id)
    db_permission = src.models.Permission(**permission.model_dump())
    db.add(db_permission)
    await db.commit()
    await db.refresh(db_permission)
    logger.info(
        'Permission created for topic %s by partner %s',
        permission.topic_id,
        current_partner_id,
    )
    return db_permission


async def delete_permission_by_id(
    permission_id: int,
    db: sqlalchemy.ext.asyncio.AsyncSession,
    current_partner_id: int,
) -> src.models.Permission:
    db_permission = await get_permission_by_id(permission_id, db)
    await check_permission(db_permission.topic_id, db, current_partner_id)
    await db.delete(db_permission)
    await db.commit()
    logger.info(
        'Permission with id %s deleted by partner %s',
        permission_id,
        current_partner_id,
    )
    return db_permission


async def delete_permission_by_ids(
    partner_id: int,
    topic_id: int,
    db: sqlalchemy.ext.asyncio.AsyncSession,
    current_partner_id: int,
) -> src.models.Permission:
    await check_permission(topic_id, db, current_partner_id)

    result = await db.execute(
        sqlalchemy.future.select(src.models.Permission)
        .filter(src.models.Permission.topic_id == topic_id)
        .filter(src.models.Permission.partner_id == partner_id),
    )
    db_permission = result.scalars().first()

    if db_permission:
        await db.delete(db_permission)
        await db.commit()
        logger.info(
            'Permission for partner %s and topic %s deleted by partner %s',
            partner_id,
            topic_id,
            current_partner_id,
        )
        return db_permission

    logger.error(
        'Permission with partner_id %s and topic_id %s not found',
        partner_id,
        topic_id,
    )
    raise fastapi.HTTPException(status_code=404, detail='Permission not found')


async def get_permission(
    permission_id: int,
    db: sqlalchemy.ext.asyncio.AsyncSession,
) -> src.models.Permission:
    return await get_permission_by_id(permission_id, db)
