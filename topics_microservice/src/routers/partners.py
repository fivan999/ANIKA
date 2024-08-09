from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.crud import crud_partners
from src.database import get_db
from src.depends import get_current_partner_id
from src.schemas import Partner

partner_router = APIRouter(prefix='/partners', tags=['Partners'])


@partner_router.get('/')
async def get_partners(
    db: AsyncSession = Depends(get_db),
    current_partner_id: int = Depends(get_current_partner_id),
) -> list[Partner]:
    return await crud_partners.get_partners(db)


@partner_router.get('/{partner_id}')
async def get_partner(
    partner_id: int,
    db: AsyncSession = Depends(get_db),
    current_partner_id: int = Depends(get_current_partner_id),
) -> Partner:
    return await crud_partners.get_partner_by_id(partner_id, db)
