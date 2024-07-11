from abc import ABC, abstractmethod

from app.domain import entities as model


class UserRepositoryInterface(ABC):
    def add(self, user: model.User) -> None:
        self._add(user)

    def get(self, email: str) -> model.User | None:
        user = self._get(email)
        return user

    def get_all(self, status: str, role: str) -> list[model.User]:
        users = self._get_all(status, role)
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
    def _get_all(self, status: str, role: str) -> list[model.User]:
        raise NotImplementedError

    @abstractmethod
    def _search(self, query: str) -> list[model.User]:
        raise NotImplementedError


class UserAuthCodeRepositoryInterface(ABC):
    def add(self, user_auth_code: model.UserAuthCode) -> None:
        self._add(user_auth_code)

    def get(self, email: str, auth_code: str) -> model.UserAuthCode | None:
        user_auth_code = self._get(email, auth_code)
        return user_auth_code

    def get_by_uuid(self, uuid: str) -> model.UserAuthCode | None:
        user_auth_code = self._get_by_uuid(uuid)
        return user_auth_code

    def search(self, query: str) -> list[model.UserAuthCode]:
        return self._search(query)

    @abstractmethod
    def _add(self, user_auth_code: model.UserAuthCode) -> None:
        raise NotImplementedError

    @abstractmethod
    def _get(self, email: str, auth_code: str) -> model.UserAuthCode | None:
        raise NotImplementedError

    @abstractmethod
    def _get_by_uuid(self, uuid: str) -> model.UserAuthCode | None:
        raise NotImplementedError

    @abstractmethod
    def _search(self, query: str) -> list[model.UserAuthCode]:
        raise NotImplementedError
