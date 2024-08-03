from pydantic import BaseModel
from typing import Optional
from utils.config import BaseConfig


class LoggerConfig(BaseModel):
    """Конфигурация для логирования.

    Attributes:
        log_to_console (bool): Логировать в консоль.
        log_to_file (bool): Логировать в файл.
        log_to_logstash (bool): Логировать в Logstash.
        file_path (Optional[str]): Путь к файлу логов.
        logstash_host (Optional[str]): Хост Logstash.
        logstash_port (Optional[int]): Порт Logstash.
        log_level (str): Уровень логирования.
    """
    log_to_console: bool
    log_to_file: bool
    log_to_logstash: bool
    file_path: Optional[str]
    logstash_host: Optional[str]
    logstash_port: Optional[int]
    log_level: str


class Server(BaseModel):
    """Конфигурация сервера.

    Attributes:
        host (str): Хост сервера.
        port (int): Порт сервера.
        workers (int): Количество рабочих процессов.
    """
    host: str
    port: int
    workers: int


class Database(BaseModel):
    """Конфигурация базы данных.

    Attributes:
        host (str): Хост базы данных.
        port (int): Порт базы данных.
        username (str): Имя пользователя базы данных.
        password (str): Пароль базы данных.
        name (str): Имя базы данных.
    """
    host: str
    port: int
    username: Optional[str] = None
    password: Optional[str] = None
    name: str


class ServiceConfig(BaseModel):
    """Главная конфигурация сервиса.

    Attributes:
        server (Server): Конфигурация сервера.
        database (Database): Конфигурация базы данных.
        logger (LoggerConfig): Конфигурация логирования.
    """
    server: Server
    database: Database
    logger: LoggerConfig


def get_config_path() -> str:
    """Возвращает путь к файлу конфигурации.

    Returns:
        str: Путь к файлу конфигурации.

    """

    return 'settings.toml'


# Путь к файлу конфигурации
config_path = get_config_path()

# Загрузка конфигурации из файла
config = BaseConfig[ServiceConfig](file_path=config_path, model_class=ServiceConfig).data
