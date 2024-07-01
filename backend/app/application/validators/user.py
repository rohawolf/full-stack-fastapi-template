from datetime import datetime

from email_validator import EmailNotValidError, validate_email

from app.domain.exceptions import (
    InvalidUserDateOfBirthFormat,
    InvalidUserEmail,
)


class UserValidator:
    @staticmethod
    def validate_email(email: str) -> str:
        try:
            email_info = validate_email(email, check_deliverability=False)
            return email_info.normalized
        except EmailNotValidError:
            raise InvalidUserEmail(email)

    @staticmethod
    def validate_date_of_birth(date_of_birth: str) -> None:
        try:
            datetime.strptime(date_of_birth, "%Y-%m-%d")
        except ValueError:
            raise InvalidUserDateOfBirthFormat(date_of_birth)
