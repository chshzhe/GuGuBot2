import asyncio
from queue import Queue

from nonebot import logger
from nonebot.adapters.onebot.v11 import Event


class MessageQueue:
    def __init__(self):
        self.message_queue = Queue()

    async def _send_message(self):
        while not self.message_queue.empty():
            try:
                (message, event, bot, *args) = self.message_queue.get()
                if isinstance(event, Event):
                    if not args:
                        _response = await bot.send(event, message)
                        logger.success(f"发送消息：{message}")
                        # Todo: 测试返回值情况
                        if not (isinstance(_response,dict) and _response.keys() == {"message_id", "time"}):
                            logger.warning(f"发送消息返回|\033[31m{_response}\033[0m")
                    else:
                        logger.error(f"发送消息失败：未知的event类型，{message, event, bot, args}")
                        # if args[0] == "approve_add_group_require":
                        #     await bot.set_group_add_request(flag=event.flag, sub_type=event.sub_type, approve=True)
                        #     logger.success(f"同意加群请求：{event}")
                        # elif args[0] == "reject_add_group_require":
                        #     await bot.set_group_add_request(flag=event.flag, sub_type=event.sub_type, approve=False,
                        #                                     reason=message)
                        #     logger.success(f"拒绝加群请求：{event}")
                        # else:
                        #     logger.error(f"发送消息失败1：未知的event类型，{message, event, bot, args}")
                elif isinstance(event, int):
                    if args[0] == "group":
                        _response = await bot.send_group_msg(group_id=event, message=message)
                        logger.success(f"发送群消息：{message}")
                        logger.debug(f"发送消息返回：{_response}")
                    elif args[0] == "private":
                        _response = await bot.send_private_msg(user_id=event, message=message)
                        logger.success(f"发送私聊消息：{message}")
                        logger.debug(f"发送消息返回：{_response}")
                    else:
                        logger.error(f"发送消息失败：未知的event类型，{message, event, bot, args}")
                else:
                    logger.error(f"发送消息失败：未知的event类型，{message, event, bot, args}")
                await asyncio.sleep(1.5)
            except Exception as e:
                logger.error(f"发送消息失败,{e}")
            await asyncio.sleep(0.5)

    async def message_sender(self):
        while True:
            if not self.message_queue.empty():
                await self._send_message()
            else:
                await asyncio.sleep(1)

    def put(self, *args):
        self.message_queue.put(*args)
        return True


class RequestQueue:
    def __init__(self):
        self.request_queue = Queue()

    async def _send_request(self):
        while not self.request_queue.empty():
            try:

                (bot, flag, subtype, approve, message) = self.request_queue.get()
                if approve:
                    _response = await bot.set_group_add_request(flag=flag, sub_type=subtype, approve=True)
                    logger.success(f"同意加群请求")
                    if _response != "已同意该申请":
                        logger.warning(f"出现报错|\033[31m{_response}\033[0m")
                else:
                    _response = await bot.set_group_add_request(flag=flag, sub_type=subtype, approve=False,
                                                                reason=message)
                    logger.success(f"拒绝加群请求")
                    if _response != "已拒绝该申请":
                        logger.warning(f"出现报错|\033[31m{_response}\033[0m")
            except Exception as e:
                logger.error(f"发送消息失败,{e}")
            await asyncio.sleep(0.5)

    async def request_sender(self):
        while True:
            # logger.debug(f"request_queue size: {self.request_queue.qsize()}")
            if not self.request_queue.empty():
                await self._send_request()
            else:
                await asyncio.sleep(1)

    def put(self, *args):
        logger.debug(f"request_queue put: {args}")
        self.request_queue.put(*args)
        return True
