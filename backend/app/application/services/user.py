from app.application.validators.user import UserValidator
from app.domain.entities.user import UserAuthCodeEntity, UserEntity
from app.domain.events.user import (
    UserAuthCodeCreatedEvent,
    UserAuthCodeUpdatedEvent,
    UserCreatedEvent,
    UserUpdatedEvent,
)
from app.domain.repositories.user import UserAuthCodeRepository, UserRepository
from app.domain.use_cases.user import UserAuthCodeUseCases, UserUseCases


class UserService(UserUseCases):
    def __init__(
        self,
        user_repository: UserRepository,
        user_created_event: UserCreatedEvent,
        user_updated_event: UserUpdatedEvent,
    ):
        super().__init__(user_repository, user_created_event, user_updated_event)

    def get_user_list(self) -> list[UserEntity]:
        users = self.user_repository.get_all()
        # TODO: some hadling user logic here
        return users

    def get_user_one(self, email: str) -> UserEntity | None:
        user = self.user_repository.get_by_email(email)
        # TODO: some hadling user logic here
        return user

    def validate_user_create_input(self, user: UserEntity) -> dict[(str, str)]:
        validates = {
            UserValidator.validate_email: user.email,
            UserValidator.validate_date_of_birth: user.date_of_birth,
        }
        error_info = {}
        for validator_, value_ in validates.items():
            try:
                validator_(value_)
            except Exception as e:
                error_info[value_] = str(e)

        return error_info

    def register_user(self, user: UserEntity) -> UserEntity:
        user = self.user_repository.add(user)

        self.user_created_event.send(user)

        return user

    def update_user(self, user: UserEntity) -> UserEntity:
        user = self.user_repository.update(user)

        self.user_updated_event.send(user)

        return user


class UserAuthCodeService(UserAuthCodeUseCases):
    def __init__(
        self,
        user_auth_code_repository: UserAuthCodeRepository,
        user_auth_code_created_event: UserAuthCodeCreatedEvent,
        user_auth_code_updated_event: UserAuthCodeUpdatedEvent,
    ):
        super().__init__(
            user_auth_code_repository,
            user_auth_code_created_event,
            user_auth_code_updated_event,
        )

    def get_user_auth_code_list(self) -> list[UserAuthCodeEntity]:
        user_auth_codes = self.user_auth_code_repository.get_all()
        return user_auth_codes

    def get_user_auth_code_one(self, email: str, auth_code: str) -> UserAuthCodeEntity | None:
        user_auth_code = self.user_auth_code_repository.get_by_email_and_auth_code(
            email, auth_code
        )
        return user_auth_code

    def register_user_auth_code(
        self,
        user_auth_code: UserAuthCodeEntity,
    ) -> UserAuthCodeEntity:
        user_auth_code = self.user_auth_code_repository.add(user_auth_code)

        self.user_auth_code_created_event.send(user_auth_code)

        return user_auth_code

    def update_user_auth_code(
        self,
        user_auth_code: UserAuthCodeEntity,
    ) -> UserAuthCodeEntity:
        user_auth_code = self.user_auth_code_repository.update(user_auth_code)

        self.user_auth_code_updated_event.send(user_auth_code)

        return user_auth_code
