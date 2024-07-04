from sqlmodel import Session

from app.adapters.db.utils import engine, init_superuser, logger


def init() -> None:
    with Session(engine) as session:
        init_superuser(session)


def main() -> None:
    logger.info("Creating initial data")
    init()
    logger.info("Initial data created")


if __name__ == "__main__":
    main()
