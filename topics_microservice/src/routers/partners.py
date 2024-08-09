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
    """
    Получить список всех партнеров.

    Возвращает список всех зарегистрированных партнеров в системе.
    Каждый партнер представлен объектом с детальной информацией, такой как ID, название, и другие атрибуты.

    Ответ:
    - Успешный запрос: возвращает список объектов Partner.
    - Пустой список, если партнеры отсутствуют.

    Пример ответа:
    ```json
    [
        {
            "id": 1,
            "name": "Партнер 1",
            "description": "Описание партнера 1"
        },
        {
            "id": 2,
            "name": "Партнер 2",
            "description": "Описание партнера 2"
        }
    ]
    ```
    """
    return await crud_partners.get_partners(db)


@partner_router.get('/{partner_id}')
async def get_partner(
    partner_id: int,
    db: AsyncSession = Depends(get_db),
    current_partner_id: int = Depends(get_current_partner_id),
) -> Partner:
    """
    Получить информацию о конкретном партнере по его ID.

    Параметры:
    - `partner_id` (int): уникальный идентификатор партнера, данные о котором необходимо получить.

    Возвращает детальную информацию о партнере, включающую его ID, название, описание и другие атрибуты.

    Ответ:
    - Успешный запрос: возвращает объект Partner с информацией о запрашиваемом партнере.
    - Если партнер с указанным ID не найден: возвращает ошибку 404.

    Пример ответа:
    ```json
    {
        "id": 1,
        "name": "Партнер 1",
        "description": "Описание партнера 1"
    }
    ```

    Пример ошибки:
    ```json
    {
        "detail": "Partner not found"
    }
    ```
    """
    return await crud_partners.get_partner_by_id(partner_id, db)
