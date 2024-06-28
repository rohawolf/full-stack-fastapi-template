from datetime import UTC, datetime, timedelta
from random import randint
from typing import Literal

from email_validator import EmailNotValidError, validate_email

from app.domain.exceptions import InvalidUserDateOfBirthFormat, InvalidUserEmail

user_gender_type = Literal["male", "female", "other"]
user_status_type = Literal["applied", "pending", "active", "inactive"]
user_role_type = Literal["admin", "user"]
user_auth_code_status_type = Literal["pending", "expired"]


class UserEntity:
    def __init__(
        self,
        *,
        email: str,
        hashed_password: str,
        username: str,
        date_of_birth: str,
        gender: user_gender_type,
        phone_number: str,
        resume_url: str,
        status: user_status_type = "applied",
        role: user_role_type = "user",
        created_at: datetime | None,
        updated_at: datetime | None,
    ):
        email_ = self.validate_email(email)
        date_of_birth_ = self.validate_date_of_birth(date_of_birth)

        self.email = email_
        self.hashed_password = hashed_password
        self.username = username
        self.date_of_birth = date_of_birth_
        self.gender = gender
        self.phone_number = phone_number
        self.resume_url = resume_url
        self.status = status
        self.role = role

        now_ = datetime.now(UTC)
        self.created_at = created_at or now_
        self.updated_at = updated_at or now_

    @staticmethod
    def validate_email(email: str) -> str:
        try:
            email_info = validate_email(email, check_deliverability=False)
            return email_info.normalized
        except EmailNotValidError:
            raise InvalidUserEmail(email)

    @staticmethod
    def validate_date_of_birth(date_of_birth: str) -> str:
        try:
            datetime.strptime(date_of_birth, "%Y-%m-%d")
            return date_of_birth
        except ValueError:
            raise InvalidUserDateOfBirthFormat(date_of_birth)


class UserEntityFactory:
    @staticmethod
    def create(
        *,
        email: str,
        hashed_password: str,
        username: str,
        date_of_birth: str,
        gender: user_gender_type,
        phone_number: str,
        resume_url: str,
        status: user_status_type = "applied",
        role: user_role_type = "user",
        created_at: datetime | None,
        updated_at: datetime | None,
    ) -> UserEntity:
        if role == "admin":
            status = "active"

        return UserEntity(
            email=email,
            hashed_password=hashed_password,
            username=username,
            date_of_birth=date_of_birth,
            gender=gender,
            phone_number=phone_number,
            resume_url=resume_url,
            status=status,
            role=role,
            created_at=created_at,
            updated_at=updated_at,
        )


class UserAuthCodeEntity:
    def __init__(
        self,
        *,
        email: str,
        auth_code: str | None,
        status: user_auth_code_status_type = "pending",
        created_at: datetime | None,
        updated_at: datetime | None,
        expired_at: datetime | None,
    ):
        self.email = email
        self.auth_code = auth_code or str(randint(100000, 999999))
        self.status = status

        now_ = datetime.now(UTC)
        self.created_at = created_at or now_
        self.updated_at = updated_at or now_
        self.expired_at = expired_at or now_ + timedelta(minutes=2)


class UserAuthCodeEntityFactory:
    @staticmethod
    def create(
        *,
        email: str,
        auth_code: str | None,
        status: user_auth_code_status_type = "pending",
        created_at: datetime | None,
        updated_at: datetime | None,
        expired_at: datetime | None,
    ) -> UserAuthCodeEntity:
        return UserAuthCodeEntity(
            email=email,
            auth_code=auth_code,
            status=status,
            created_at=created_at,
            updated_at=updated_at,
            expired_at=expired_at,
        )
