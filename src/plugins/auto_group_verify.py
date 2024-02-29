import re
from datetime import datetime
from typing import List, Tuple

import pandas as pd
from nonebot import on_request, get_driver
from nonebot.adapters.onebot.v11 import Bot, Event
from nonebot.log import logger
from nonebot.typing import T_State
from configs.path_config import DATABASE_PATH, TEXT_PATH
from utils import SQLiteDB, request_queue
from utils.permission_checker import auth_manager

__plugin_name__ = "自动加群验证"
__plugin_usage__ = f"""验证信息为“<姓名> <学号>”，如果信息匹配，即可自动入群"""
__plugin_cmd_name__ = "verify"
__command_description__ = "自助加群验证"
__default_permission__ = True

AutoVerify = on_request(
    rule=auth_manager.get_rule(f"{__plugin_cmd_name__}"),
    priority=7,
    block=False,
)

MODE_PASS = 1
MODE_FAIL = 2
MODE_WAIT = 3

driver = get_driver()

stu_db = SQLiteDB(DATABASE_PATH + "identify.db")
add_group_result = SQLiteDB(DATABASE_PATH + "identify_result.db")
stu_csv_path = TEXT_PATH + '/verify/example.csv'


@AutoVerify.handle()
async def handle_receive(bot: Bot, event: Event, state: T_State):
    if hasattr(event, "request_type"):
        if event.request_type == "friend":
            pass
        elif event.request_type == "group":
            logger.info(f"收到加群请求: {event}")
            if hasattr(event, "comment"):
                request_msg = str(event.comment).split("\n答案：")[1]
                group_id = event.group_id
                user_id = event.user_id
                logger.debug(f"收到加群请求: {event}")
                verify_result, stu_id, name = await verify_user(request_msg)
                if verify_result == MODE_PASS:
                    logger.info(f"{user_id}加群{group_id}验证通过，同意入群")
                    await add_result_to_db(group_id,
                                           user_id,
                                           stu_id,
                                           name,
                                           "通过",
                                           event.time)
                    # await bot.set_group_add_request(flag=event.flag, sub_type=event.sub_type, approve=True)
                    request_queue.put((bot, event.flag, event.sub_type, True, "验证通过"))
                elif verify_result == MODE_FAIL:
                    logger.info(f"{user_id}加群{group_id}验证失败，拒绝入群")
                    await add_result_to_db(group_id,
                                           user_id,
                                           stu_id,
                                           name,
                                           "拒绝",
                                           event.time)
                    # await bot.set_group_add_request(flag=event.flag, sub_type=event.sub_type, approve=False,
                    #                                 reason="验证失败")
                    request_queue.put((bot, event.flag, event.sub_type, False, "验证失败"))
                elif verify_result == MODE_WAIT:
                    logger.info(f"{user_id}加群{group_id}验证等待中")
                    await add_result_to_db(group_id,
                                           user_id,
                                           stu_id,
                                           name,
                                           "未定",
                                           event.time)
                await AutoVerify.finish()
            else:
                logger.warning(f"没有comment: {event}")
                await AutoVerify.finish()


async def verify_user(comment: str) -> Tuple[int, str, str]:
    logger.debug(f"验证信息: {comment}")
    comment_id = re.findall(r'\d{6,}', comment)[0]
    if comment:
        logger.debug(f"学号: {comment_id}")
        check_result = stu_db.query(f"""SELECT * FROM example_table WHERE stuid = '{comment_id}'""")
        logger.debug(f"查询结果: {check_result}")
        if check_result:
            if check_result[0][1] in comment:
                return MODE_PASS, comment_id, check_result[0][1]
            else:
                return MODE_FAIL, comment_id, check_result[0][1]
        else:
            return MODE_WAIT, comment_id, 'None'
    else:
        return MODE_FAIL, 'FAIL', comment


@driver.on_startup
async def get_name_id():
    stu_db.connect()
    add_group_result.connect()
    logger.info("身份数据库已连接")
    try:
        excel_data = pd.read_csv(stu_csv_path, encoding='utf-8', dtype=str)
    except Exception as e:
        logger.error(f"读取csv文件失败，错误信息：{e}")
        return
    excel_data.to_sql('example_table', stu_db.get_conn(), if_exists='replace', index=False)
    add_group_result.create_table(f"""CREATE TABLE IF NOT EXISTS add_group_result(
                                        group_id INT,
                                        user_id INT,
                                        stu_id TEXT,
                                        name TEXT,
                                        result TEXT,
                                        time DATETIME
                                        );""")
    logger.info("身份数据库已初始化")


async def add_result_to_db(group_id: int, user_id: int, stu_id: str, name: str, result: str, time: int):
    add_group_result.insert(
        f"""INSERT INTO add_group_result (group_id, user_id, stu_id, name, result, time) VALUES (?, ?, ?, ?, ?, ?)""",
        (group_id, user_id, stu_id, name, result, datetime.fromtimestamp(time)))


@driver.on_shutdown
async def get_name_id():
    stu_db.close()
    logger.info("身份数据库已关闭")
