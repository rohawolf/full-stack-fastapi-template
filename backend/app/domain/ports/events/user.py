import abc

from app.domain import entities as model


class UserCreatedEventInterface(abc.ABC):
    @abc.abstractmethod
    def send(self, user: model.User) -> bool:
        raise NotImplementedError


class UserUpdatedEventInterface(abc.ABC):
    @abc.abstractmethod
    def send(self, user: model.User) -> bool:
        raise NotImplementedError


class UserAuthCodeCreatedEventInterface(abc.ABC):
    @abc.abstractmethod
    def send(self, user_auth_code: model.UserAuthCode) -> bool:
        raise NotImplementedError


class UserAuthCodeUpdatedEventInterface(abc.ABC):
    @abc.abstractmethod
    def send(self, user_auth_code: model.UserAuthCode) -> bool:
        raise NotImplementedError
