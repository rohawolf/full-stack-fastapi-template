from app.domain.ports.repositories.user import (
    UserAuthCodeRepositoryInterface,
    UserRepositoryInterface,
)
from app.domain.ports.unit_of_works.common import BaseUnitOfWorkInterface


class UserAuthCodeUnitOfWorkInterface(BaseUnitOfWorkInterface):
    user_auth_codes: UserAuthCodeRepositoryInterface

    def publish_events(self) -> None:
        while self.user_auth_codes.events:
            event = self.user_auth_codes.events.pop(0)
            event.send()


class UserUnitOfWorkInterface(BaseUnitOfWorkInterface):
    users: UserRepositoryInterface

    def publish_events(self) -> None:
        while self.users.events:
            event = self.users.events.pop(0)
            event.send()
