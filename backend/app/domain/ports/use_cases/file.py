import abc

from app.domain.ports.common.responses import ResponseFailure, ResponseSuccess
from app.domain.ports.unit_of_works.file import FileUnitOfWorkInterface
from app.domain.schemas.file import FileCreateInput, FileUpdateInput


class FileServiceInterface(abc.ABC):
    @abc.abstractmethod
    def __init__(self, unit_of_work: FileUnitOfWorkInterface):
        self.unit_of_work = unit_of_work

    def create(self, file: FileCreateInput) -> ResponseFailure | ResponseSuccess:
        return self._create(file)

    def retrieve_file(self, id_: str) -> ResponseFailure | ResponseSuccess:
        return self._retrieve_file(id_)

    def list_files(self) -> ResponseSuccess:
        return self._list_files()

    def update_file_by_id(
        self, id_: str, file: FileUpdateInput
    ) -> ResponseFailure | ResponseSuccess:
        return self._update_file_by_id(id_, file)

    def delete_file_by_id(self, id_: str) -> ResponseFailure | ResponseSuccess:
        return self._delete_file_by_id(id_)

    def search_file(self, query: str) -> ResponseSuccess:
        return self._search_file(query)

    @abc.abstractmethod
    def _create(self, file: FileCreateInput) -> ResponseFailure | ResponseSuccess:
        raise NotImplementedError

    @abc.abstractmethod
    def _retrieve_file(self, id_: str) -> ResponseFailure | ResponseSuccess:
        raise NotImplementedError

    @abc.abstractmethod
    def _list_files(self) -> ResponseSuccess:
        raise NotImplementedError

    @abc.abstractmethod
    def _update_file_by_id(
        self, id_: str, file: FileUpdateInput
    ) -> ResponseFailure | ResponseSuccess:
        raise NotImplementedError

    @abc.abstractmethod
    def _delete_file_by_id(self, id_: str) -> ResponseFailure | ResponseSuccess:
        raise NotImplementedError

    @abc.abstractmethod
    def _search_file(self, query: str) -> ResponseSuccess:
        raise NotImplementedError
