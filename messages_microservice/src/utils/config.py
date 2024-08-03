import tomllib
from pathlib import Path
from typing import TypeVar, Generic, Type
from pydantic import BaseModel

T = TypeVar('T', bound=BaseModel)


class BaseConfig(Generic[T]):
    """Базовый класс для загрузки конфигурации из TOML файла в объект модели Pydantic.

    Attributes:
        _file_path (str | Path): Путь к файлу конфигурации.
        _model_class (Type[T]): Класс модели Pydantic.
        _data (T): Данные конфигурации, загруженные в модель Pydantic.
    """

    def __init__(self, file_path: str | Path, model_class: Type[T]):
        """Инициализирует BaseConfig с заданным путем к файлу и классом модели.

        Args:
            file_path (str | Path): Путь к файлу конфигурации.
            model_class (Type[T]): Класс модели Pydantic.
        """
        self._file_path = file_path
        self._model_class = model_class
        self._data = self._load_data()

    def _load_data(self) -> T:
        """Загружает данные из TOML файла и парсит их в объект модели Pydantic.

        Returns:
            T: Объект модели Pydantic, содержащий данные из конфигурационного файла.
        """
        with open(self._file_path, 'rb') as f:
            toml_data = tomllib.load(f)

        return self._model_class.parse_obj(toml_data)

    @property
    def file_path(self) -> str | Path:
        """Возвращает путь к файлу конфигурации.

        Returns:
            str | Path: Путь к файлу конфигурации.
        """
        return self._file_path

    @property
    def data(self) -> T:
        """Возвращает данные конфигурации, загруженные в модель Pydantic.

        Returns:
            T: Объект модели Pydantic, содержащий данные из конфигурационного файла.
        """
        return self._data
