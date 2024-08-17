from typing import Dict
from fastapi import APIRouter

# Создание роутера с префиксом '/base'
router = APIRouter(prefix='/base', tags=['Основное'])


@router.get('/ping')
async def pong() -> Dict[str, str]:
    """Обработчик GET-запросов на маршрут '/ping'.

    Этот обработчик возвращает простое сообщение для проверки доступности сервера.

    Returns:
        Dict[str, str]: Ответ в формате JSON с результатом 'pong'.
    """
    return {'result': 'pong'}
