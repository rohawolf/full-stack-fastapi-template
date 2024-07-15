from datetime import UTC, datetime

from pydantic_core import ValidationError

from app.adapters.events.user import (
    UserAuthCodeCreatedEvent,
    UserAuthCodeUpdatedEvent,
    UserCreatedEvent,
    UserUpdatedEvent,
)
from app.adapters.unit_of_works.user import (
    UserAuthCodeSqlAlchemyUnitOfWork,
    UserSqlAlchemyUnitOfWork,
)
from app.core.common.hashing import get_password_hash, verify_password
from app.domain.entities.user import user_auth_code_model_factory, user_model_factory
from app.domain.ports.common.responses import (
    ResponseFailure,
    ResponseSuccess,
    ResponseTypes,
)
from app.domain.ports.use_cases.user import (
    UserAuthCodeServiceInterface,
    UserServiceInterface,
)
from app.domain.schemas.user import (
    UserAuthCodeCreateInput,
    UserAuthCodeOutput,
    UserAuthCodeUpdateInput,
    UserCreateInput,
    UserListInput,
    UserLoginInput,
    UserOutput,
    UserUpdateInput,
)


class UserService(UserServiceInterface):
    def __init__(
        self,
        unit_of_work: UserSqlAlchemyUnitOfWork,
        created_event: UserCreatedEvent,
        updated_event: UserUpdatedEvent,
    ):
        self.unit_of_work = unit_of_work
        self.created_event = created_event
        self.updated_event = updated_event

    def _create(
        self,
        user: UserCreateInput,
    ) -> ResponseFailure | ResponseSuccess:
        try:
            with self.unit_of_work as tx:
                new_user = user_model_factory(
                    email=user.email,
                    hashed_password=get_password_hash(user.password),
                    username=user.username,
                    date_of_birth=user.date_of_birth,
                    gender=user.gender,
                    phone_number=user.phone_number,
                    resume_file_id=user.resume_file_id,
                    role=user.role,
                )
                tx.users.add(new_user)
                tx.commit()
                tx.refresh(new_user)

                if new_user:
                    self.created_event.send(new_user)
                    db_user_ = UserOutput.model_validate(new_user)
                    return ResponseSuccess(db_user_)

                return ResponseFailure(
                    ResponseTypes.RESOURCE_ERROR,
                    message="Fail to create new user",
                )
        except Exception as exc:
            return ResponseFailure(ResponseTypes.SYSTEM_ERROR, exc)

    def _retrieve_user(self, email: str) -> ResponseFailure | ResponseSuccess:
        with self.unit_of_work as tx:
            user_ = tx.users.get(email)
            if user_:
                db_user_ = UserOutput.model_validate(user_)
                return ResponseSuccess(db_user_)
            else:
                return ResponseFailure(
                    ResponseTypes.RESOURCE_ERROR,
                    message="User not found",
                )

    def _list_users(self, users: UserListInput) -> ResponseSuccess:
        with self.unit_of_work as tx:
            users_ = tx.users.get_all(status=users.status, role=users.role)
            db_users = []
            for user_ in users_:
                db_users.append(UserOutput.model_validate(user_))
            return ResponseSuccess(db_users)

    def _update_user_by_email(
        self, email: str, user: UserUpdateInput
    ) -> ResponseFailure | ResponseSuccess:
        try:
            with self.unit_of_work as tx:
                user_to_be_updated = tx.users.get(email)
                if user_to_be_updated is None:
                    return ResponseFailure(
                        ResponseTypes.RESOURCE_ERROR,
                        message="User not found",
                    )
                if user.password:
                    user_to_be_updated.hashed_password = get_password_hash(
                        user.password
                    )
                if user.status:
                    user_to_be_updated.status = user.status
                tx.commit()
                tx.refresh(user_to_be_updated)

                self.updated_event.send(user_to_be_updated)
                db_user = UserOutput.model_validate(user_to_be_updated)
                return ResponseSuccess(db_user)

        except Exception as exc:
            return ResponseFailure(ResponseTypes.SYSTEM_ERROR, exc)

    def _search_user(self, query: str) -> ResponseSuccess:
        with self.unit_of_work as tx:
            results = tx.users.search(query)
            db_users = [UserOutput.model_validate(user_) for user_ in results]
            return ResponseSuccess(value=db_users)

    def _authenticate_user(self, user: UserLoginInput) -> UserOutput | None:
        with self.unit_of_work as tx:
            user_ = tx.users.get(user.email)
            if user_ is None or not verify_password(
                user.password, user_.hashed_password
            ):
                return None
            return UserOutput.model_validate(user_)

    def _validate_user_create_input(
        self, user: UserCreateInput
    ) -> ResponseFailure | ResponseSuccess:
        try:
            UserCreateInput.model_validate(user)
            return ResponseSuccess(
                value={"detail": "successfully validate user create input"},
            )
        except ValidationError as ve:
            return ResponseFailure(
                ResponseTypes.PARAMETERS_ERROR,
                message=ve.json(),
            )


