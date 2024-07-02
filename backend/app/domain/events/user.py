from app.domain import entities as model
from app.domain.events.common import Event


class UserCreatedEvent(Event):
    def __init__(self, user: model.User) -> None:
        self.user = user

    def send(self) -> bool:
        raise NotImplementedError


class UserUpdatedEvent(Event):
    def __init__(self, user: model.User) -> None:
        self.user = user

    def send(self) -> bool:
        raise NotImplementedError


class UserAuthCodeCreatedEvent(Event):
    def __init__(self, user_auth_code: model.UserAuthCode) -> None:
        self.user_auth_code = user_auth_code

    def send(self) -> bool:
        raise NotImplementedError


class UserAuthCodeUpdatedEvent(Event):
    def __init__(self, user_auth_code: model.UserAuthCode) -> None:
        self.user_auth_code = user_auth_code

    def send(self) -> bool:
        raise NotImplementedError
