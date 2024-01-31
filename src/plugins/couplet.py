
from nonebot import on_startswith, logger, on_command
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import GROUP, Bot, MessageEvent, Message
import random
import httpx

__plugin_name__ = "对联"
__plugin_usage__ = f"""咕咕给您生成对联
对联 <上联>：生成对应的下联
对对联 <上联>：随机生成对应的下联
"""


from utils.send_queue import message_queue

Couplet = on_startswith(("对联 ", "对对联 "), permission=GROUP, priority=15)


url_base = 'https://seq2seq-couplet-model.rssbrain.com/v0.2/couplet/'


async def couplet(shanglian, is_random=False) -> str:
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(url=url_base + shanglian)
        response = resp.json()['output']
    except Exception as e:
        logger.error(f'对联接口返回值异常，上联：{shanglian}，错误信息：{e}')
        return '服务器出错啦，请稍后再试'
    if not response:
        logger.error(f'对联接口返回空值，上联：{shanglian}')
        return '服务器出错啦，请稍后再试'
    if is_random:
        return random.choice(response)
    else:
        if '李克强' in response[0]:
            return ''
        else:
            return response[0]


@Couplet.handle()
async def handle_receive(bot: Bot, event: MessageEvent, state: T_State):
    if event.raw_message.startswith("对联 "):
        shang_lian = event.raw_message.replace("对联 ", "")
        message = f"上联：{shang_lian}\n下联：{await couplet(shang_lian)}"
    else:
        shang_lian = event.raw_message.replace("对对联 ", "")
        message = f"上联：{shang_lian}\n下联：{await couplet(shang_lian, is_random=True)}"

    message_queue.put((Message(message), event, bot))
    logger.debug(f"进入队列：{message}")
    logger.success(f"用户：{event.user_id}，在群：{event.group_id}，对bot使用了对联")
    await Couplet.finish()
