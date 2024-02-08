from typing import Dict, List
import httpx
import lxml
from bs4 import BeautifulSoup
from nonebot import on_startswith
from nonebot.adapters.onebot.v11 import GROUP, Bot, MessageEvent, Message
from nonebot import get_bot
from nonebot.log import logger
from nonebot_plugin_apscheduler import scheduler
from nonebot.typing import T_State
from configs.config import PREVIEW_GROUP
from utils.permission_checker import auth_manager
from utils.send_queue import message_queue

news_list = []

jwc_news_url = ["https://jwc.sjtu.edu.cn/xwtg/tztg.htm",
                "https://jwc.sjtu.edu.cn/index/mxxsdtz.htm"
                ]

__plugin_name__ = "教务处通知推送"
__plugin_usage__ = f"""订阅教务处通知
-jwc: 教务处最近10条通知,
-jwc off: 关闭订阅,
-jwc on: 开启订阅,
-jwc help: 打开帮助,
"""

__plugin_cmd_name__ = "jwc"

__default_permission__ = {
    "jwc": True,
    "jwcsub": False
}
__default_permission_cn__ = {
    "jwc": "教务处通知查询",
    "jwcsub": "教务处通知订阅"
}

Jwc_message = on_startswith(("-jwc",),
                            rule=auth_manager.get_rule(f"jwc", "jwc"),
                            permission=GROUP,
                            priority=17
                            )


@Jwc_message.handle()
async def handle_receive(bot: Bot, event: MessageEvent, state: T_State):
    if event.raw_message == "-jwc":
        global news_list
        # news_list = await get_news_list()
        news_list.sort(key=lambda x: x["time"], reverse=True)
        msg = ""
        if not news_list:
            news_list = await get_news_list()
        for i in range(min(5, len(news_list))):
            msg += f"【{i + 1}】{news_list[i]['time']} {news_list[i]['title']} {news_list[i]['link']} \n"
        message_queue.put((Message(msg), event, bot))
        logger.debug(f"进入队列：{msg}")
        logger.info(f"用户：{event.user_id}，在群：{event.group_id}，使用了教务处通知推送")
        await Jwc_message.finish()


@scheduler.scheduled_job("interval", seconds=60, id="get_news_list")
async def check_update():
    global news_list
    fetched_news = await get_news_list()
    if not news_list:
        news_list = fetched_news
        return
    if not fetched_news:
        return
    for news in news_list:
        if not _url_match(news, news_list):
            news_list.append(news)
            logger.info(f"检测到通知：{news['title']}")
            news_msg = f"{news['title']}\n{news['description']}\n{news['link']}"
            bot = get_bot()
            for group in PREVIEW_GROUP:
                message_queue.put((Message(news_msg), group, bot, "group"))
                logger.debug(f"进入群发队列：{news_msg}")
                logger.info(f"群{group}，自动发送教务处通知推送")


def _url_match(new: dict, cache: list) -> bool:
    url_cache = [i['link'] for i in cache]
    if new['link'] in url_cache:
        return True
    else:
        return False


async def get_news_list() -> List[Dict[str, str]]:
    try:
        fetched_news = []
        for url in jwc_news_url:
            async with httpx.AsyncClient() as client:
                r = await client.get(url=url)
            soup = BeautifulSoup(r, 'lxml')
            # print(soup)
            items_list = soup.body.find(class_='Newslist').find_all(name='div', attrs={"class": "wz"})
            times_list = soup.body.find(class_='Newslist').find_all(name='div', attrs={"class": "sj"})
            for item, time in zip(items_list, times_list):
                link = str(item.find('a', href=True)['href'])
                link = link.replace('..', 'https://jwc.sjtu.edu.cn')
                title = str(item.a.h2.contents[0])
                description = str(item.p.contents[0])
                month = str(time.p.contents[0])
                day = str(time.h2.contents[0])
                time_str = month.replace('.', '-') + '-' + day
                fetched_news.append({"title": title, "link": link, "description": description, 'time': time_str})
        fetched_news = [i for n, i in enumerate(fetched_news) if i not in fetched_news[n + 1:]]
        fetched_news.sort(key=lambda x: x["time"], reverse=True)
        logger.debug(f"Successfully fetched {len(fetched_news)} news.")
        return fetched_news
    except Exception as e:
        logger.error("获取教务处新闻列表失败，错误信息：", e)
