import asyncio
from queue import Queue

from nonebot import logger


async def send_message():
    while not message_queue.empty():
        message, event, bot = message_queue.get()
        logger.success(f"发送消息：{message}")
        await bot.send(event, message)
        await asyncio.sleep(0.6)


async def message_sender():
    while True:
        if not message_queue.empty():
            await send_message()
        else:
            await asyncio.sleep(0.1)


message_queue = Queue()
