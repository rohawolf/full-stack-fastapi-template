from sqlalchemy.orm import Session

from app.domain import entities as model
from app.domain.ports.repositories.file import FileRepositoryInterface


class FileSqlAlchemyRepository(FileRepositoryInterface):
    def __init__(self, session: Session) -> None:
        super().__init__()
        self.session = session

    def _add(self, file: model.File) -> None:
        self.session.add(file)

    def _get(self, id_: str) -> model.File | None:
        return self.session.query(model.File).filter_by(id=id_).first()

    def _get_all(self) -> list[model.File]:
        return self.session.query(model.File).all()

    def _search(self, query: str) -> list[model.File]:
        return (
            self.session.query(model.File)
            .filter(
                model.File.name.contains(query)  # type: ignore
            )
            .all()
        )
