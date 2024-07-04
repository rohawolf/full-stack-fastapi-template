import abc

from app.domain.ports.common.responses import ResponseFailure, ResponseSuccess
from app.domain.ports.events import (
    UserAuthCodeCreatedEventInterface,
    UserAuthCodeUpdatedEventInterface,
    UserCreatedEventInterface,
    UserUpdatedEventInterface,
)
from app.domain.ports.unit_of_works.user import (
    UserAuthCodeUnitOfWorkInterface,
    UserUnitOfWorkInterface,
)
from app.domain.schemas.user import (
    UserAuthCodeCreateInput,
    UserAuthCodeOutput,
    UserAuthCodeUpdateInput,
    UserCreateInput,
    UserLoginInput,
    UserOutput,
    UserUpdateInput,
)


class UserServiceInterface(abc.ABC):
    @abc.abstractmethod
    def __init__(
        self,
        unit_of_work: UserUnitOfWorkInterface,
        created_event: UserCreatedEventInterface,
        updated_event: UserUpdatedEventInterface,
    ):
        self.unit_of_work = unit_of_work
        self.created_event = created_event
        self.updated_event = updated_event

    def create(self, user: UserCreateInput) -> ResponseFailure | ResponseSuccess:
        return self._create(user)

    def retrieve_user(self, email: str) -> ResponseFailure | ResponseSuccess:
        return self._retrieve_user(email)

    def list_users(self) -> ResponseSuccess:
        return self._list_users()

    def update_user_by_email(
        self, email: str, user: UserUpdateInput
    ) -> ResponseFailure | ResponseSuccess:
        return self._update_user_by_email(email, user)

    def search_user(self, query: str) -> ResponseSuccess:
        return self._search_user(query)

    def authenticate_user(self, user: UserLoginInput) -> UserOutput | None:
        return self._authenticate_user(user)

    def validate_user_create_input(
        self, user: UserCreateInput
    ) -> ResponseFailure | ResponseSuccess:
        return self._validate_user_create_input(user)

    @abc.abstractmethod
    def _create(self, user: UserCreateInput) -> ResponseFailure | ResponseSuccess:
        raise NotImplementedError

    @abc.abstractmethod
    def _retrieve_user(self, email: str) -> ResponseFailure | ResponseSuccess:
        raise NotImplementedError

    @abc.abstractmethod
    def _list_users(self) -> ResponseSuccess:
        raise NotImplementedError

    @abc.abstractmethod
    def _update_user_by_email(
        self, email: str, user: UserUpdateInput
    ) -> ResponseFailure | ResponseSuccess:
        raise NotImplementedError

    @abc.abstractmethod
    def _search_user(self, query: str) -> ResponseSuccess:
        raise NotImplementedError

    @abc.abstractmethod
    def _authenticate_user(self, user: UserLoginInput) -> UserOutput | None:
        raise NotImplementedError

    @abc.abstractmethod
    def _validate_user_create_input(
        self, user: UserCreateInput
    ) -> ResponseFailure | ResponseSuccess:
        raise NotImplementedError


class UserAuthCodeServiceInterface(abc.ABC):
    @abc.abstractmethod
    def __init__(
        self,
        unit_of_work: UserAuthCodeUnitOfWorkInterface,
        created_event: UserAuthCodeCreatedEventInterface,
        updated_event: UserAuthCodeUpdatedEventInterface,
    ):
        self.unit_of_work = unit_of_work
        self.created_event = created_event
        self.updated_event = updated_event

    def create(
        self, user_auth_code: UserAuthCodeCreateInput
    ) -> ResponseFailure | ResponseSuccess:
        return self._create(user_auth_code)

    def retrieve_user_auth_code(
        self, email: str, auth_code: str
    ) -> ResponseFailure | ResponseSuccess:
        return self._retrieve_user_auth_code(email, auth_code)

    def update_user_auth_code_by_email_and_auth_code(
        self, email: str, auth_code: str, user_auth_code: UserAuthCodeUpdateInput
    ) -> ResponseFailure | ResponseSuccess:
        return self._update_user_auth_code_by_email_and_auth_code(
            email, auth_code, user_auth_code
        )

    def validate_user_auth_code(
        self, email: str, auth_code: str
    ) -> UserAuthCodeOutput | None:
        return self._validate_user_auth_code(email, auth_code)

    @abc.abstractmethod
    def _create(
        self, user_auth_code: UserAuthCodeCreateInput
    ) -> ResponseFailure | ResponseSuccess:
        raise NotImplementedError

    @abc.abstractmethod
    def _retrieve_user_auth_code(
        self, email: str, auth_code: str
    ) -> ResponseFailure | ResponseSuccess:
        raise NotImplementedError

    @abc.abstractmethod
    def _update_user_auth_code_by_email_and_auth_code(
        self, email: str, auth_code: str, user_auth_code: UserAuthCodeUpdateInput
    ) -> ResponseFailure | ResponseSuccess:
        raise NotImplementedError

    @abc.abstractmethod
    def _validate_user_auth_code(
        self, email: str, auth_code: str
    ) -> UserAuthCodeOutput | None:
        raise NotImplementedError
