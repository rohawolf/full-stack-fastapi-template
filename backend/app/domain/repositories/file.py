from abc import ABC, abstractmethod
from typing import Any

from app.domain.entities.file import FileEntity


class FileRepository(ABC):
    @abstractmethod
    def get_all(self, **kwargs: dict[str, Any]) -> list[FileEntity]:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, id: str) -> FileEntity | None:
        raise NotImplementedError

    @abstractmethod
    def add(self, file: FileEntity) -> FileEntity:
        raise NotImplementedError

    @abstractmethod
    def update(self, file: FileEntity) -> FileEntity:
        raise NotImplementedError
