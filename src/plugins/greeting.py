import random
from nonebot import on_startswith
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import GROUP, Bot, MessageEvent, Message
from nonebot.log import logger
from configs.config import BOT_NAME
from utils.data import MORNING, NIGHT
from utils.permission_checker import auth_manager
from utils.send_queue import message_queue

__plugin_name__ = "一声问候"
__plugin_usage__ = f"""早安晚安捏~
早安/晚安：来自{BOT_NAME}的问候
"""
__plugin_cmd_name__ = "greeting"
__command_description__="来自咕咕的问候：早安[...]/晚安[...]"
__default_permission__ = True

Morning = on_startswith("早安",
                        rule=auth_manager.get_rule(f"{__plugin_cmd_name__}"),
                        permission=GROUP,
                        priority=13,
                        )

Night = on_startswith("晚安",
                      rule=auth_manager.get_rule(f"{__plugin_cmd_name__}"),
                      permission=GROUP,
                      priority=13,
                      )


@Morning.handle()
async def handle_receive(bot: Bot, event: MessageEvent, state: T_State):
    morning = random.choice(MORNING)
    message_queue.put((Message(f"[CQ:reply,id={event.message_id}]{morning}"), event, bot))
    logger.debug(f"进入队列：{morning}")
    logger.info(f"用户：{event.user_id}，在群：{event.group_id}，使用了早安")

    await Morning.finish()


@Night.handle()
async def handle_receive(bot: Bot, event: MessageEvent, state: T_State):
    night = random.choice(NIGHT)
    message_queue.put((Message(f"[CQ:reply,id={event.message_id}]{night}"), event, bot))
    logger.debug(f"进入队列：{night}")
    logger.info(f"用户：{event.user_id}，在群：{event.group_id}，使用了晚安")

    await Morning.finish()
