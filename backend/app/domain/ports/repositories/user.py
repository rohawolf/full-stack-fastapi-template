from abc import ABC, abstractmethod

from app.domain import entities as model
from app.domain.events.user import (
    UserAuthCodeCreatedEvent,
    UserAuthCodeUpdatedEvent,
    UserCreatedEvent,
    UserUpdatedEvent,
)

user_event_types = UserCreatedEvent | UserUpdatedEvent
user_auth_code_event_types = UserAuthCodeCreatedEvent | UserAuthCodeUpdatedEvent


class UserRepositoryInterface(ABC):
    def __init__(self) -> None:
        self.events: list[UserCreatedEvent | UserUpdatedEvent] = []

    def add(self, user: model.User) -> None:
        self._add(user)
        self.events.append(UserCreatedEvent(user))

    def get(self, email: str) -> model.User | None:
        user = self._get(email)
        return user

    def get_by_email_for_update(self, email: str) -> model.User | None:
        user = self._get(email)
        if user:
            self.events.append(UserUpdatedEvent(user))
        return user

    def get_all(self) -> list[model.User]:
        users = self._get_all()
        return users

    def search(self, query: str) -> list[model.User]:
        return self._search(query)

    @abstractmethod
    def _add(self, user: model.User) -> None:
        raise NotImplementedError

    @abstractmethod
    def _get(self, email: str) -> model.User | None:
        raise NotImplementedError

    @abstractmethod
    def _get_all(self) -> list[model.User]:
        raise NotImplementedError

    @abstractmethod
    def _search(self, query: str) -> list[model.User]:
        raise NotImplementedError


class UserAuthCodeRepositoryInterface(ABC):
    def __init__(self) -> None:
        self.events: list[UserAuthCodeCreatedEvent | UserAuthCodeUpdatedEvent] = []

    def add(self, user_auth_code: model.UserAuthCode) -> None:
        self._add(user_auth_code)
        self.events.append(UserAuthCodeCreatedEvent(user_auth_code))

    def get(self, email: str, auth_code: str) -> model.UserAuthCode | None:
        user_auth_code = self._get(email, auth_code)
        return user_auth_code

    def get_by_id(self, id_: str) -> model.UserAuthCode | None:
        user_auth_code = self._get_by_id(id_)
        return user_auth_code

    def get_by_email_and_auth_code_for_update(
        self, email: str, auth_code: str
    ) -> model.UserAuthCode | None:
        user_auth_code = self._get(email, auth_code)
        if user_auth_code:
            self.events.append(UserAuthCodeUpdatedEvent(user_auth_code))
        return user_auth_code

    def get_all(self) -> list[model.UserAuthCode]:
        user_auth_codes = self._get_all()
        return user_auth_codes

    def search(self, query: str) -> list[model.UserAuthCode]:
        return self._search(query)

    @abstractmethod
    def _add(self, user_auth_code: model.UserAuthCode) -> None:
        raise NotImplementedError

    @abstractmethod
    def _get(self, email: str, auth_code: str) -> model.UserAuthCode | None:
        raise NotImplementedError

    @abstractmethod
    def _get_by_id(self, id_: str) -> model.UserAuthCode | None:
        raise NotImplementedError

    @abstractmethod
    def _get_all(self) -> list[model.UserAuthCode]:
        raise NotImplementedError

    @abstractmethod
    def _search(self, query: str) -> list[model.UserAuthCode]:
        raise NotImplementedError
