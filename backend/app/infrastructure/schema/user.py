from pydantic import BaseModel

from app.domain.entities.user import (
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


class UserOutput(BaseModel):
    email: str
    password: str
    username: str
    date_of_birth: str
    gender: user_gender_type
    phone_number: str
    resume_file_id: str
    status: user_status_type
    role: user_role_type
