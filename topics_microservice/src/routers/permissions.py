from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.crud import crud_permissions
from src.database import get_db
from src.depends import get_current_partner_id
from src.schemas import Permission, PermissionCreate

permission_router = APIRouter(prefix='/permissions', tags=['Permissions'])


@permission_router.get('/my')
async def get_my_permissions(
    limit: int = 100,
    skip: int = 0,
    db: AsyncSession = Depends(get_db),
    current_partner_id: int = Depends(get_current_partner_id),
) -> list[Permission]:
    """
    Получить список прав доступа для текущего пользователя.

    Параметры:
    - **limit**: Максимальное количество возвращаемых прав доступа (по умолчанию 100).
    - **skip**: Количество прав доступа, которое нужно пропустить (для пагинации, по умолчанию 0).

    Возвращает:
    - Список объектов прав доступа, связанных с текущим пользователем.

    Пример использования:
    - GET `/permissions/my` — получить первые 100 прав доступа пользователя.
    """
    return await crud_permissions.get_permissions(
        limit=limit,
        skip=skip,
        db=db,
        current_partner_id=current_partner_id,
    )


@permission_router.get('/topic/{topic_id}')
async def get_permissions_by_topic_id(
    topic_id: int,
    db: AsyncSession = Depends(get_db),
    current_partner_id: int = Depends(get_current_partner_id),  # noqa: ARG001
) -> list[Permission]:
    """
    Получить список прав доступа для определённой темы.

    Параметры:
    - **topic_id**: Идентификатор темы, для которой необходимо получить права доступа.

    Возвращает:
    - Список объектов прав доступа, связанных с указанной темой.

    Пример использования:
    - GET `/permissions/topic/123` — получить все права доступа для темы с идентификатором 123.
    """
    return await crud_permissions.get_permissions_by_topic_id(
        topic_id=topic_id,
        db=db,
    )


@permission_router.get(
    '/check/{topic_id}',
    responses={
        200: {
            'description': 'You are authorized to access this topic',
        },
        403: {
            'description': 'You are not authorized to access this topic',
        },
        404: {
            'description': 'Topic not found',
        },
    },
)
async def check_permission(
    topic_id: int,
    db: AsyncSession = Depends(get_db),
    current_partner_id: int = Depends(get_current_partner_id),
) -> str:
    """
    Проверить, имеет ли текущий пользователь право доступа к указанной теме.

    Параметры:
    - **topic_id**: Идентификатор темы, доступ к которой проверяется.

    Возвращает:
    - Сообщение о наличии или отсутствии прав доступа.

    Ошибки:
    - **403**: Если пользователь не имеет права доступа к теме.
    - **404**: Если тема не найдена.

    Пример использования:
    - GET `/permissions/check/123` — проверить права доступа к теме с идентификатором 123.
    """
    await crud_permissions.check_permission(
        topic_id=topic_id,
        db=db,
        current_partner_id=current_partner_id,
    )
    return 'You are authorized to access this topic'


@permission_router.post('/create')
async def create_permission(
    permission: PermissionCreate,
    db: AsyncSession = Depends(get_db),
    current_partner_id: int = Depends(get_current_partner_id),
) -> Permission:
    """
    Создать новое право доступа для указанной темы и партнёра.

    Параметры:
    - **permission**: Данные для создания права доступа. Включает идентификатор партнёра и идентификатор темы.

    Возвращает:
    - Объект созданного права доступа.

    Пример использования:
    - POST `/permissions/create` с телом запроса:
      ```json
      {
        "partner_id": 456,
        "topic_id": 123
      }
      ```
    """
    return await crud_permissions.create_permission(
        permission=permission,
        db=db,
        current_partner_id=current_partner_id,
    )


@permission_router.delete('/{permission_id}')
async def delete_permission_by_id(
    permission_id: int,
    db: AsyncSession = Depends(get_db),
    current_partner_id: int = Depends(get_current_partner_id),
) -> Permission:
    """
    Удалить право доступа по его идентификатору.

    Параметры:
    - **permission_id**: Идентификатор права доступа, которое нужно удалить.

    Возвращает:
    - Объект удалённого права доступа.

    Пример использования:
    - DELETE `/permissions/123` — удалить право доступа с идентификатором 123.
    """
    return await crud_permissions.delete_permission_by_id(
        permission_id=permission_id,
        db=db,
        current_partner_id=current_partner_id,
    )


@permission_router.delete('/{other_partner_id}/{my_topic_id}')
async def delete_permission_by_ids(
    other_partner_id: int,
    my_topic_id: int,
    db: AsyncSession = Depends(get_db),
    current_partner_id: int = Depends(get_current_partner_id),
) -> Permission:
    """
    Удалить право доступа по идентификаторам партнёра и темы.

    Параметры:
    - **other_partner_id**: Идентификатор партнёра, для которого необходимо удалить право доступа.
    - **my_topic_id**: Идентификатор темы, для которой необходимо удалить право доступа.

    Возвращает:
    - Объект удалённого права доступа.

    Пример использования:
    - DELETE `/permissions/456/123` — удалить право доступа для партнёра 456 на тему 123.
    """
    return await crud_permissions.delete_permission_by_ids(
        partner_id=other_partner_id,
        topic_id=my_topic_id,
        db=db,
        current_partner_id=current_partner_id,
    )
