from app.domain.ports.repositories.user import (
    UserAuthCodeRepositoryInterface,
    UserRepositoryInterface,
)
from app.domain.ports.unit_of_works.common import BaseUnitOfWorkInterface


class UserAuthCodeUnitOfWorkInterface(BaseUnitOfWorkInterface):
    user_auth_codes: UserAuthCodeRepositoryInterface


class UserUnitOfWorkInterface(BaseUnitOfWorkInterface):
    users: UserRepositoryInterface
