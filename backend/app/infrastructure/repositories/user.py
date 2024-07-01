from copy import copy
from datetime import UTC, datetime
from typing import Any

from app.domain.entities.user import (
    UserAuthCodeEntity,
    UserAuthCodeEntityFactory,
    UserEntity,
    UserEntityFactory,
)
from app.domain.repositories.user import UserAuthCodeRepository, UserRepository


class UserInMemoryRepository(UserRepository):
    users: list[dict[(str, Any)]] = [
        {
            "email": "user_1@gesso.com",
            "hashed_password": "user_1_password",
            "username": "gesso_user_1",
            "date_of_birth": "1990-01-01",
            "gender": "male",
            "phone_number": "01234567890",
            "resume_file_id": "file-4",
        },
        {
            "email": "user_2@gesso.com",
            "hashed_password": "user_2_password",
            "username": "gesso_user_2",
            "date_of_birth": "1990-12-31",
            "gender": "female",
            "phone_number": "01278903456",
            "resume_file_id": "file-5",
            "status": "pending",
        },
        {
            "email": "user_3@gesso.com",
            "hashed_password": "user_3_password",
            "username": "gesso_user_3",
            "date_of_birth": "2003-01-01",
            "gender": "other",
            "phone_number": "01234907856",
            "resume_file_id": "file-6",
            "status": "active",
        },
        {
            "email": "user_4@gesso.com",
            "hashed_password": "user_4_password",
            "username": "gesso_user_4",
            "date_of_birth": "1989-03-20",
            "gender": "male",
            "phone_number": "01278563490",
            "resume_file_id": "file-7",
            "status": "inactive",
        },
        {
            "email": "admin@gesso.com",
            "hashed_password": "admin_password",
            "username": "gesso_admin",
            "date_of_birth": "1989-03-20",
            "gender": "male",
            "phone_number": "01278563490",
            "resume_file_id": None,
            "role": "admin",
        },
    ]

    def get_all(self, **kwargs: dict[str, Any]) -> list[UserEntity]:
        return [UserEntityFactory.create(**user) for user in self.users]

    def get_by_email(self, email: str) -> UserEntity | None:
        try:
            user = next(filter(lambda p: p["email"] == email, self.users))
            return UserEntityFactory.create(**user)
        except StopIteration:
            return None

    def add(self, user: UserEntity) -> UserEntity:
        self.users.append(copy(user.__dict__))
        return user

    def update(self, user: UserEntity) -> UserEntity:
        for key, value in enumerate(self.users):
            if value["email"] == user.email:
                self.users[key] = copy(user.__dict__)
        return user


class UserAuthCodeInMemoryRepository(UserAuthCodeRepository):
    user_auth_codes: list[dict[(str, Any)]] = [
        {
            "id": "user_auth_code-1",
            "email": "user_5@gesso.com",
            "auth_code": "123456",
        },
        {
            "id": "user_auth_code-2",
            "email": "user_5@gesso.com",
            "auth_code": "123456",
            "status": "expired",
            "created_at": datetime(2020, 1, 1, 0, 0, 0, tzinfo=UTC),
            "updated_at": datetime(2020, 1, 1, 0, 2, 0, tzinfo=UTC),
        },
        {
            "id": "user_auth_code-2",
            "email": "user_6@gesso.com",
            "auth_code": "132435",
            "status": "authorized",
            "created_at": datetime(2020, 1, 1, 0, 0, 0, tzinfo=UTC),
            "updated_at": datetime(2020, 1, 1, 0, 1, 0, tzinfo=UTC),
        },
    ]

    def get_all(self, **kwargs: dict[str, Any]) -> list[UserAuthCodeEntity]:
        return [
            UserAuthCodeEntityFactory.create(**user_auth_code)
            for user_auth_code in self.user_auth_codes
        ]

    def get_by_email_and_auth_code(
        self, email: str, auth_code: str
    ) -> UserAuthCodeEntity | None:
        try:
            user_auth_code = next(
                filter(
                    lambda p: p["email"] == email and p["auth_code"] == auth_code,
                    self.user_auth_codes,
                )
            )
            return UserAuthCodeEntityFactory.create(**user_auth_code)
        except StopIteration:
            return None

    def add(self, user_auth_code: UserAuthCodeEntity) -> UserAuthCodeEntity:
        self.user_auth_codes.append(copy(user_auth_code.__dict__))
        return user_auth_code

    def update(self, user_auth_code: UserAuthCodeEntity) -> UserAuthCodeEntity:
        for key, value in enumerate(self.user_auth_codes):
            if value["id"] == user_auth_code.id:
                self.user_auth_codes[key] = copy(user_auth_code.__dict__)
        return user_auth_code
