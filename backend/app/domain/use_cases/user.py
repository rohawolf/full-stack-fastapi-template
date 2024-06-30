from abc import ABC, abstractmethod

from app.domain.entities.user import UserAuthCodeEntity, UserEntity
from app.domain.events.user import (
    UserAuthCodeCreatedEvent,
    UserAuthCodeUpdatedEvent,
    UserCreatedEvent,
    UserUpdatedEvent,
)
from app.domain.repositories.user import UserAuthCodeRepository, UserRepository


class UserUseCases(ABC):
    @abstractmethod
    def __init__(
        self,
        user_repository: UserRepository,
        user_created_event: UserCreatedEvent,
        user_updated_event: UserUpdatedEvent,
    ):
        self.user_repository = user_repository
        self.user_created_event = user_created_event
        self.user_updated_event = user_updated_event

    @abstractmethod
    def get_user_list(self) -> list[UserEntity]:
        raise NotImplementedError

    @abstractmethod
    def get_user_one(self, email: str) -> UserEntity | None:
        raise NotImplementedError

    @abstractmethod
    def validate_user_create_input(self, user: UserEntity) -> dict[(str, str)]:
        raise NotImplementedError

    @abstractmethod
    def register_user(self, user: UserEntity) -> UserEntity:
        raise NotImplementedError

    @abstractmethod
    def update_user(self, user: UserEntity) -> UserEntity:
        raise NotImplementedError


class UserAuthCodeUseCases(ABC):
    @abstractmethod
    def __init__(
        self,
        user_auth_code_repository: UserAuthCodeRepository,
        user_auth_code_created_event: UserAuthCodeCreatedEvent,
        user_auth_code_updated_event: UserAuthCodeUpdatedEvent,
    ):
        self.user_auth_code_repository = user_auth_code_repository
        self.user_auth_code_created_event = user_auth_code_created_event
        self.user_auth_code_updated_event = user_auth_code_updated_event

    @abstractmethod
    def get_user_auth_code_list(self) -> list[UserAuthCodeEntity]:
        raise NotImplementedError

    @abstractmethod
    def get_user_auth_code_one(self, email: str, auth_code: str) -> UserAuthCodeEntity | None:
        raise NotImplementedError

    @abstractmethod
    def register_user_auth_code(
        self,
        user_auth_code: UserAuthCodeEntity,
    ) -> UserAuthCodeEntity:
        raise NotImplementedError

    @abstractmethod
    def update_user_auth_code(
        self,
        user_auth_code: UserAuthCodeEntity,
    ) -> UserAuthCodeEntity:
        raise NotImplementedError
