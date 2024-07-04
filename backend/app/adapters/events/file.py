from app.domain import entities as model
from app.domain.ports.events.file import (
    FileCreatedEventInterface,
    FileUpdatedEventInterface,
)


class FileDummyCreatedEvent(FileCreatedEventInterface):
    def send(self, file: model.File) -> bool:
        print(f"FileDummyCreatedEvent send:{file}")
        return True


class FileDummyUpdatedEvent(FileUpdatedEventInterface):
    def send(self, file: model.File) -> bool:
        print(f"FileDummyUpdatedEvent send:{file}")
        return True
