from app.adapters.events.file import FileDummyCreatedEvent, FileDummyUpdatedEvent
from app.adapters.unit_of_works.file import FileSqlAlchemyUnitOfWork
from app.domain.entities.file import file_model_factory
from app.domain.ports.common.responses import (
    ResponseFailure,
    ResponseSuccess,
    ResponseTypes,
)
from app.domain.ports.use_cases.file import FileServiceInterface
from app.domain.schemas.file import (
    FileCreateInput,
    FileListInput,
    FileOutput,
)


class FileService(FileServiceInterface):
    def __init__(
        self,
        unit_of_work: FileSqlAlchemyUnitOfWork,
        created_event: FileDummyCreatedEvent,
        updated_event: FileDummyUpdatedEvent,
    ):
        self.unit_of_work = unit_of_work
        self.created_event = created_event
        self.updated_event = updated_event

    def _create(
        self, file: FileCreateInput, url: str
    ) -> ResponseFailure | ResponseSuccess:
        try:
            with self.unit_of_work as tx:
                new_file = file_model_factory(
                    category=file.category,
                    name=file.name,
                    url=url,
                )
                tx.files.add(new_file)
                tx.commit()
                tx.refresh(new_file)

                if new_file:
                    self.created_event.send(new_file)
                    db_file_ = FileOutput.model_validate(new_file)
                    return ResponseSuccess(db_file_)
                else:
                    return ResponseFailure(
                        ResponseTypes.RESOURCE_ERROR,
                        message="Fail to create new file",
                    )
        except Exception as exc:
            return ResponseFailure(ResponseTypes.SYSTEM_ERROR, exc)

    def _retrieve_file(self, uuid: str) -> ResponseFailure | ResponseSuccess:
        with self.unit_of_work as tx:
            file_ = tx.files.get(uuid)
            if file_ is None or file_.is_deleted:
                return ResponseFailure(
                    ResponseTypes.RESOURCE_ERROR,
                    message="File not found",
                )

            db_file_ = FileOutput.model_validate(file_)
            return ResponseSuccess(db_file_)

    def _list_files(self, files: FileListInput) -> ResponseSuccess:
        with self.unit_of_work as tx:
            files_ = tx.files.get_all(files.category, files.extension, files.is_deleted)
            db_files = [FileOutput.model_validate(file_) for file_ in files_]
            return ResponseSuccess(db_files)

    def _delete_file_by_id(self, uuid: str) -> ResponseFailure | ResponseSuccess:
        with self.unit_of_work as tx:
            existing_file = tx.files.get(uuid)
            if existing_file is None:
                return ResponseFailure(
                    ResponseTypes.RESOURCE_ERROR,
                    message="File not found",
                )
            existing_file.is_deleted = True
            tx.commit()
            self.updated_event.send(existing_file)
            return ResponseSuccess(
                value={"detail": "successfully set file.is_deleted=True"},
            )

    def _search_file(self, query: str) -> ResponseSuccess:
        with self.unit_of_work as tx:
            results = tx.files.search(query)
            db_files = [FileOutput.model_validate(file_) for file_ in results]
            return ResponseSuccess(value=db_files)
