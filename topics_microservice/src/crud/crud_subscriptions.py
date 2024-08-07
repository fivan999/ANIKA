import fastapi
import sqlalchemy.ext.asyncio
import sqlalchemy.future
import sqlalchemy.orm

import src.config
import src.crud.crud_permissions
import src.models
import src.schemas

logger = src.config.logger


async def get_subscription_by_id(
    subscription_id: int,
    db: sqlalchemy.ext.asyncio.AsyncSession,
    current_partner_id: int,
) -> src.models.Subscription:
    if subscription_id <= 0:
        logger.error('Invalid subscription_id: %s', subscription_id)
        raise fastapi.HTTPException(
            status_code=400,
            detail='Invalid subscription ID',
        )

    result = await db.execute(
        sqlalchemy.future.select(src.models.Subscription)
        .filter(src.models.Subscription.id == subscription_id)
        .filter(src.models.Subscription.partner_id == current_partner_id),
    )

    subscription = result.scalars().first()
    if not subscription:
        logger.error('Subscription with id %s not found', subscription_id)
        raise fastapi.HTTPException(
            status_code=404,
            detail='Subscription not found',
        )

    return subscription


async def create_subscription(
    subscription: src.schemas.SubscriptionCreate,
    db: sqlalchemy.ext.asyncio.AsyncSession,
    current_partner_id: int,
) -> src.models.Subscription:
    await src.crud.crud_permissions.check_permission(
        subscription.topic_id,
        db,
        current_partner_id,
    )
    db_subscription = src.models.Subscription(
        **subscription.model_dump(),
        partner_id=current_partner_id,
    )
    db.add(db_subscription)
    await db.commit()
    await db.refresh(db_subscription)
    logger.info(
        'Subscription created with id %s for partner %s',
        db_subscription.id,
        current_partner_id,
    )
    return db_subscription


async def delete_subscription_by_id(
    subscription_id: int,
    db: sqlalchemy.ext.asyncio.AsyncSession,
    current_partner_id: int,
) -> src.models.Subscription:
    db_subscription = await get_subscription_by_id(
        subscription_id,
        db,
        current_partner_id,
    )
    await db.delete(db_subscription)
    await db.commit()
    logger.info(
        'Subscription with id %s deleted by partner %s',
        subscription_id,
        current_partner_id,
    )
    return db_subscription


async def get_topic_subscriptions(
    topic_id: int,
    db: sqlalchemy.ext.asyncio.AsyncSession,
    current_partner_id: int,
) -> list[src.models.Subscription]:
    if topic_id <= 0:
        logger.error('Invalid topic_id: %s', topic_id)
        raise fastapi.HTTPException(status_code=400, detail='Invalid topic ID')

    stmt = (
        sqlalchemy.future.select(src.models.Subscription)
        .join(
            src.models.Permission,
            src.models.Permission.topic_id == src.models.Subscription.topic_id,
        )
        .where(src.models.Subscription.topic_id == topic_id)
        .where(src.models.Permission.partner_id == current_partner_id)
        .options(
            sqlalchemy.orm.selectinload(src.models.Subscription.topic),
            sqlalchemy.orm.selectinload(src.models.Subscription.partner),
        )
    )

    result = await db.execute(stmt)
    return result.scalars().all()


async def get_subscription(
    subscription_id: int,
    db: sqlalchemy.ext.asyncio.AsyncSession,
    current_partner_id: int,
) -> src.models.Subscription:
    return await get_subscription_by_id(
        subscription_id,
        db,
        current_partner_id,
    )
