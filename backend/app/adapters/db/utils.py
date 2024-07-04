import logging
from datetime import date

from sqlalchemy import Engine
from sqlmodel import Session, create_engine, select
from tenacity import after_log, before_log, retry, stop_after_attempt, wait_fixed

from app.adapters.repositories.user import UserSqlAlchemyRepository
from app.core.common.hashing import get_password_hash
from app.core.config import get_database_uri, settings
from app.domain import entities as model
from app.domain.schemas.user import UserCreateInput

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


engine = create_engine(get_database_uri())


# make sure all SQLModel models are imported (app.models) before initializing DB
# otherwise, SQLModel might fail to initialize relationships properly
# for more details: https://github.com/tiangolo/full-stack-fastapi-template/issues/28


def init_superuser(session: Session) -> None:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next lines
    # from sqlmodel import SQLModel

    # from app.core.engine import engine
    # This works because the models are already imported and registered from app.models
    # SQLModel.metadata.create_all(engine)

    users = UserSqlAlchemyRepository(session)

    user_ = UserCreateInput(
        email=settings.FIRST_SUPERUSER,
        password=settings.FIRST_SUPERUSER_PASSWORD,
        username=settings.FIRST_SUPERUSER.split("@")[0],
        date_of_birth=date(1989, 3, 20),
        gender="male",
        phone_number="",
        resume_file_id="",
        role="admin",
    )
    user = users.get(email=user_.email)
    if not user:
        new_user = model.user_model_factory(
            email=user_.email,
            hashed_password=get_password_hash(user_.password),
            username=user_.username,
            date_of_birth=user_.date_of_birth,
            gender=user_.gender,
            phone_number=user_.phone_number,
            resume_file_id=user_.resume_file_id,
            role=user_.role,
        )
        users.add(new_user)
    session.commit()


max_tries = 60 * 5  # 5 minutes
wait_seconds = 1


@retry(
    stop=stop_after_attempt(max_tries),
    wait=wait_fixed(wait_seconds),
    before=before_log(logger, logging.INFO),
    after=after_log(logger, logging.WARN),
)
def check_db_connected(db_engine: Engine) -> None:
    try:
        with Session(db_engine) as session:
            # Try to create session to check if DB is awake
            session.exec(select(1))
    except Exception as e:
        logger.error(e)
        raise e
