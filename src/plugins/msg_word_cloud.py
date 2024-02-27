import datetime
import logging
import re
from typing import List, Dict

from wordcloud import WordCloud
import jieba
import jieba.analyse
from emoji import replace_emoji
from nonebot import on_command
from nonebot.params import CommandArg
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import GROUP, Bot, MessageEvent, MessageSegment
from nonebot.log import logger
from utils import db
from configs.path_config import FONT_PATH, TEMP_PATH
from utils.msg_util import text, upload_for_shamrock
from utils.permission_checker import auth_manager
from utils import message_queue

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
__command_description__ = {
    "wc": """生成本群昨日词云：-wc\n生成指定用户近三天词云：-wc <QQ号>\n生成自己的词云：-wcme""",
    "wcsub": "词云订阅"
}
MsgWordCloud = on_command("-wc",
                          rule=auth_manager.get_rule(f"{__plugin_cmd_name__}", "wc"),
                          permission=GROUP,
                          priority=18,
                          )

select = ["E", "W", "F", "UP", "C", "T", "PYI", "Q"]
ignore = ["E402", "E501", "E711", "C901", "UP037"]
jieba.setLogLevel(logging.WARNING)

@MsgWordCloud.handle()
async def handle_receive(bot: Bot, event: MessageEvent, state: T_State, args=CommandArg()):
    logger.info(f"用户：{event.user_id}，在群：{event.group_id}，使用了词云生成，参数{args}")
    args = str(args).strip()
    if args == "":
        logger.debug(f"wc命令")
        msg = await generate_word_cloud(event.group_id)
        message_queue.put((msg, event, bot))
    elif args == "me":
        logger.debug(f"wcme命令")
        msg = await generate_word_cloud(event.group_id, event.user_id)
        message_queue.put((msg, event, bot))
    else:
        if not str(args).isdigit():
            logger.debug(f"参数错误")
            msg = "参数错误"
            message_queue.put((msg, event, bot))
        else:
            logger.debug(f"-wc {args}命令")
            user_id = int(args)
            msg = await generate_word_cloud(event.group_id, user_id)
            message_queue.put((msg, event, bot))

    await MsgWordCloud.finish()


async def generate_word_cloud(group_id: int, user_id: int = None) -> MessageSegment:
    if not db.table_exists(f"msg{group_id}"):
        return text("本群暂无消息记录诶")
    else:
        if user_id:
            data = db.query(f"SELECT message FROM msg{group_id} "
                            f"WHERE user_id = {user_id} "
                            f"AND time > datetime('now', '-3 day')")
        else:
            data = db.query(f"SELECT message FROM msg{group_id} "
                            f"WHERE time > datetime('now', '-1 day')")
        if not data:
            return text("暂无消息记录诶")
        else:
            frequency = data_filter(data)
            if frequency == {}:
                return text("暂无消息记录诶")
            path = TEMP_PATH
            file = f"wordcloud_{int(datetime.datetime.now().timestamp())}_{group_id}_{user_id}.png"
            await generate_picture(frequency, path + file)
            msg = await upload_for_shamrock(path, file)
            if msg:
                return msg
            else:
                return text("生成词云失败")


async def generate_picture(frequency: Dict[str, float], filename: str):
    wordcloud_options = {}
    wordcloud_options.setdefault("font_path", FONT_PATH + "HYWenHei-85W.otf")
    wordcloud_options.setdefault("width", 800)
    wordcloud_options.setdefault("height", 600)
    wordcloud_options.setdefault(
        "background_color", 'white'
    )
    wordcloud = WordCloud(**wordcloud_options)
    generate_image = wordcloud.generate_from_frequencies(frequency).to_image()
    generate_image.save(filename, format="PNG")


def data_filter(data: List[str]) -> Dict[str, float]:
    msg_list = [item[0] for item in data]
    msg_list = [re.sub(r'\[CQ:[^\]]+\]', '', item) for item in msg_list]
    command_start_list = ['/', '#', '-']
    command_start = tuple(i for i in command_start_list if i)
    message = " ".join(m for m in msg_list if not m.startswith(command_start))
    # 预处理
    message = pre_precess(message)
    # 分析消息。分词，并统计词频
    frequency = analyse_message(message)
    return frequency


def pre_precess(msg: str) -> str:
    """对消息进行预处理"""
    # 去除网址
    # https://stackoverflow.com/a/17773849/9212748
    url_regex = re.compile(
        r"(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]"
        r"+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})"
    )
    msg = url_regex.sub("", msg)

    # 去除 \u200b
    msg = re.sub(r"\u200b", "", msg)
    msg = re.sub(r"&#91", "", msg)
    msg = re.sub(r"&#93", "", msg)

    # 去除 emoji
    # https://github.com/carpedm20/emoji
    msg = replace_emoji(msg)

    return msg


def analyse_message(msg: str) -> Dict[str, float]:
    """分析消息
    分词，并统计词频
    """
    # 设置停用词表
    # if plugin_config.wordcloud_stopwords_path:
    #     jieba.analyse.set_stop_words(plugin_config.wordcloud_stopwords_path)
    # # 加载用户词典
    # if plugin_config.wordcloud_userdict_path:
    #     jieba.load_userdict(str(plugin_config.wordcloud_userdict_path))
    # 基于 TF-IDF 算法的关键词抽取
    # 返回所有关键词，因为设置了数量其实也只是 tags[:topK]，不如交给词云库处理
    words = jieba.analyse.extract_tags(msg, topK=0, withWeight=True)
    return dict(words)
