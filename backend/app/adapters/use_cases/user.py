from pydantic_core import ValidationError

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
    UserLoginInput,
    UserOutput,
    UserUpdateInput,
)


class UserService(UserServiceInterface):
    def __init__(self, unit_of_work: UserSqlAlchemyUnitOfWork):
        self.unit_of_work = unit_of_work

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

                user_ = tx.users.get(new_user.email)
                if user_:
                    db_user_ = UserOutput.model_validate(new_user)
                    return ResponseSuccess(db_user_)
                else:
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

    def _list_users(self) -> ResponseSuccess:
        with self.unit_of_work as tx:
            users_ = tx.users.get_all()
            db_users = [UserOutput.model_validate(user_) for user_ in users_]
            return ResponseSuccess(db_users)

    def _update_user_by_email(
        self, email: str, user: UserUpdateInput
    ) -> ResponseFailure | ResponseSuccess:
        with self.unit_of_work as tx:
            existing_user = tx.users.get(email)
            if existing_user is None:
                return ResponseFailure(
                    ResponseTypes.RESOURCE_ERROR,
                    message="User not found",
                )
            if user.password:
                existing_user.hashed_password = get_password_hash(user.password)
            if user.status:
                existing_user.status = user.status
            tx.commit()
            updated_user = tx.users.get(email)
            if existing_user != updated_user:
                db_user = UserOutput.model_validate(updated_user)
                return ResponseSuccess(db_user)

            return ResponseFailure(
                ResponseTypes.RESOURCE_ERROR,
                message="Fail to update user",
            )

    def _search_user(self, query: str) -> ResponseSuccess:
        with self.unit_of_work as tx:
            results = tx.users.search(query)
            db_users = [UserOutput.model_validate(user_) for user_ in results]
            return ResponseSuccess(value=db_users)

    def _authenticate_user(self, user: UserLoginInput) -> UserOutput | bool:
        with self.unit_of_work as tx:
            user_ = tx.users.get(user.email)
            if user_ is None or not verify_password(
                user.password, user_.hashed_password
            ):
                return False
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
    def __init__(self, unit_of_work: UserAuthCodeSqlAlchemyUnitOfWork):
        self.unit_of_work = unit_of_work

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

                user_auth_code_ = tx.user_auth_codes.get(
                    new_user_auth_code.email,
                    new_user_auth_code.auth_code,
                )
                if user_auth_code_ is None:
                    return ResponseFailure(
                        ResponseTypes.RESOURCE_ERROR,
                        message="Fail to create new user auth code",
                    )
                db_user_auth_code_ = UserAuthCodeOutput.model_validate(
                    new_user_auth_code
                )
                return ResponseSuccess(db_user_auth_code_)

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
        with self.unit_of_work as tx:
            existing_user_auth_code = tx.user_auth_codes.get(email, auth_code)
            if existing_user_auth_code is None:
                return ResponseFailure(
                    ResponseTypes.RESOURCE_ERROR,
                    message="User auth code not found",
                )
            if user_auth_code.status:
                existing_user_auth_code.status = user_auth_code.status

            updated = tx.user_auth_codes.get(email, auth_code)
            if existing_user_auth_code != updated:
                db_user_auth_code_ = UserOutput.model_validate(updated)
                return ResponseSuccess(db_user_auth_code_)

            return ResponseFailure(
                ResponseTypes.RESOURCE_ERROR,
                message="Fail to update user_auth_code",
            )
