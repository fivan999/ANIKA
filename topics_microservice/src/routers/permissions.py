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
    Возвращает список всех разрешений, которые есть у текущего партнера
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
    Возвращает список всех разрешений топика
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
    Проверяет, есть ли у текущего партнера разрешение на доступ к этому топику
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
    Создает новое разрешение
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
    Удаляет разрешение по его идентификатору
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
    Удаляет разрешение, которое даёт доступ к
    топику партнёру по его идентификатору
    """
    return await crud_permissions.delete_permission_by_ids(
        partner_id=other_partner_id,
        topic_id=my_topic_id,
        db=db,
        current_partner_id=current_partner_id,
    )
