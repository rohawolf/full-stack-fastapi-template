import uuid
from datetime import UTC, datetime, timedelta
from random import randint
from typing import Literal

user_gender_type = Literal["male", "female", "other"]
user_status_type = Literal["applied", "pending", "active", "inactive"]
user_role_type = Literal["admin", "user"]
user_auth_code_status_type = Literal["pending", "authorized", "expired"]


class UserEntity:
    def __init__(
        self,
        *,
        email: str,
        password: str,
        username: str,
        date_of_birth: str,
        gender: user_gender_type,
        phone_number: str,
        resume_file_id: str | None,
        status: user_status_type = "applied",
        role: user_role_type = "user",
    ):
        self.email = email
        self.password = password
        self.username = username
        self.date_of_birth = date_of_birth
        self.gender = gender
        self.phone_number = phone_number
        self.resume_file_id = resume_file_id
        self.status = status
        self.role = role


class UserEntityFactory:
    @staticmethod
    def create(
        *,
        email: str,
        password: str,
        username: str,
        date_of_birth: str,
        gender: user_gender_type,
        phone_number: str,
        resume_file_id: str | None,
        status: user_status_type = "applied",
        role: user_role_type = "user",
    ) -> UserEntity:
        if role == "admin":
            status = "active"

        return UserEntity(
            email=email,
            password=password,
            username=username,
            date_of_birth=date_of_birth,
            gender=gender,
            phone_number=phone_number,
            resume_file_id=resume_file_id,
            status=status,
            role=role,
        )


class UserAuthCodeEntity:
    def __init__(
        self,
        *,
        id: str,
        email: str,
        auth_code: str | None,
        status: user_auth_code_status_type = "pending",
        expired_at: datetime | None,
    ):
        self.id = id
        self.email = email
        self.auth_code = auth_code or str(randint(100000, 999999))
        self.status = status
        self.expired_at = expired_at or datetime.now(UTC) + timedelta(minutes=2)


class UserAuthCodeEntityFactory:
    @staticmethod
    def create(
        *,
        id: str | None,
        email: str,
        auth_code: str | None,
        status: user_auth_code_status_type = "pending",
        expired_at: datetime | None,
    ) -> UserAuthCodeEntity:
        if id is None:
            id = f"user_auth_code-{uuid.uuid4()}"
        return UserAuthCodeEntity(
            id=id,
            email=email,
            auth_code=auth_code,
            status=status,
            expired_at=expired_at,
        )
