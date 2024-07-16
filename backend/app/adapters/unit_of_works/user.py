from collections.abc import Callable
from typing import Any, Self

from sqlalchemy.orm import Session

from app.adapters.repositories.user import (
    UserAuthCodeSqlAlchemyRepository,
    UserSqlAlchemyRepository,
)
from app.domain.ports.unit_of_works.user import (
    UserAuthCodeUnitOfWorkInterface,
    UserUnitOfWorkInterface,
)


class UserSqlAlchemyUnitOfWork(UserUnitOfWorkInterface):
    def __init__(
        self,
        session_factory: Callable[[], Any],
    ) -> None:
        self.session_factory = session_factory()

    def __enter__(self) -> Self:
        self.session: Session = self.session_factory()
        self.users = UserSqlAlchemyRepository(self.session)
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

    def refresh(self, obj: Any) -> None:
        self.session.refresh(obj)


class UserAuthCodeSqlAlchemyUnitOfWork(UserAuthCodeUnitOfWorkInterface):
    def __init__(
        self,
        session_factory: Callable[[], Any],
    ) -> None:
        self.session_factory = session_factory()

    def __enter__(self) -> Self:
        self.session: Session = self.session_factory()
        self.user_auth_codes = UserAuthCodeSqlAlchemyRepository(self.session)
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

    def refresh(self, obj: Any) -> None:
        self.session.refresh(obj)