import uuid
from dataclasses import asdict, dataclass, field
from datetime import UTC, date, datetime, timedelta
from random import randint
from typing import Any, Literal, Self

user_gender_type = Literal["male", "female", "other"]
user_status_type = Literal["applied", "pending", "active", "inactive"]
user_role_type = Literal["admin", "user"]
user_auth_code_status_type = Literal["pending", "authorized", "expired"]


@dataclass
class BaseUser:
    email: str
    hashed_password: str
    username: str
    date_of_birth: date
    gender: user_gender_type
    phone_number: str
    resume_file_id: str | None
    status: user_status_type = field(default="applied")
    role: user_role_type = field(default="user")


@dataclass
class User(BaseUser):
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, User):
            return False

        return self.email == other.email

    def __hash__(self) -> int:
        return hash(self.email)

    @classmethod
    def from_dict(cls, dict_: dict[str, Any]) -> Self:
        return cls(**dict_)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class BaseUserAuthCode:
    uuid: str
    email: str
    auth_code: str
    expired_at: datetime | None
    status: user_auth_code_status_type = field(default="pending")


@dataclass
class UserAuthCode(BaseUserAuthCode):
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, UserAuthCode):
            return False

        return self.email == other.email and self.auth_code == other.auth_code

    def __hash__(self) -> int:
        return hash(self.uuid)

    @classmethod
    def from_dict(cls, dict_: dict[str, Any]) -> Self:
        return cls(**dict_)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def user_model_factory(
    email: str,
    hashed_password: str,
    username: str,
    date_of_birth: date,
    gender: user_gender_type,
    phone_number: str,
    resume_file_id: str | None,
    status: user_status_type = "applied",
    role: user_role_type = "user",
) -> User:
    if role == "admin":
        status = "active"

    return User(
        email=email,
        hashed_password=hashed_password,
        username=username,
        date_of_birth=date_of_birth,
        gender=gender,
        phone_number=phone_number,
        resume_file_id=resume_file_id,
        status=status,
        role=role,
    )


def user_auth_code_model_factory(
    email: str,
    auth_code: str = "",
    expired_at: datetime | None = None,
    status: user_auth_code_status_type = "pending",
) -> UserAuthCode:
    if not auth_code:
        auth_code = str(randint(100000, 999999))

    if expired_at is None:
        expired_at = datetime.now(UTC) + timedelta(minutes=10)

    return UserAuthCode(
        uuid=f"user_auth_code-{uuid.uuid4()}",
        email=email,
        auth_code=auth_code,
        status=status,
        expired_at=expired_at,
    )
