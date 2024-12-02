from typing import Optional
import httpx
from nonebot import on_startswith, logger
from nonebot.adapters.onebot.v11 import GROUP, Bot, MessageEvent, Message
from nonebot.typing import T_State
from configs.config import BOT_NAME
from utils.permission_checker import auth_manager
from utils import message_queue

__plugin_name__ = "表白"
__plugin_usage__ = f"""咕咕帮您表白~
表白xxx：咕咕帮您表白xxx
"""

__plugin_cmd_name__ = "declaration"

__default_permission__ = False
__command_description__ = f"{BOT_NAME}帮你表白：表白[...]"
Declaration = on_startswith("表白",
                            rule=auth_manager.get_rule(f"{__plugin_cmd_name__}"),
                            permission=GROUP,
                            priority=16,
                            )

# url = 'https://api.vvhan.com/api/love'
url = "https://api.lovelive.tools/api/SweetNothings"


async def declaration() -> Optional[str]:
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(url=url)
        txt = resp.text
    except Exception as e:
        logger.error(f'表白接口返回值异常，错误信息：{e}')
        return None
    if not txt:
        logger.error(f'表白接口返回空值')
        return None
    return txt


@Declaration.handle()
async def handle_receive(bot: Bot, event: MessageEvent, state: T_State):
    sender = event.raw_message.replace("表白", "")
    if sender != "" and not sender.isspace():
        declaration_str = await declaration()
        if declaration_str is None:
            message = f"咕咕出错啦，请稍后再试"
        else:
            message = f"{sender}，{declaration_str}"
        message_queue.put((Message(message), event, bot))
        logger.debug(f"进入队列：{message}")
        logger.info(f"用户：{event.user_id}，在群：{event.group_id}，使用了表白")
        await Declaration.finish()
    else:
        message = "你要表白谁捏？"
        message_queue.put((Message(message), event, bot))
        logger.debug(f"进入队列：{message}")
        logger.info(f"用户：{event.user_id}，在群：{event.group_id}，使用了表白，没有提供表白对象")
        await Declaration.reject()
