from datetime import datetime
from nonebot import on_message
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import GROUP, Bot, MessageEvent
from nonebot.log import logger
from utils import db

MessageStorage = on_message(permission=GROUP,
                            priority=3,
                            block=False
                            )


@MessageStorage.handle()
async def handle_receive(bot: Bot, event: MessageEvent, state: T_State):
    time = event.time
    user_id = event.user_id
    group_id = event.group_id
    message = event.raw_message
    msg_id = event.message_id
    logger.debug(f"time: {time}, user_id: {user_id}, group_id: {group_id}, message: {message}, msg_id: {msg_id}")
    if not db.table_exists(f"msg{group_id}"):
        db.create_table(f"""CREATE TABLE msg{group_id}(
        time DATETIME, 
        user_id INT, 
        message TEXT,
        msg_id INT
        );""")
    db.insert(f"""INSERT INTO msg{group_id} (time, user_id, message, msg_id) VALUES (?, ?, ?, ?)""",
              (datetime.fromtimestamp(time), user_id, message, msg_id))
    await MessageStorage.finish()
