from abc import ABC, abstractmethod

from app.domain.entities.user import UserAuthCodeEntity, UserEntity


class UserCreatedEvent(ABC):
    @abstractmethod
    def send(self, user: UserEntity) -> bool:
        raise NotImplementedError


class UserUpdatedEvent(ABC):
    @abstractmethod
    def send(self, user: UserEntity) -> bool:
        raise NotImplementedError


class UserAuthCodeCreatedEvent(ABC):
    @abstractmethod
    def send(self, user_auth_code: UserAuthCodeEntity) -> bool:
        raise NotImplementedError


class UserAuthCodeUpdatedEvent(ABC):
    @abstractmethod
    def send(self, user_auth_code: UserAuthCodeEntity) -> bool:
        raise NotImplementedError
