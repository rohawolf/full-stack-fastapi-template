from app.adapters.entrypoints.api.utils import generate_new_auth_code_email, send_email
from app.domain import entities as model
from app.domain.ports.events.user import (
    UserAuthCodeCreatedEventInterface,
    UserAuthCodeUpdatedEventInterface,
    UserCreatedEventInterface,
    UserUpdatedEventInterface,
)


class UserCreatedEvent(UserCreatedEventInterface):
    def send(self, user: model.User) -> bool:
        print(f"UserCreatedEvent send: {user}")
        return True


class UserUpdatedEvent(UserUpdatedEventInterface):
    def send(self, user: model.User) -> bool:
        print(f"UserUpdatedEvent send: {user}")
        return True


class UserAuthCodeCreatedEvent(UserAuthCodeCreatedEventInterface):
    def send(self, user_auth_code: model.UserAuthCode) -> bool:
        print(f"UserAuthCodeCreatedEvent send: {user_auth_code}")

        email_data = generate_new_auth_code_email(
            email_to=user_auth_code.email,
            auth_code=user_auth_code.auth_code,
        )

        send_email(
            email_to=user_auth_code.email,
            subject=email_data.subject,
            html_content=email_data.html_content,
        )
        return True


class UserAuthCodeUpdatedEvent(UserAuthCodeUpdatedEventInterface):
    def send(self, user_auth_code: model.UserAuthCode) -> bool:
        print(f"UserAuthCodeUpdatedEvent send: {user_auth_code}")
        return True
