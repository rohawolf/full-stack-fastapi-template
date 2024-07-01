from datetime import datetime

from pydantic import BaseModel

from app.domain.entities.user import (
    user_auth_code_status_type,
    user_gender_type,
    user_role_type,
    user_status_type,
)


class UserCreateInput(BaseModel):
    email: str
    password: str
    username: str
    date_of_birth: str
    gender: user_gender_type
    phone_number: str
    resume_file_id: str


class UserListInput(BaseModel):
    ...


class UserOutput(BaseModel):
    email: str
    hashed_password: str
    username: str
    date_of_birth: str
    gender: user_gender_type
    phone_number: str
    resume_file_id: str
    status: user_status_type
    role: user_role_type


class UserAuthCodeCreateInput(BaseModel):
    email: str


class UserAuthCodeOutput(BaseModel):
    id: str
    email: str
    auth_code: str
    status: user_auth_code_status_type
    expired_at: datetime