class UserAuthCodeService(UserAuthCodeServiceInterface):
    def __init__(
        self,
        unit_of_work: UserAuthCodeSqlAlchemyUnitOfWork,
        created_event: UserAuthCodeCreatedEvent,
        updated_event: UserAuthCodeUpdatedEvent,
    ):
        self.unit_of_work = unit_of_work
        self.created_event = created_event
        self.updated_event = updated_event

    def _create(
        self,
        user_auth_code: UserAuthCodeCreateInput,
    ) -> ResponseFailure | ResponseSuccess:
        try:
            with self.unit_of_work as tx:
                new_user_auth_code = user_auth_code_model_factory(
                    email=user_auth_code.email,
                )
                tx.user_auth_codes.add(new_user_auth_code)
                tx.commit()
                tx.refresh(new_user_auth_code)

                if new_user_auth_code:
                    self.created_event.send(new_user_auth_code)
                    db_user_auth_code_ = UserAuthCodeOutput.model_validate(
                        new_user_auth_code
                    )
                    return ResponseSuccess(db_user_auth_code_)
                return ResponseFailure(
                    ResponseTypes.RESOURCE_ERROR,
                    message="Fail to create new user auth code",
                )

        except Exception as exc:
            return ResponseFailure(ResponseTypes.SYSTEM_ERROR, exc)

    def _retrieve_user_auth_code(
        self, email: str, auth_code: str
    ) -> ResponseFailure | ResponseSuccess:
        with self.unit_of_work as tx:
            user_auth_code_ = tx.user_auth_codes.get(email, auth_code)
            if user_auth_code_ is None:
                return ResponseFailure(
                    ResponseTypes.RESOURCE_ERROR,
                    message="user_auth_code not found",
                )

            db_user_auth_code_ = UserAuthCodeOutput.model_validate(user_auth_code_)
            return ResponseSuccess(db_user_auth_code_)

    def _update_user_auth_code_by_email_and_auth_code(
        self, email: str, auth_code: str, user_auth_code: UserAuthCodeUpdateInput
    ) -> ResponseFailure | ResponseSuccess:
        try:
            with self.unit_of_work as tx:
                user_auth_code_to_be_updated = tx.user_auth_codes.get(email, auth_code)
                if user_auth_code_to_be_updated is None:
                    return ResponseFailure(
                        ResponseTypes.RESOURCE_ERROR,
                        message="User auth code not found",
                    )
                if user_auth_code.status:
                    user_auth_code_to_be_updated.status = user_auth_code.status

                tx.commit()
                tx.refresh(user_auth_code_to_be_updated)

                db_user_auth_code_ = UserAuthCodeOutput.model_validate(
                    user_auth_code_to_be_updated
                )
                return ResponseSuccess(db_user_auth_code_)

        except Exception as exc:
            return ResponseFailure(ResponseTypes.SYSTEM_ERROR, exc)

    def _validate_user_auth_code(
        self, email: str, auth_code: str
    ) -> UserAuthCodeOutput | None:
        with self.unit_of_work as tx:
            user_auth_code_ = tx.user_auth_codes.get(email, auth_code)
            if user_auth_code_ is None:
                return None

            expired_at: datetime | None = user_auth_code_.expired_at
            if expired_at is not None and datetime.now(UTC) >= expired_at.astimezone(
                UTC
            ):
                return None

            return UserAuthCodeOutput.model_validate(user_auth_code_)
