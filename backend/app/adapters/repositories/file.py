from sqlalchemy.orm import Session

from app.domain import entities as model
from app.domain.ports.repositories.file import FileRepositoryInterface


class FileSqlAlchemyRepository(FileRepositoryInterface):
    def __init__(
        self,
        session: Session,
    ) -> None:
        super().__init__()
        self.session = session

    def _add(self, file: model.File) -> None:
        self.session.add(file)

    def _get(self, uuid: str) -> model.File | None:
        return self.session.query(model.File).filter_by(uuid=uuid).first()

    def _get_all(
        self, category: str, extention: str, is_deleted: bool
    ) -> list[model.File]:
        qs = self.session.query(model.File)
        if category:
            qs = qs.filter_by(category=category)

        if extention:
            qs = qs.filter_by(extention=extention)

        if is_deleted:
            qs = qs.filter_by(is_deleted=is_deleted)

        return qs.all()

    def _search(self, query: str) -> list[model.File]:
        return (
            self.session.query(model.File)
            .filter(
                model.File.name.contains(query)  # type: ignore
            )
            .all()
        )
