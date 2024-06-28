from copy import copy
from typing import Any

from app.domain.entities.file import FileEntity, FileEntityFactory
from app.domain.repositories.file import FileRepository


class FileInMemoryRepository(FileRepository):
    files: list[dict[(str, Any)]] = [
        {
            "id": "file-1",
            "category": "avatar",
            "name": "user_1.jpg",
            "extensions": "jpg",
            "url": "/images/avatar/user_1.jpg",
        },
        {
            "id": "file-2",
            "category": "avatar",
            "name": "user_2.png",
            "extensions": "png",
            "url": "/images/avatar/user_2.png",
            "is_deleted": True,
        },
        {
            "id": "file-3",
            "category": "avatar",
            "name": "user_3.gif",
            "extensions": "gif",
            "url": "/images/avatar/user_3.gif",
        },
        {
            "id": "file-4",
            "category": "resume",
            "name": "resume_user_1.doc",
            "extensions": "doc",
            "url": "/resume/resume_user_1.doc",
        },
        {
            "id": "file-5",
            "category": "resume",
            "name": "resume_user_2.docx",
            "extensions": "docx",
            "url": "/resume/resume_user_2.docx",
        },
        {
            "id": "file-6",
            "category": "resume",
            "name": "resume_user_3.pdf",
            "extensions": "pdf",
            "url": "/resume/resume_user_3.pdf",
        },
        {
            "id": "file-7",
            "category": "resume",
            "name": "resume_user_4.pdf",
            "extensions": "pdf",
            "url": "/resume/resume_user_4.pdf",
        },
    ]

    def get_all(self) -> list[FileEntity]:
        return [FileEntityFactory.create(**file) for file in self.files]

    def get_by_id(self, id: str) -> FileEntity | None:
        try:
            file = next(filter(lambda p: p["id"] == id, self.files))
            return FileEntityFactory.create(**file)
        except StopIteration:
            return None

    def add(self, file: FileEntity) -> FileEntity:
        self.files.append(copy(file.__dict__))
        return file

    def update(self, file: FileEntity) -> FileEntity:
        for key, value in enumerate(self.files):
            if value["id"] == file.id:
                self.files[key] = copy(file.__dict__)
        return file
