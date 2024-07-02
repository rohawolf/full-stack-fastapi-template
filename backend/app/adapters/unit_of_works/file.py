from collections.abc import Callable
from typing import Any, Self

from sqlalchemy.orm import Session

from app.adapters.repositories.file import FileSqlAlchemyRepository
from app.domain.ports.unit_of_works.file import FileUnitOfWorkInterface


class FileSqlAlchemyUnitOfWork(FileUnitOfWorkInterface):
    def __init__(self, session_factory: Callable[[], Any]) -> None:
        self.session_factory = session_factory()

    def __enter__(self) -> Self:
        self.session: Session = self.session_factory()
        self.files = FileSqlAlchemyRepository(self.session)
        return super().__enter__()

    def __exit__(
        self,
        *args: list[Any],
    ) -> None:
        super().__exit__(*args)
        self.session.close()

    def _commit(self) -> None:
        self.session.commit()

    def rollback(self) -> None:
        self.session.rollback()
