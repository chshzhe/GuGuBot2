from nonebot import on_fullmatch
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import GROUP, Bot, MessageEvent, Message
from nonebot.log import logger
from configs.config import SUPERUSERS
from utils.permission_checker import auth_manager
from utils import message_queue

__plugin_name__ = "自助问答"
__plugin_usage__ = None
__plugin_cmd_name__ = "faq"

__default_permission__ = {
    "faq": True,
    "faqstatus": ["Normal"],
    "faqadmin": [] + SUPERUSERS
}
__command_description__={
    "faq": "自助问答：问 [...]\n不过还没写好",
    "faqstatus": "自助问答权限管理状态",
    "faqadmin": "自助问答管理"
}


Dragon = on_fullmatch(("龙",
                       "接龙",
                       # """[该消息类型不支持查看，请使用QQ最新版本]"""
                       ),
                      rule=auth_manager.get_rule(f"{__plugin_cmd_name__}"),
                      permission=GROUP,
                      priority=13,
                      )


@Dragon.handle()
async def handle_receive(bot: Bot, event: MessageEvent, state: T_State):
    message = "[CQ:face,id=394]"
    message_queue.put((Message(message), event, bot))
    logger.debug(f"进入队列：{message}")
    logger.info(f"用户：{event.user_id}，在群：{event.group_id}，使用了接龙")

    await Dragon.finish()
