import sys
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from loguru import Logger, Record
from nonebot.log import logger, logger_id
from configs.config import INFO_LOG_TIME, DEBUG_LOG_TIME, ERROR_LOG_TIME, WARNING_LOG_TIME
from configs.path_config import LOG_PATH
from utils.db import db


def custom_filter(record: "Record"):
    # 排除info级别的日志
    log_level = record["extra"].get("nonebot_log_level", "INFO")
    levelno = logger.level(log_level).no if isinstance(log_level, str) else log_level
    flag1 = record["level"].no >= levelno
    if record["function"] in ['_run_matcher', 'simple_run']:
        flag2 = False
    else:
        flag2 = True
    return flag1 and flag2


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
        level=0,
        format=special_format,
        filter=custom_filter
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
