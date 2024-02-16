import random
from nonebot import on_startswith
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import GROUP, Bot, MessageEvent, Message
from nonebot.log import logger
from configs.config import BOT_NAME
from utils.data import BOOK
from utils.permission_checker import auth_manager
from utils.send_queue import message_queue

__plugin_name__ = "答案之书"
__plugin_usage__ = f"""通过马纳姆效应解决历史难题
{BOT_NAME}，……: 告诉你如何解决……
"""
__plugin_cmd_name__ = "answerbook"
__command_description__ = f"通过马纳姆效应解决历史难题：{BOT_NAME}，[...]"
__default_permission__ = True

AnswerBook = on_startswith((f"{BOT_NAME}，", f"{BOT_NAME} ", f"{BOT_NAME},", f"{BOT_NAME}.", f"{BOT_NAME}。"),
                           rule=auth_manager.get_rule(f"{__plugin_cmd_name__}"),
                           permission=GROUP,
                           priority=12,
                           )


@AnswerBook.handle()
async def handle_receive(bot: Bot, event: MessageEvent, state: T_State):
    answer = random.choice(BOOK)
    message_queue.put((Message(f"[CQ:reply,id={event.message_id}]{answer}"), event, bot))
    logger.debug(f"进入队列：{answer}")
    logger.info(f"用户：{event.user_id}，在群：{event.group_id}，使用了答案之书")

    await AnswerBook.finish()
