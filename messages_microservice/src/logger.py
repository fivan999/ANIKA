from config import config
from utils.logger import AsyncLogger


def initialize_logger() -> AsyncLogger:
    """Инициализирует асинхронный логгер с конфигурацией из файла настроек.

    Использует параметры конфигурации для создания экземпляра асинхронного логгера.

    Returns:
        AsyncLogger: Экземпляр асинхронного логгера, настроенный согласно конфигурации.
    """
    return AsyncLogger(**config.logger.dict())


# Инициализация логгера
logger = initialize_logger()
