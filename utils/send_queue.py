import asyncio
from queue import Queue

from nonebot import logger
from nonebot.adapters.onebot.v11 import Event


async def send_message():
    while not message_queue.empty():
        try:
            message, event, bot, *args = message_queue.get()
            if isinstance(event, Event):
                await bot.send(event, message)
                logger.success(f"发送消息：{message}")
            elif isinstance(event, int):
                if args[0] == "group":
                    await bot.send_group_msg(group_id=event, message=message)
                    logger.success(f"发送群消息：{message}")
                elif args[0] == "private":
                    await bot.send_private_msg(user_id=event, message=message)
                    logger.success(f"发送私聊消息：{message}")
                else:
                    logger.error(f"发送消息失败：未知的event类型，{message, event, bot, args}")
            else:
                logger.error(f"发送消息失败：未知的event类型，{message, event, bot, args}")
            await asyncio.sleep(0.6)
        except Exception as e:
            logger.error(f"发送消息失败,{e}")


async def message_sender():
    while True:
        if not message_queue.empty():
            await send_message()
        else:
            await asyncio.sleep(0.1)


message_queue = Queue()
