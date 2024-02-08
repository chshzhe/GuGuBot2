import re
from wordcloud import WordCloud
import jieba
from nonebot import on_command
from nonebot.params import CommandArg
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import GROUP, Bot, MessageEvent, Message
from nonebot.log import logger
from utils.db import db
from configs.path_config import FONT_PATH, TEMP_PATH
from utils.send_queue import message_queue

__plugin_name__ = "词云"
__plugin_usage__ = f"""根据历史发言生成词云
-wc: 生成本群词云
-wc <QQ号>: 生成指定用户词云
-wcme: 生成自己的词云
"""

__plugin_cmd_name__ = "wc"

__default_permission__ = {
    "wc": True,
    "wcsub": False
}
__default_permission_cn__ = {
    "wc": "词云生成",
    "wcsub": "词云订阅"
}

MsgWordCloud = on_command("-wc",
                          permission=GROUP,
                          priority=18,
                          )


@MsgWordCloud.handle()
async def handle_receive(bot: Bot, event: MessageEvent, state: T_State, args=CommandArg()):
    logger.info(f"用户：{event.user_id}，在群：{event.group_id}，使用了词云生成，参数{args}")
    args = str(args).strip()
    # 根据参数区分不同的命令逻辑
    if args == "":
        logger.debug(f"wc命令")
        msg = await generate_word_cloud(event.group_id)
        message_queue.put((Message(msg), event, bot))

    elif args == "me":
        logger.debug(f"wcme命令")
        msg = await generate_word_cloud(event.group_id, event.user_id)
        message_queue.put((Message(msg), event, bot))

    else:
        if not str(args).isdigit():
            logger.debug(f"参数错误")
            msg = "参数错误"
            message_queue.put((Message(msg), event, bot))

        else:
            logger.debug(f"-wc {args}命令")
            user_id = int(args)
            msg = await generate_word_cloud(event.group_id, user_id)
            message_queue.put((Message(msg), event, bot))

    await MsgWordCloud.finish()


async def generate_word_cloud(group_id: int, user_id: int = None):
    if not db.table_exists(f"msg{group_id}"):
        return "本群暂无消息记录诶"
    else:
        if user_id:
            data = db.query(f"SELECT message FROM msg{group_id} WHERE user_id = {user_id}")
        else:
            data = db.query(f"SELECT message FROM msg{group_id}")
        if not data:
            return "暂无消息记录诶"
        else:
            logger.debug(data)
            string_list = [item[0] for item in data]
            cleaned_list = [re.sub(r'\[CQ:[^\]]+\]', '', item) for item in string_list]
            no_empty_lines = [line for line in cleaned_list if line.strip()]
            result_no_empty = '\n'.join(no_empty_lines)
            logger.debug(result_no_empty)
            await generate_picture(result_no_empty)
            return "正常"


async def generate_picture(text: str):
    text = ' '.join(jieba.cut(text))  # 利用jieba进行分词形成列表，将列表里面的词用空格分开并拼成长字符串。
    logger.debug(text[:4])  # 打印前100个字符
    logger.debug(text[-4:])  # 打印后100个字符
    # 生成对象
    wc = WordCloud(font_path=FONT_PATH + "HYWenHei-85W.otf",
                   width=800,
                   height=600,
                   mode="RGBA",
                   background_color=None
                   ).generate(text)
    wc.to_file(TEMP_PATH + "wordcloud.png")
