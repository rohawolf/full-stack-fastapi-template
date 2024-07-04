from abc import ABC, abstractmethod

from app.domain import entities as model


class FileRepositoryInterface(ABC):
    def add(self, file: model.File) -> None:
        self._add(file)

    def get(self, uuid: str) -> model.File | None:
        file: model.File | None = self._get(uuid)
        return file

    def get_all(self) -> list[model.File]:
        files: list[model.File] = self._get_all()
        return files

    def search(self, query: str) -> list[model.File]:
        return self._search(query)

    @abstractmethod
    def _add(self, file: model.File) -> None:
        raise NotImplementedError

    @abstractmethod
    def _get(self, uuid: str) -> model.File | None:
        raise NotImplementedError

    @abstractmethod
    def _get_all(self) -> list[model.File]:
        raise NotImplementedError

    @abstractmethod
    def _search(self, query: str) -> list[model.File]:
        raise NotImplementedError
