from nonebot import on_message
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import GROUP, Bot, MessageEvent, Message
from nonebot.log import logger
from configs.config import BOT_NAME

__plugin_name__ = "接个龙龙"
__plugin_usage__ = f"""什么逆天功能~
早安/晚安：来自{BOT_NAME}的问候
"""

Test = on_message(
    permission=GROUP,
    priority=1,
    block=False
)


@Test.handle()
async def handle_receive(bot: Bot, event: MessageEvent, state: T_State):
    logger.debug(event.original_message)
    # logger.debug(event.raw_message)
    # logger.debug(event.message)
    # logger.debug(event.message_id)
    # logger.debug(event.message_type)
    # logger.debug(event.sub_type)
    # logger.debug(event.time)
    # logger.debug(event.user_id)
    # logger.debug(event)
    await Test.finish()
