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
    Создать новую подписку на тему.

    Параметры:
    - **subscription**: Данные для создания подписки. Включает идентификатор темы, на которую оформляется подписка.

    Возвращает:
    - Объект созданной подписки.

    Пример использования:
    - POST `/subscriptions/create` с телом запроса:
      ```json
      {
        "topic_id": 123
      }
      ```
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
    Получить информацию о подписке по её идентификатору.

    Параметры:
    - **subscription_id**: Идентификатор подписки, которую необходимо получить.

    Возвращает:
    - Объект подписки.

    Ошибки:
    - **404**: Подписка с указанным идентификатором не найдена.

    Пример использования:
    - GET `/subscriptions/123` — получить подписку с идентификатором 123.
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
    Получить список подписок на указанную тему для текущего пользователя.

    Параметры:
    - **topic_id**: Идентификатор темы, на которую оформлены подписки.

    Возвращает:
    - Список объектов подписок для данной темы.

    Пример использования:
    - GET `/subscriptions/topic/456` — получить все подписки на тему с идентификатором 456.
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
    Удалить подписку по её идентификатору.

    Параметры:
    - **subscription_id**: Идентификатор подписки, которую нужно удалить.

    Возвращает:
    - Объект удаленной подписки.

    Ошибки:
    - **404**: Подписка с указанным идентификатором не найдена.

    Пример использования:
    - DELETE `/subscriptions/delete/123` — удалить подписку с идентификатором 123.
    """
    deleted_subscription = await crud_subscriptions.delete_subscription_by_id(
        subscription_id=subscription_id,
        db=db,
        current_partner_id=current_partner_id,
    )

    if not deleted_subscription:
        raise HTTPException(status_code=404, detail='Subscription not found')

    return deleted_subscription
