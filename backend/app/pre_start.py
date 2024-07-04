from app.adapters.db.utils import check_db_connected, engine, logger


def main() -> None:
    logger.info("Initializing service")
    check_db_connected(engine)
    logger.info("Service finished initializing")


if __name__ == "__main__":
    main()
