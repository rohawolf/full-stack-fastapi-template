from pydantic import BaseModel


class FileCreateInput(BaseModel):
    category: str
    name: str
    url: str


class FileUpdateInput(BaseModel):
    ...


class FileOutput(BaseModel):
    uuid: str
    category: str
    name: str
    extension: str
    url: str
    is_deleted: bool
