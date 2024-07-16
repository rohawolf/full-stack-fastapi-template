from app.adapters.db.utils import init_superuser, logger


def main() -> None:
    logger.info("Creating initial data")
    init_superuser()
    logger.info("Initial data created")


if __name__ == "__main__":
    main()
