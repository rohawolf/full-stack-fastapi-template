from app.domain import entities as model
from app.domain.ports.events.user import (
    UserAuthCodeCreatedEventInterface,
    UserAuthCodeUpdatedEventInterface,
    UserCreatedEventInterface,
    UserUpdatedEventInterface,
)


class UserDummyCreatedEvent(UserCreatedEventInterface):
    def send(self, user: model.User) -> bool:
        print(f"UserDummyCreatedEvent send: {user}")
        return True


class UserDummyUpdatedEvent(UserUpdatedEventInterface):
    def send(self, user: model.User) -> bool:
        print(f"UserDummyUpdatedEvent send: {user}")
        return True


class UserAuthCodeDummyCreatedEvent(UserAuthCodeCreatedEventInterface):
    def send(self, user_auth_code: model.UserAuthCode) -> bool:
        print(f"UserAuthCodeDummyCreatedEvent send: {user_auth_code}")
        return True


class UserAuthCodeDummyUpdatedEvent(UserAuthCodeUpdatedEventInterface):
    def send(self, user_auth_code: model.UserAuthCode) -> bool:
        print(f"UserAuthCodeDummyUpdatedEvent send: {user_auth_code}")
        return True
