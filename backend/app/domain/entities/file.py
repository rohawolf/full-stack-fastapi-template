import uuid
from dataclasses import asdict, dataclass, field
from typing import Any, Self

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


@dataclass
class BaseFile:
    uuid: str
    category: str
    name: str
    extension: str
    url: str
    is_deleted: bool = field(default=False)


@dataclass
class File(BaseFile):
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, File):
            return False

        return self.uuid == other.uuid

    def __hash__(self) -> int:
        return hash(self.uuid)

    @classmethod
    def from_dict(cls, dict_: dict[str, Any]) -> Self:
        return cls(**dict_)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def file_model_factory(
    category: str,
    name: str,
    url: str,
    extension: str | None = None,
    is_deleted: bool = False,
) -> File:
    if extension is None:
        extension = name.split(".")[-1]

    return File(
        uuid=f"file-{uuid.uuid4()}",
        category=category,
        name=name,
        url=url,
        extension=extension,
        is_deleted=is_deleted,
    )
