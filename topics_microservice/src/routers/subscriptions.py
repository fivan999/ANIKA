from fastapi import APIRouter, HTTPException
from fastapi.param_functions import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src import schemas
from src.crud import crud_subscriptions
from src.database import get_db
from src.depends import get_current_partner_id

subscription_router = APIRouter(
    prefix='/subscriptions', tags=['Subscriptions'],
)


@subscription_router.post('/create')
async def create_subscription(
    subscription: schemas.SubscriptionCreate,
    db: AsyncSession = Depends(get_db),
    current_partner_id: int = Depends(get_current_partner_id),
) -> schemas.Subscription:
    """
    Создает новую подписку
    """
    return await crud_subscriptions.create_subscription(
        subscription=subscription,
        db=db,
        current_partner_id=current_partner_id,
    )


@subscription_router.get('/{subscription_id}')
async def get_subscription(
    subscription_id: int,
    db: AsyncSession = Depends(get_db),
    current_partner_id: int = Depends(get_current_partner_id),
) -> schemas.Subscription:
    """
    Возвращает подписку по ID
    """
    subscription = await crud_subscriptions.get_subscription(
        subscription_id=subscription_id,
        db=db,
        current_partner_id=current_partner_id,
    )

    if not subscription:
        raise HTTPException(status_code=404, detail='Subscription not found')

    return subscription


@subscription_router.get('/topic/{topic_id}')
async def get_topic_subscriptions(
    topic_id: int,
    db: AsyncSession = Depends(get_db),
    current_partner_id: int = Depends(get_current_partner_id),
) -> list[schemas.Subscription]:
    """
    Возвращает список подписок на топик
    """
    return await crud_subscriptions.get_topic_subscriptions(
        topic_id=topic_id,
        db=db,
        current_partner_id=current_partner_id,
    )


@subscription_router.delete('/delete/{subscription_id}')
async def delete_subscription(
    subscription_id: int,
    db: AsyncSession = Depends(get_db),
    current_partner_id: int = Depends(get_current_partner_id),
) -> schemas.Subscription:
    """
    Удаляет подписку
    """
    deleted_subscription = await crud_subscriptions.delete_subscription_by_id(
        subscription_id=subscription_id,
        db=db,
        current_partner_id=current_partner_id,
    )

    if not deleted_subscription:
        raise HTTPException(status_code=404, detail='Subscription not found')

    return deleted_subscription
