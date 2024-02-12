from nonebot import on_fullmatch, on_message
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import GROUP, Bot, MessageEvent, Message
from nonebot.log import logger
from configs.config import BOT_NAME
from utils.permission_checker import auth_manager
from utils.send_queue import message_queue

__plugin_name__ = "群权限管理"
__plugin_usage__ = f"""大概是个占位符吧"""
__plugin_cmd_name__ = "admin"

__default_permission__ = [1299946476, ]

MessageStorage = on_message(permission=GROUP,
                            rule=auth_manager.get_rule(f"{__plugin_cmd_name__}"),
                            priority=3,
                            block=False

                            )