from pydantic import BaseModel


class FileCreateInput(BaseModel):
    category: str
    name: str
    url: str


class FileListInput(BaseModel):
    category: str
    extension: str
    is_deleted: bool


class FileOutput(BaseModel):
    uuid: str
    category: str
    name: str
    extension: str
    url: str
    is_deleted: bool

    class Config:
        from_attributes = True
