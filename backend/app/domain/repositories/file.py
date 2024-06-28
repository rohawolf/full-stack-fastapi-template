from abc import ABC, abstractmethod

from app.domain.entities.file import FileEntity


class FileRepository(ABC):
    @abstractmethod
    def get_all(self) -> list[FileEntity]:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, id: str) -> FileEntity:
        raise NotImplementedError

    @abstractmethod
    def add(self, file: FileEntity) -> FileEntity:
        raise NotImplementedError

    @abstractmethod
    def update(self, file: FileEntity) -> FileEntity:
        raise NotImplementedError
