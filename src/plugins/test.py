from nonebot import on_fullmatch
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import GROUP, Bot, MessageEvent, Message
from nonebot.log import logger

__plugin_name__ = "测试"
__plugin_usage__ = f"""什么逆天功能~
114514
"""
__plugin_cmd_name__ = "test"

__default_permission__ = {
    "test": True
}
__command_description__ = {
    "test": "测试"
}

from utils.msg_util import image
# __default_permission__ = True
# __default_permission__ = ["1234567"]

from utils.permission_checker import auth_manager

Test = on_fullmatch("test",
                    permission=auth_manager.get_permission("test", "test"),
                    priority=1,
                    block=False
                    )


@Test.handle()
async def handle_receive(bot: Bot, event: MessageEvent, state: T_State):
    logger.debug(event.original_message)
    # await bot.send(event, image(abspath="D:\\GITHUB\\GuGuBot2\\temp\\temp.png"))
    await Test.finish()
