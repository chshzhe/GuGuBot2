import datetime
import random
import httpx
from nonebot import on_fullmatch, logger
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import GROUP, Bot, MessageEvent, Message, MessageSegment

from configs.path_config import TEMP_PATH
from utils.msg_util import text, image
from utils.permission_checker import auth_manager
from utils import message_queue

__plugin_name__ = "来点那个"
__plugin_usage__ = f"""roll一张二次元图片
来点那个：你懂的..."""
__plugin_cmd_name__ = "picture"

__default_permission__ = False
__command_description__ = "来点动漫图片：来点那个"
Couplet = on_fullmatch("来点那个",
                       rule=auth_manager.get_rule(f"{__plugin_cmd_name__}"),
                       permission=GROUP,
                       priority=20,

                       )

url_1 = 'https://api.btstu.cn/sjbz/?lx=dongman&format=json'
url_2 = "https://img.xjh.me/random_img.php?type=bg&ctype=acg&return=json"
url_3 = "https://loli.garden/ranimg/api.php"


# find more at https://air.moe/archives/17

async def get_picture() -> MessageSegment:
    try:
        async with httpx.AsyncClient(follow_redirects=True) as client:
            response = await client.get(url_3)
            pic_res = response.url
        async with httpx.AsyncClient() as client:
            pic_res = await client.get(pic_res)

        # async with httpx.AsyncClient() as client:
        #     response = await client.get(url_2)
        # url2 = "https:"+response.json()["img"]
        # logger.debug(f"图片url：{url2}")
        # async with httpx.AsyncClient() as client:
        #     pic_res = await client.get(url2)

        # async with httpx.AsyncClient() as client:
        #     pic_res = await client.get(url)
        # async with httpx.AsyncClient() as client:
        #     response = await client.get(url_1)
        # url = response.json()["imgurl"]
        # async with httpx.AsyncClient() as client:
        #     pic_res = await client.get(url)
        # logger.debug(f"图片url：{url}")
        path = TEMP_PATH
        filename = f"animation_{int(datetime.datetime.now().timestamp())}_{random.randint(0, 100000)}.jpg"
        with open(path + filename, "wb") as f:
            f.write(pic_res.content)
        msg = image(abspath=f"{path}{filename}")
    except Exception as e:
        logger.error(f"获取图片失败：{e}")
        msg = text("获取图片失败")
    return msg


@Couplet.handle()
async def handle_receive(bot: Bot, event: MessageEvent, state: T_State):
    msg = await get_picture()
    message_queue.put((msg, event, bot))
    logger.debug(f"进入队列：{msg}")
    logger.info(f"用户：{event.user_id}，在群：{event.group_id}，使用了来点那个")
    await Couplet.finish()
