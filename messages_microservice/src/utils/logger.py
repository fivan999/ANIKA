import logging
import logging.config
import logging.handlers
import json
import uuid
from typing import Any, Optional
from aiohttp import ClientSession


class AsyncLogstashHandler(logging.Handler):
    """Асинхронный обработчик для отправки логов в Logstash.

    Args:
        host (str): Хост Logstash.
        port (int): Порт Logstash.
    """

    def __init__(self, host: str, port: int):
        super().__init__()
        self.host = host
        self.port = port

    async def emit(self, record):
        """Отправляет лог-запись в Logstash.

        Args:
            record (logging.LogRecord): Лог-запись.
        """
        log_entry = self.format(record)
        async with ClientSession() as session:
            try:
                await session.post(f'http://{self.host}:{self.port}', data=log_entry)
            except Exception as e:
                # Локальное логирование ошибки отправки
                print(f"Failed to send log to Logstash: {e}")


class AsyncLogger:
    """Класс для асинхронного логирования с поддержкой консоли, файла и Logstash.

    Args:
        log_to_console (bool): Логировать ли в консоль.
        log_to_file (bool): Логировать ли в файл.
        log_to_logstash (bool): Логировать ли в Logstash.
        file_path (Optional[str]): Путь к файлу для логов.
        logstash_host (Optional[str]): Хост Logstash.
        logstash_port (Optional[int]): Порт Logstash.
        log_level (str): Уровень логирования.
    """

    def __init__(self, log_to_console: bool, log_to_file: bool, log_to_logstash: bool,
                 file_path: Optional[str], logstash_host: Optional[str], logstash_port: Optional[int], log_level: str):
        self.log_to_logstash = log_to_logstash
        self.logstash_host: Optional[str] = logstash_host
        self.logstash_port: Optional[str] = logstash_port

        self.logger = logging.getLogger("Service logger")
        self.logger.setLevel(getattr(logging, log_level))
        self.logger.propagate = False

        if log_to_console:
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
            self.logger.addHandler(console_handler)

        if log_to_file and file_path:
            file_handler = logging.handlers.RotatingFileHandler(file_path, maxBytes=10485760, backupCount=5)
            file_handler.setFormatter(self._json_formatter())
            self.logger.addHandler(file_handler)

        if log_to_logstash and logstash_host and logstash_port:
            logstash_handler = AsyncLogstashHandler(logstash_host, logstash_port)
            logstash_handler.setFormatter(self._json_formatter())
            self.logger.addHandler(logstash_handler)

    def _json_formatter(self):
        """Создает JSON форматтер для логов.

        Returns:
            logging.Formatter: JSON форматтер.
        """

        class JsonFormatter(logging.Formatter):
            def format(self, record):
                """Форматирует лог-запись в JSON.

                Args:
                    record (logging.LogRecord): Лог-запись.

                Returns:
                    str: Форматированная лог-запись в формате JSON.
                """
                log_record = {
                    "time": self.formatTime(record, self.datefmt),
                    "level": record.levelname,
                    "message": record.getMessage(),
                    "custom_data": record.__dict__.get('custom_data', {}),
                    "trace_id": record.__dict__.get('trace_id', str(uuid.uuid4()))
                }
                return json.dumps(log_record)

        return JsonFormatter()

    async def debug(self, message: str, trace_id: Optional[str] = None, **kwargs: Any):
        """Логирует сообщение с уровнем DEBUG.

        Args:
            message (str): Логируемое сообщение.
            trace_id (Optional[str]): Идентификатор трассировки.
            **kwargs: Дополнительные параметры.
        """
        await self._log('DEBUG', message, trace_id, **kwargs)

    async def info(self, message: str, trace_id: Optional[str] = None, **kwargs: Any):
        """Логирует сообщение с уровнем INFO.

        Args:
            message (str): Логируемое сообщение.
            trace_id (Optional[str]): Идентификатор трассировки.
            **kwargs: Дополнительные параметры.
        """
        await self._log('INFO', message, trace_id, **kwargs)

    async def warning(self, message: str, trace_id: Optional[str] = None, **kwargs: Any):
        """Логирует сообщение с уровнем WARNING.

        Args:
            message (str): Логируемое сообщение.
            trace_id (Optional[str]): Идентификатор трассировки.
            **kwargs: Дополнительные параметры.
        """
        await self._log('WARNING', message, trace_id, **kwargs)

    async def error(self, message: str, trace_id: Optional[str] = None, **kwargs: Any):
        """Логирует сообщение с уровнем ERROR.

        Args:
            message (str): Логируемое сообщение.
            trace_id (Optional[str]): Идентификатор трассировки.
            **kwargs: Дополнительные параметры.
        """
        await self._log('ERROR', message, trace_id, **kwargs)

    async def critical(self, message: str, trace_id: Optional[str] = None, **kwargs: Any):
        """Логирует сообщение с уровнем CRITICAL.

        Args:
            message (str): Логируемое сообщение.
            trace_id (Optional[str]): Идентификатор трассировки.
            **kwargs: Дополнительные параметры.
        """
        await self._log('CRITICAL', message, trace_id, **kwargs)

    async def _log(self, level: str, message: str, trace_id: Optional[str], **kwargs: Any):
        """Основной метод для логирования сообщений с разными уровнями.

        Args:
            level (str): Уровень логирования.
            message (str): Логируемое сообщение.
            trace_id (Optional[str]): Идентификатор трассировки.
            **kwargs: Дополнительные параметры.
        """
        log_method = getattr(self.logger, level.lower(), None)
        extra = {'custom_data': kwargs}
        if trace_id:
            extra['trace_id'] = trace_id
        if log_method:
            log_method(message, extra=extra)

        if self.log_to_logstash and self.logstash_host and self.logstash_port:
            await self._log_to_logstash(level, message, trace_id, **kwargs)

    async def _log_to_logstash(self, level: str, message: str, trace_id: Optional[str], **kwargs: Any):
        """Отправляет лог-запись в Logstash.

        Args:
            level (str): Уровень логирования.
            message (str): Логируемое сообщение.
            trace_id (Optional[str]): Идентификатор трассировки.
            **kwargs: Дополнительные параметры.
        """
        log_entry = {
            "level": level,
            "message": message,
            "trace_id": trace_id,
            "extra": kwargs
        }
        async with ClientSession() as session:
            await session.post(f'http://{self.logstash_host}:{self.logstash_port}', data=json.dumps(log_entry))
