from typing import Any


class ResponseTypes:
    PARAMETERS_ERROR = "ParametersError"
    RESOURCE_ERROR = "ResourceError"
    SYSTEM_ERROR = "SystemError"
    SUCCESS = "Success"


class ResponseFailure:
    def __init__(self, type_: str, message: Exception | str) -> None:
        self.type = type_
        self.message = self._format_message(message)

    def _format_message(self, message: Exception | str) -> str:
        if isinstance(message, Exception):
            return f"{message.__class__.__name__}: {message}"
        return message

    @property
    def value(self) -> dict[str, str]:
        return {"type": self.type, "message": self.message}

    def __bool__(self) -> bool:
        return False


class ResponseSuccess:
    def __init__(self, value: Any | None = None) -> None:
        self.type = ResponseTypes.SUCCESS
        self.value = value

    def __bool__(self) -> bool:
        return True
