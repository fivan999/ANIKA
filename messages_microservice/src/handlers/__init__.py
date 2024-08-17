from fastapi import APIRouter

from .base import router as base_router
from .messages import router as messages_router

router = APIRouter(prefix='/api')
router.include_router(base_router)
router.include_router(messages_router)
