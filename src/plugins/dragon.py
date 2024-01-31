from nonebot import on_fullmatch
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import GROUP, Bot, MessageEvent, Message
from nonebot.log import logger
from configs.config import BOT_NAME
from utils.send_queue import message_queue

__plugin_name__ = "接个龙龙"
__plugin_usage__ = f"""什么逆天功能~
早安/晚安：来自{BOT_NAME}的问候
"""

Dragon = on_fullmatch(("龙", "接龙", """&#91;该消息类型不支持查看，请使用QQ最新版本&#93;"""),
                      permission=GROUP,
                      priority=13,
                      )


@Dragon.handle()
async def handle_receive(bot: Bot, event: MessageEvent, state: T_State):
    message_queue.put((Message(f"[CQ:face,id=394,big=true]"), event, bot))
    logger.debug(f"进入队列：[CQ:face,id=394,big=true]")
    logger.info(f"用户：{event.user_id}，在群：{event.group_id}，使用了接龙")

    await Dragon.finish()
