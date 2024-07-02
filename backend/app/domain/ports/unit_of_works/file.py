from app.domain.ports.repositories.file import FileRepositoryInterface
from app.domain.ports.unit_of_works.common import BaseUnitOfWorkInterface


class FileUnitOfWorkInterface(BaseUnitOfWorkInterface):
    files: FileRepositoryInterface

    def publish_events(self) -> None:
        while self.files.events:
            event = self.files.events.pop(0)
            event.send()
