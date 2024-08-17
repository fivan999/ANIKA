from datetime import datetime
from typing import List, Dict, Any
from pymongo.errors import ExecutionTimeout
from src.database.models import Message
from src.database.repository import MongoDBRepository
from src.schemas.exceptions import TimeOutException

class MessagesManager:
    """Класс для управления сообщениями в базе данных MongoDB.

    Атрибуты:
        _repository (MongoDBRepository): Репозиторий для взаимодействия с базой данных MongoDB.
    """

    def __init__(self, repository: MongoDBRepository):
        """Инициализирует экземпляр MessagesManager с указанным репозиторием.

        Args:
            repository (MongoDBRepository): Репозиторий для взаимодействия с базой данных.
        """
        self._repository = repository

    async def create_message(self, message: Message) -> str:
        """Создает новое сообщение в коллекции 'messages'.

        Args:
            message (Message): Сообщение для добавления в базу данных.

        Returns:
            str: Идентификатор созданного сообщения.
        """
        if not message.payload.get('created_date'):
            message.payload['created_date'] = datetime.now()
            
        document = message.dict(by_alias=True)
        return await self._repository.create('messages', document)

    async def aggregate_messages(self, pipeline: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Выполняет агрегацию сообщений с использованием указанного конвейера.

        Args:
            pipeline (List[Dict[str, Any]]): Конвейер агрегации для выполнения.

        Returns:
            List[Dict[str, Any]]: Результат агрегации.

        Raises:
            TimeOutException: Исключение, если выполнение запроса превышает установленное время ожидания.
        """
        try:
            return await self._repository.aggregate('messages', pipeline)
        except ExecutionTimeout:
            raise TimeOutException

    async def create_all_messages(self, messages: List[Message]) -> List[str]:
        """Создает несколько сообщений в коллекции 'messages'.

        Args:
            messages (List[Message]): Список сообщений для добавления в базу данных.

        Returns:
            List[str]: Список идентификаторов созданных сообщений.
        """
        documents = [message.dict() for message in messages]
        return await self._repository.create_all('messages', documents)
