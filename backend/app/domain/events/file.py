from app.domain import entities as model
from app.domain.events.common import Event


class FileCreatedEvent(Event):
    def __init__(self, file: model.File) -> None:
        self.file = file

    def send(self) -> bool:
        raise NotImplementedError


class FileUpdatedEvent(Event):
    def __init__(self, file: model.File) -> None:
        self.file = file

    def send(self) -> bool:
        raise NotImplementedError
