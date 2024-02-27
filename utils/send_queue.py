import asyncio
from queue import Queue

from nonebot import logger
from nonebot.adapters.onebot.v11 import Event


class MessageQueue:
    def __init__(self):
        self.message_queue = Queue()

    async def send_message(self):
        while not self.message_queue.empty():
            try:
                (message, event, bot, *args) = self.message_queue.get()
                if isinstance(event, Event):
                    if not args:
                        await bot.send(event, message)
                        logger.success(f"发送消息：{message}")
                    else:
                        if args[0] == "approve_add_group_require":
                            await bot.set_group_add_request(flag=event.flag, sub_type=event.sub_type, approve=True)
                            logger.success(f"同意加群请求：{event}")
                        elif args[0] == "reject_add_group_require":
                            await bot.set_group_add_request(flag=event.flag, sub_type=event.sub_type, approve=False,
                                                            reason=message)
                            logger.success(f"拒绝加群请求：{event}")
                        else:
                            logger.error(f"发送消息失败1：未知的event类型，{message, event, bot, args}")
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
                    logger.error(f"发送消息失败2：未知的event类型，{message, event, bot, args}")
                await asyncio.sleep(1.5)
            except Exception as e:
                logger.error(f"发送消息失败,{e}")
            await asyncio.sleep(0.5)

    async def message_sender(self):
        while True:
            if not self.message_queue.empty():
                await self.send_message()
            else:
                await asyncio.sleep(1)

    def put(self, *args):
        self.message_queue.put(*args)
        return True
