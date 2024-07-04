import abc

from app.domain import entities as model


class FileCreatedEventInterface(abc.ABC):
    @abc.abstractmethod
    def send(self, file: model.File) -> bool:
        raise NotImplementedError


class FileUpdatedEventInterface(abc.ABC):
    @abc.abstractmethod
    def send(self, file: model.File) -> bool:
        raise NotImplementedError
