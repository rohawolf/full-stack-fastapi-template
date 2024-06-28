from app.domain.entities.user import UserAuthCodeEntity, UserEntity
from app.domain.events.user import (
    UserAuthCodeCreatedEvent,
    UserAuthCodeUpdatedEvent,
    UserCreatedEvent,
    UserUpdatedEvent,
)


class UserCreatedQueueEvent(UserCreatedEvent):
    def send(self, user: UserEntity) -> bool:
        # TODO: Your code here
        return True


class UserUpdatedQueueEvent(UserUpdatedEvent):
    def send(self, user: UserEntity) -> bool:
        # TODO: Your code here
        return True


class UserAuthCodeCreatedQueueEvent(UserAuthCodeCreatedEvent):
    def send(self, user_auth_code: UserAuthCodeEntity) -> bool:
        # TODO: Your code here
        return True


class UserAuthCodeUpdatedQueueEvent(UserAuthCodeUpdatedEvent):
    def send(self, user_auth_code: UserAuthCodeEntity) -> bool:
        # TODO: Your code here
        return True
