import asyncio
from nonebot import get_driver, logger

from utils.db import db
from utils.send_queue import message_sender
from utils.permission_checker import auth_manager

driver = get_driver()


@driver.on_bot_connect
async def _():
    logger.debug("已连接到BOT")
    auth_manager.load_plugin_default_perm_and_desc()
    await asyncio.create_task(message_sender())
