import motor.motor_asyncio
from typing import List, Any, Dict, Optional, Mapping

class MongoDBRepository:
    """Репозиторий для взаимодействия с базой данных MongoDB.

    Атрибуты:
        _host (str): Хост MongoDB.
        _port (int): Порт MongoDB.
        _db_name (str): Имя базы данных.
        _username (Optional[str]): Имя пользователя для подключения к MongoDB.
        _password (Optional[str]): Пароль для подключения к MongoDB.
        _client (AsyncIOMotorClient): Асинхронный клиент MongoDB.
        _db (AsyncIOMotorDatabase): База данных MongoDB.
    """

    def __init__(self, host: str, port: int, db_name: str, username: Optional[str] = None, password: Optional[str] = None):
        """Инициализирует экземпляр MongoDBRepository с указанными параметрами.

        Args:
            host (str): Хост MongoDB.
            port (int): Порт MongoDB.
            db_name (str): Имя базы данных.
            username (Optional[str], optional): Имя пользователя для подключения к MongoDB. По умолчанию None.
            password (Optional[str], optional): Пароль для подключения к MongoDB. По умолчанию None.
        """
        self._host = host
        self._port = port
        self._db_name = db_name
        self._username = username
        self._password = password
        self._client = motor.motor_asyncio.AsyncIOMotorClient(self.url)
        self._db = self._client[self._db_name]

    @property
    def url(self) -> str:
        """Формирует URL для подключения к MongoDB.

        Returns:
            str: URL для подключения к MongoDB.
        """
        if self._username and self._password:
            return f'mongodb://{self._username}:{self._password}@{self._host}:{self._port}'
        return f'mongodb://{self._host}:{self._port}'

    async def create(self, collection: str, document: Dict[str, Any]) -> str:
        """Создает документ в указанной коллекции.

        Args:
            collection (str): Название коллекции.
            document (Dict[str, Any]): Документ для добавления.

        Returns:
            str: Идентификатор созданного документа.
        """
        result = await self._db[collection].insert_one(document)
        return str(result.inserted_id)

    async def create_all(self, collection: str, documents: List[Dict[str, Any]]) -> List[str]:
        """Создает несколько документов в указанной коллекции.

        Args:
            collection (str): Название коллекции.
            documents (List[Dict[str, Any]]): Список документов для добавления.

        Returns:
            List[str]: Список идентификаторов созданных документов.
        """
        result = await self._db[collection].insert_many(documents)
        return result.inserted_ids

    async def aggregate(self, collection: str, pipeline: List[Dict[str, Any]], max_time_ms: int = None) -> List[Dict[str, Any]]:
        """Выполняет агрегацию в указанной коллекции.

        Args:
            collection (str): Название коллекции.
            pipeline (List[Dict[str, Any]]): Конвейер агрегации.
            max_time_ms (int, optional): Максимальное время выполнения в миллисекундах. По умолчанию None.

        Returns:
            List[Dict[str, Any]]: Результат агрегации.
        """
        cursor = self._db[collection].aggregate(pipeline, max_time_ms=max_time_ms)
        result = []
        async for document in cursor:
            result.append(document)
        return result

    async def find(self, collection: str, query: Dict[str, Any]) -> Optional[Mapping[str, Any]]:
        """Находит один документ в указанной коллекции по заданному запросу.

        Args:
            collection (str): Название коллекции.
            query (Dict[str, Any]): Запрос для поиска документа.

        Returns:
            Optional[Mapping[str, Any]]: Найденный документ или None, если документ не найден.
        """
        document = await self._db[collection].find_one(query)
        if document:
            return document
        return None

    async def update(self, collection: str, query: Dict[str, Any], update: Dict[str, Any]) -> int:
        """Обновляет один документ в указанной коллекции по заданному запросу.

        Args:
            collection (str): Название коллекции.
            query (Dict[str, Any]): Запрос для поиска документа.
            update (Dict[str, Any]): Обновляемые данные.

        Returns:
            int: Количество обновленных документов.
        """
        result = await self._db[collection].update_one(query, {'$set': update})
        return result.modified_count

    async def delete(self, collection: str, query: Dict[str, Any]) -> int:
        """Удаляет один документ в указанной коллекции по заданному запросу.

        Args:
            collection (str): Название коллекции.
            query (Dict[str, Any]): Запрос для поиска документа.

        Returns:
            int: Количество удаленных документов.
        """
        result = await self._db[collection].delete_one(query)
        return result.deleted_count
