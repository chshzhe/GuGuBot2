from configs.path_config import DATABASE_PATH
from .db import *
from .send_queue import *
import asyncio
from nonebot import get_driver, logger
from utils.permission_checker import auth_manager


db = SQLiteDB(DATABASE_PATH + "GuGuBot.db")
message_queue = MessageQueue()

driver = get_driver()


@driver.on_startup
async def init_db():
    db.connect()
    logger.info("数据库已连接")


@driver.on_shutdown
async def close_db():
    db.close()
    logger.info("数据库已关闭")


@driver.on_bot_connect
async def auth_manager_handle():
    global message_queue
    logger.debug("已连接到BOT")
    auth_manager.load_plugin_default_perm_and_desc()
    await asyncio.create_task(message_queue.message_sender())

