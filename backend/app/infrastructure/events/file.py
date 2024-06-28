from app.domain.entities.file import FileEntity
from app.domain.events.file import FileCreatedEvent, FileUpdatedEvent


class FileCreatedQueueEvent(FileCreatedEvent):
    def send(self, file: FileEntity) -> bool:
        # TODO: Your code here
        return True


class FileUpdatedQueueEvent(FileUpdatedEvent):
    def send(self, file: FileEntity) -> bool:
        # TODO: Your code here
        return True
