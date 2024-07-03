from dependency_injector import containers, providers
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.adapters.unit_of_works.file import FileSqlAlchemyUnitOfWork
from app.adapters.unit_of_works.user import (
    UserAuthCodeSqlAlchemyUnitOfWork,
    UserSqlAlchemyUnitOfWork,
)
from app.adapters.use_cases.file import FileService
from app.adapters.use_cases.user import UserAuthCodeService, UserService
from app.core import config

ENGINE = create_engine(
    config.get_database_uri(), connect_args={"check_same_thread": False}
)


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        packages=[
            "app.adapters.entrypoints.api.v1",
        ]
    )

    @staticmethod
    def DEFAULT_SESSION_FACTORY() -> sessionmaker[Session]:
        return sessionmaker(bind=ENGINE)

    file_unit_of_work = providers.Singleton(
        FileSqlAlchemyUnitOfWork, session_factory=DEFAULT_SESSION_FACTORY
    )
    user_unit_of_work = providers.Singleton(
        UserSqlAlchemyUnitOfWork, session_factory=DEFAULT_SESSION_FACTORY
    )
    user_auth_code_unit_of_work = providers.Singleton(
        UserAuthCodeSqlAlchemyUnitOfWork, session_factory=DEFAULT_SESSION_FACTORY
    )

    file_service = providers.Factory(
        FileService,
        unit_of_work=file_unit_of_work,
    )
    user_service = providers.Factory(
        UserService,
        unit_of_work=user_unit_of_work,
    )
    user_auth_code_service = providers.Factory(
        UserAuthCodeService,
        unit_of_work=user_auth_code_unit_of_work,
    )
