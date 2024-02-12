from typing import List, Union

OWNER: str = ""  # 主人

BOT_NAME: str = "咕咕"  # 机器人名称
SELF_DEBUG_MODE = True

# 日志记录时长
DEBUG_LOG_TIME: int = 5  # 调试日志记录时长，单位天
INFO_LOG_TIME: int = 60  # 普通日志记录时长，单位天
ERROR_LOG_TIME: int = 90  # 错误日志记录时长，单位天
WARNING_LOG_TIME: int = 180  # 警告日志记录时长，单位天

PREVIEW_GROUP: List[int] = [632894117, 801212936]  # 预览群
SUPERUSERS: List[Union[int, str]] = [1299946476]  # 超级用户名单

HTTP_API_URL: str = "http://127.0.0.1:5700"  # HTTP API URL