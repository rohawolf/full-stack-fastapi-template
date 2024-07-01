from typing import Any

from app.domain.entities.file import FileEntity
from app.domain.events.file import FileCreatedEvent, FileUpdatedEvent
from app.domain.repositories.file import FileRepository
from app.domain.use_cases.file import FileUseCases


class FileService(FileUseCases):
    def __init__(
        self,
        file_repository: FileRepository,
        file_created_event: FileCreatedEvent,
        file_updated_event: FileUpdatedEvent,
    ):
        super().__init__(file_repository, file_created_event, file_updated_event)

    def file_url(self, file: FileEntity) -> str:
        path_prefix = {
            "avatar": "/images/avatar",
            "resume": "/resume",
        }[file.category]

        return "/".join(
            [
                path_prefix,
                file.url,
            ]
        )

    def get_file_list(self, **kwargs: dict[str, Any]) -> list[FileEntity]:
        files = self.file_repository.get_all(**kwargs)
        for file in files:
            file.url = self.file_url(file)
        return files

    def get_file_one(self, id: str) -> FileEntity | None:
        file = self.file_repository.get_by_id(id)
        if file is not None:
            file.url = self.file_url(file)
        return file

    def register_file(self, file: FileEntity) -> FileEntity:
        file = self.file_repository.add(file)

        self.file_created_event.send(file)

        return file

    def update_file(self, file: FileEntity) -> FileEntity:
        file = self.file_repository.update(file)

        self.file_updated_event.send(file)

        return file
