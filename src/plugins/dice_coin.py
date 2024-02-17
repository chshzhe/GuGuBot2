import random
from nonebot import on_startswith
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import GROUP, Bot, MessageEvent, Message
from nonebot.log import logger
from configs.config import BOT_NAME
from utils.data import BOOK
from utils.permission_checker import auth_manager
from utils.send_queue import message_queue

__plugin_name__ = "骰子&硬币"
__plugin_usage__ = f"""抛硬币或者骰子
"""
__plugin_cmd_name__ = "choice"
__command_description__ = {
    "coin": "抛硬币：投个硬币/抛硬币/-coin[...]",
    "dice": "抛骰子：投个骰子/抛骰子/-dice[...]"
}
__default_permission__ = {
    "coin": True,
    "dice": True
}

Coin = on_startswith(("投个硬币", "抛硬币", "-coin"),
                     rule=auth_manager.get_rule(f"{__plugin_cmd_name__}", "coin"),
                     permission=GROUP,
                     priority=22,
                     )

Dice = on_startswith(("投个骰子", "抛骰子", "-dice"),
                     rule=auth_manager.get_rule(f"{__plugin_cmd_name__}", "dice"),
                     permission=GROUP,
                     priority=22,
                     )


@Coin.handle()
async def coin_handle(bot: Bot, event: MessageEvent, state: T_State):
    answer = random.random()
    rate = 0.49
    if answer < rate:
        answer = "是正面！"
    elif answer > 1 - rate:
        answer = "是反面！"
    else:
        answer = "硬币竖着立了起来~"
    message_queue.put((Message(f"[CQ:reply,id={event.message_id}]{answer}"), event, bot))
    logger.debug(f"进入队列：抛硬币：{answer}")
    logger.info(f"用户：{event.user_id}，在群：{event.group_id}，使用了抛硬币")

    await Coin.finish()


@Dice.handle()
async def dice_handle(bot: Bot, event: MessageEvent, state: T_State):
    answer = random.randint(1, 6)
    message_queue.put((Message(f"[CQ:reply,id={event.message_id}]🎲{answer}"), event, bot))
    logger.debug(f"进入队列：抛骰子：{answer}")
    logger.info(f"用户：{event.user_id}，在群：{event.group_id}，使用了抛骰子")

    await Dice.finish()
