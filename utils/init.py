import sys

from nonebot.log import logger
from configs.config import INFO_LOG_TIME, DEBUG_LOG_TIME, ERROR_LOG_TIME, WARNING_LOG_TIME
from configs.path_config import LOG_PATH
from utils.db import db


async def init_bot_startup():
    logger.remove()
    special_format: str = (
        # "<g>{time:%m-%d %H:%M:%S.%f}</g> "
        "<g>{time:MM-DD HH:mm:ss}</g> "
        "[<lvl>{level}</lvl>] "
        "<c><u>{name}</u></c> | "
        "<c>{function}:{line}</c>| "
        "{message}"
    )
    logger.add(
        sys.stdout,
        level="DEBUG",
        format=special_format,
    )

    custom_format = (
        "<g>{time:YYYY-MM-DD HH:mm:ss}</g> " "[{level}] " "{name} | " "{message}"
    )
    logger.add(
        LOG_PATH + "debug/{time:YYYY-MM-DD}.log",
        rotation="00:00",
        retention=f"{DEBUG_LOG_TIME} days",
        level="DEBUG",
        format=custom_format,
        encoding="utf-8",
    )
    logger.add(
        LOG_PATH + "info/{time:YYYY-MM-DD}.log",
        rotation="00:00",
        retention=f"{INFO_LOG_TIME} days",
        level="INFO",
        format=custom_format,
        encoding="utf-8",
    )
    logger.add(
        LOG_PATH + "warning/{time:YYYY-MM-DD}.log",
        rotation="00:00",
        retention=f"{WARNING_LOG_TIME} days",
        level="WARNING",
        format=custom_format,
        encoding="utf-8",
    )
    logger.add(
        LOG_PATH + "error/{time:YYYY-MM-DD}.log",
        rotation="00:00",
        retention=f"{ERROR_LOG_TIME} days",
        level="ERROR",
        format=custom_format,
        encoding="utf-8",
    )
    # logger.add(
    #     sys.stdout,
    #     level="INFO",
    #     format=custom_format,
    # )
    # logger.add(
    #     LOG_PATH + "database/{time:YYYY-MM-DD}.log",
    #     rotation="00:00",
    #     filter=lambda record: "数据库" in record['message']
    #                           or "Database" in record['message']
    #                           or "db" in record['message'],
    #     format=custom_format,
    #     encoding="utf-8",
    # )

    logger.info("Bot started.")
    db.connect()


async def shutdown():
    logger.info("Shutting down...")
    db.close()
