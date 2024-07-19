from dependency_injector import containers, providers
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.adapters.events.file import FileDummyCreatedEvent, FileDummyUpdatedEvent
from app.adapters.events.user import (
    UserAuthCodeCreatedEvent,
    UserAuthCodeUpdatedEvent,
    UserCreatedEvent,
    UserUpdatedEvent,
)
from app.adapters.unit_of_works.file import FileSqlAlchemyUnitOfWork
from app.adapters.unit_of_works.user import (
    UserAuthCodeSqlAlchemyUnitOfWork,
    UserSqlAlchemyUnitOfWork,
)
from app.adapters.use_cases.file import FileService
from app.adapters.use_cases.user import UserAuthCodeService, UserService
from app.core import config

ENGINE = create_engine(config.get_database_uri())


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        packages=[
            "app.adapters.entrypoints.api.v1",
        ]
    )

    DEFAULT_SESSION_FACTORY = lambda: sessionmaker(bind=ENGINE)

    file_created_event = providers.Factory(FileDummyCreatedEvent)
    file_updated_event = providers.Factory(FileDummyUpdatedEvent)
    user_created_event = providers.Factory(UserCreatedEvent)
    user_updated_event = providers.Factory(UserUpdatedEvent)
    user_auth_code_created_event = providers.Factory(UserAuthCodeCreatedEvent)
    user_auth_code_updated_event = providers.Factory(UserAuthCodeUpdatedEvent)

    file_unit_of_work = providers.Singleton(
        FileSqlAlchemyUnitOfWork,
        session_factory=DEFAULT_SESSION_FACTORY,
    )
    user_unit_of_work = providers.Singleton(
        UserSqlAlchemyUnitOfWork,
        session_factory=DEFAULT_SESSION_FACTORY,
    )
    user_auth_code_unit_of_work = providers.Singleton(
        UserAuthCodeSqlAlchemyUnitOfWork,
        session_factory=DEFAULT_SESSION_FACTORY,
    )

    file_service = providers.Factory(
        FileService,
        unit_of_work=file_unit_of_work,
        created_event=file_created_event,
        updated_event=file_updated_event,
    )
    user_service = providers.Factory(
        UserService,
        unit_of_work=user_unit_of_work,
        created_event=user_created_event,
        updated_event=user_updated_event,
    )
    user_auth_code_service = providers.Factory(
        UserAuthCodeService,
        unit_of_work=user_auth_code_unit_of_work,
        created_event=user_auth_code_created_event,
        updated_event=user_auth_code_updated_event,
    )
