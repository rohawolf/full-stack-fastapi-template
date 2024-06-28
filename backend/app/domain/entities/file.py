import uuid
from datetime import UTC, datetime

from app.domain.exceptions import UnsupportedFileCategory, UnsupportedFileExtension

available_file_categories_and_extensions = {
    "avatar": [
        "jpg",
        "jpeg",
        "gif",
        "png",
    ],
    "resume": [
        "doc",
        "docx",
        "pdf",
    ],
}


class FileEntity:
    def __init__(
        self,
        *,
        id: str,
        category: str,
        name: str,
        extensions: str,
        url: str,
        is_deleted: bool = False,
        created_at: datetime | None,
        updated_at: datetime | None,
    ):
        self.validate_category_extension_map(category, extensions)

        self.id = id
        self.category = category
        self.name = name
        self.extensions = extensions
        self.url = url

        self.is_deleted = is_deleted
        now_ = datetime.now(UTC)
        self.created_at = created_at or now_
        self.updated_at = updated_at or now_

    @staticmethod
    def validate_category_extension_map(category: str, extension: str) -> None:
        if category not in available_file_categories_and_extensions:
            raise UnsupportedFileCategory(category=category)

        if extension not in available_file_categories_and_extensions[category]:
            raise UnsupportedFileExtension(extension=extension)


class FileEntityFactory:
    @staticmethod
    def create(
        *,
        id: str | None,
        category: str,
        name: str,
        extensions: str,
        url: str,
        is_deleted: bool = False,
        created_at: datetime | None,
        updated_at: datetime | None,
    ) -> FileEntity:
        if id is None:
            id = f"file-{uuid.uuid4()}"
        return FileEntity(
            id=id,
            category=category,
            name=name,
            extensions=extensions,
            url=url,
            is_deleted=is_deleted,
            created_at=created_at,
            updated_at=updated_at,
        )
