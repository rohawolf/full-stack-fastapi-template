from datetime import datetime

from pydantic import BaseModel


class FileCreateInput(BaseModel):
    category: str
    name: str
    url: str


class FileUpdateInput(BaseModel):
    ...


class FileOutput(BaseModel):
    id: str
    category: str
    name: str
    extension: str
    url: str
    is_deleted: bool
    created_at: datetime
    updated_at: datetime
