from abc import ABC, abstractmethod

from app.domain.entities.user import UserAuthCodeEntity, UserEntity


class UserRepository(ABC):
    @abstractmethod
    def get_all(self) -> list[UserEntity]:
        raise NotImplementedError

    @abstractmethod
    def get_by_email(self, email: str) -> UserEntity:
        raise NotImplementedError

    @abstractmethod
    def add(self, user: UserEntity) -> UserEntity:
        raise NotImplementedError

    @abstractmethod
    def update(self, user: UserEntity) -> UserEntity:
        raise NotImplementedError


class UserAuthCodeRepository(ABC):
    @abstractmethod
    def get_all(self) -> list[UserAuthCodeEntity]:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, id: str) -> UserAuthCodeEntity:
        raise NotImplementedError

    @abstractmethod
    def add(self, user_auth_code: UserAuthCodeEntity) -> UserAuthCodeEntity:
        raise NotImplementedError

    @abstractmethod
    def update(self, user_auth_code: UserAuthCodeEntity) -> UserAuthCodeEntity:
        raise NotImplementedError
