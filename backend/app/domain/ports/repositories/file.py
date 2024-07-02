from abc import ABC, abstractmethod
from typing import Any

from app.domain import entities as model
from app.domain.events.file import FileCreatedEvent, FileUpdatedEvent

file_event_types = FileCreatedEvent | FileUpdatedEvent


class FileRepositoryInterface(ABC):
    def __init__(self) -> None:
        self.events: list[FileCreatedEvent | FileUpdatedEvent] = []

    def add(self, file: model.File) -> None:
        self._add(file)
        self.events.append(FileCreatedEvent(file))

    def get(self, id_: str) -> model.File | None:
        file: model.File | None = self._get(id_)
        return file

    def get_by_id_for_update(self, id_: str) -> model.File | None:
        file: model.File | None = self._get(id_)
        if file:
            self.events.append(FileUpdatedEvent(file))
        return file

    def get_all(self) -> list[model.File]:
        files: list[model.File] = self._get_all()
        return files

    def search(self, query: str) -> Any | None:
        return self._search(query)

    @abstractmethod
    def _add(self, file: model.File) -> None:
        raise NotImplementedError

    @abstractmethod
    def _get(self, id_: str) -> model.File | None:
        raise NotImplementedError

    @abstractmethod
    def _get_all(self) -> list[model.File]:
        raise NotImplementedError

    @abstractmethod
    def _search(self, query: str) -> list[model.File]:
        raise NotImplementedError
