from configs.path_config import DATABASE_PATH
from .db import *
from .send_queue import *
import asyncio
from nonebot import get_driver, logger
from utils.permission_checker import auth_manager

msg_db = SQLiteDB(DATABASE_PATH + "GuGuBot.db")
message_queue = MessageQueue()
request_queue = RequestQueue()
driver = get_driver()


@driver.on_startup
async def init_db():
    msg_db.connect()
    logger.info("数据库已连接")


@driver.on_shutdown
async def close_db():
    msg_db.close()
    logger.info("数据库已关闭")


@driver.on_bot_connect
async def auth_manager_handle():
    global message_queue
    global request_queue
    logger.debug("已连接到BOT")
    auth_manager.load_plugin_default_perm_and_desc()
    await init_send_queue()


async def init_send_queue():
    msg_queue_task = asyncio.create_task(message_queue.message_sender())
    rqt_queue_task = asyncio.create_task(request_queue.request_sender())
    await asyncio.gather(msg_queue_task, rqt_queue_task)
