import asyncio

from nonebot import get_driver, logger

from utils.send_queue import message_sender

driver = get_driver()


@driver.on_bot_connect
async def _():
    logger.debug("已连接到BOT")
    # 安排异步任务
    await asyncio.create_task(message_sender())
