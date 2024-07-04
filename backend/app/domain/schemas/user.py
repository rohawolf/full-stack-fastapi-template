from datetime import date, datetime

from pydantic import BaseModel, EmailStr

from app.domain.entities.user import (
    user_auth_code_status_type,
    user_gender_type,
    user_role_type,
    user_status_type,
)


class UserCreateInput(BaseModel):
    email: EmailStr
    password: str
    username: str
    date_of_birth: date
    gender: user_gender_type
    phone_number: str
    resume_file_id: str | None
    role: user_role_type = "user"

    class Config:
        from_attributes = True


class UserLoginInput(BaseModel):
    email: EmailStr
    password: str


class UserUpdateInput(BaseModel):
    password: str
    status: user_status_type


class UserOutput(BaseModel):
    email: EmailStr
    username: str
    date_of_birth: date
    gender: user_gender_type
    phone_number: str
    resume_file_id: str
    status: user_status_type
    role: user_role_type

    class Config:
        from_attributes = True


class UserAuthCodeCreateInput(BaseModel):
    email: EmailStr

    class Config:
        from_attributes = True


class UserAuthCodeUpdateInput(BaseModel):
    status: user_auth_code_status_type


class UserAuthCodeOutput(BaseModel):
    uuid: str
    email: EmailStr
    auth_code: str
    status: user_auth_code_status_type
    expired_at: datetime

    class Config:
        from_attributes = True
