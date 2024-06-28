class InvalidUserEmail(Exception):
    def __init__(self, email: str) -> None:
        self.email = email
        super().__init__(f"Invalid email: {email}")


class InvalidUserDateOfBirthFormat(Exception):
    def __init__(self, date_of_birth: str) -> None:
        self.date_of_birth = date_of_birth
        super().__init__(
            f"Invalid date of birth format: ({date_of_birth}), Use YYYY-MM-DD"
        )


class UnsupportedFileCategory(Exception):
    def __init__(self, category: str) -> None:
        self.category = category
        super().__init__(f"Unsupported file category: {category}")


class UnsupportedFileExtension(Exception):
    def __init__(self, extension: str) -> None:
        self.extension = extension
        super().__init__(f"Unsupported file extension: {extension}")
