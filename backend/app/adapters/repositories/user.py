from sqlalchemy.orm import Session

from app.domain import entities as model
from app.domain.ports.repositories.user import (
    UserAuthCodeRepositoryInterface,
    UserRepositoryInterface,
)


class UserSqlAlchemyRepository(UserRepositoryInterface):
    def __init__(
        self,
        session: Session,
    ) -> None:
        super().__init__()
        self.session = session

    def _add(self, user: model.User) -> None:
        self.session.add(user)

    def _get(self, email: str) -> model.User | None:
        return self.session.query(model.User).filter_by(email=email).first()

    def _get_all(self) -> list[model.User]:
        return self.session.query(model.User).all()

    def _search(self, query: str) -> list[model.User]:
        return (
            self.session.query(model.User)
            .filter(
                model.User.email.contains(query)  # type: ignore
            )
            .all()
        )


class UserAuthCodeSqlAlchemyRepository(UserAuthCodeRepositoryInterface):
    def __init__(
        self,
        session: Session,
    ) -> None:
        super().__init__()
        self.session = session

    def _add(self, user_auth_code: model.UserAuthCode) -> None:
        self.session.add(user_auth_code)

    def _get(self, email: str, auth_code: str) -> model.UserAuthCode | None:
        return (
            self.session.query(model.UserAuthCode)
            .filter_by(email=email, auth_code=auth_code)
            .first()
        )

    def _get_by_uuid(self, uuid: str) -> model.UserAuthCode | None:
        return self.session.query(model.UserAuthCode).filter_by(uuid=uuid).first()

    def _get_all(self) -> list[model.UserAuthCode]:
        return self.session.query(model.UserAuthCode).all()

    def _search(self, query: str) -> list[model.UserAuthCode]:
        return (
            self.session.query(model.UserAuthCode)
            .filter(
                model.UserAuthCode.email.contains(query)  # type: ignore
            )
            .all()
        )
