from contextlib import suppress
import uvicorn
from fastapi import FastAPI

from config import config
from handlers import router
from handlers.general import lifespan


def create_app() -> FastAPI:
    """Создает и конфигурирует экземпляр приложения FastAPI.

    Returns:
        FastAPI: Настроенный экземпляр FastAPI.
    """
    app = FastAPI(lifespan=lifespan)
    app.include_router(router=router)

    return app


def run_server():
    """Запускает сервер Uvicorn с конфигурацией из файла config."""
    with suppress(KeyboardInterrupt):
        uvicorn.run(app, host=config.server.host, port=config.server.port, workers=config.server.workers)


app = create_app()

# Основная точка входа приложения
if __name__ == '__main__':
    run_server()
