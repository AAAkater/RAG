from app.core.db import init_db
from app.core.log import logger


def main(uri: str) -> None:
    logger.info("初始化数据库")
    init_db(uri)
    logger.info("数据库初始化成功")


if __name__ == "__main__":
    main("http://127.0.0.1:19530")
