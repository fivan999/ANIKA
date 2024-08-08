import fastapi
import sqlalchemy
import sqlalchemy.ext.asyncio
import sqlalchemy.future

import src.config
import src.models
import src.schemas

logger = src.config.logger


async def check_partner_is_exists(
    partner_id: int,
    db: sqlalchemy.ext.asyncio.AsyncSession,
) -> src.models.Partner:
    result = await db.execute(
        sqlalchemy.future.select(src.models.Partner).filter(
            src.models.Partner.id == partner_id,
        ),
    )
    partner = result.scalars().first()

    if not partner:
        logger.error('Partner with id %s not found', partner_id)
        raise fastapi.HTTPException(
            status_code=404,
            detail='Partner not found',
        )

    return partner
