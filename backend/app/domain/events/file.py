from abc import ABC, abstractmethod

from app.domain.entities.file import FileEntity


class FileCreatedEvent(ABC):
    @abstractmethod
    def send(self, file: FileEntity) -> bool:
        raise NotImplementedError


class FileUpdatedEvent(ABC):
    @abstractmethod
    def send(self, file: FileEntity) -> bool:
        raise NotImplementedError
