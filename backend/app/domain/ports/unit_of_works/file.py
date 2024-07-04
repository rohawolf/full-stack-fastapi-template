from app.domain.ports.repositories.file import FileRepositoryInterface
from app.domain.ports.unit_of_works.common import BaseUnitOfWorkInterface


class FileUnitOfWorkInterface(BaseUnitOfWorkInterface):
    files: FileRepositoryInterface
