from random import random, choice
from nonebot import on_notice
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import Bot, Event, Message, PokeNotifyEvent
from nonebot.log import logger
from configs.config import BOT_NAME
from utils.permission_checker import auth_manager
from utils.send_queue import message_queue

__plugin_name__ = "戳一戳"
__plugin_usage__ = f"""戳戳你的~
大概是bot被戳了就会反戳你一下，说不定还有彩蛋呢~
"""
__plugin_cmd_name__ = "poke"

__default_permission__ = True


async def __poke_notify__(bot: Bot, event: Event) -> bool:
    if isinstance(event, PokeNotifyEvent) and event.notice_type == 'notify' and event.sub_type == 'poke' and event.is_tome():
        return True
    return False


Poke = on_notice(rule=__poke_notify__ & auth_manager.get_rule(f"{__plugin_cmd_name__}"),
                 priority=1,
                 block=False,
                 )


@Poke.handle()
async def handle_receive(bot: Bot, event: Event, state: T_State):
    if random() < 0.3:
        message = choice([
            "不准戳不准戳！！！",
            "不要戳啦！！呜呜呜",
            f"再戳{BOT_NAME}就生气啦！",
            "真的有那么好戳嘛...",
            "嘤嘤嘤，被戳痛了呜呜呜",
            "不可以戳这里！",
            "再戳会坏掉的QAQ",
            # "恕我突兀，你是否知晓「纯美」的女神伊德莉拉"
        ])
    else:
        # message = Message(f"[CQ:poke,qq={event.user_id}]")    #go-cqhttp
        # message = Message(f"[CQ:poke,type=1,id={event.user_id}]")     #Shamrock
        message = Message(f"[CQ:touch,id={event.user_id}]")  # Shamrock

    message_queue.put((Message(message), event, bot))
    logger.debug(f"进入队列：{message}")
    logger.info(f"用户：{event.user_id}，在群：{event.group_id}，对bot使用了戳一戳")
    await Poke.finish()
