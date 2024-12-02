from pathlib import Path

# 图片路径
IMAGE_PATH = Path("src/resource/img/")
# 音频路径
VOICE_PATH = Path("src/resource/voice/")
# 文本路径
TEXT_PATH = Path("src/resource/text/")
# 模板路径
TEMPLATE_PATH = Path("src/resource/templates")
# 字体路径
FONT_PATH = Path("src/resource/fonts/")
# 日志路径
LOG_PATH = Path("log/")
# 临时图片路径
TEMP_PATH = Path("temp/")
# 权限文件路径
PERMISSION_PATH = Path("configs/permission.json")
# 数据库路径
DATABASE_PATH = Path("database/")


def init_path():
    global IMAGE_PATH, VOICE_PATH, TEXT_PATH, LOG_PATH, FONT_PATH, TEMP_PATH, TEMPLATE_PATH, PERMISSION_PATH, DATABASE_PATH
    IMAGE_PATH.mkdir(parents=True, exist_ok=True)  # type: ignore
    VOICE_PATH.mkdir(parents=True, exist_ok=True)  # type: ignore
    TEXT_PATH.mkdir(parents=True, exist_ok=True)  # type: ignore
    TEMPLATE_PATH.mkdir(parents=True, exist_ok=True)  # type: ignore
    FONT_PATH.mkdir(parents=True, exist_ok=True)  # type: ignore
    LOG_PATH.mkdir(parents=True, exist_ok=True)  # type: ignore
    TEMP_PATH.mkdir(parents=True, exist_ok=True)  # type: ignore
    PERMISSION_PATH.touch(exist_ok=True)  # type: ignore
    DATABASE_PATH.mkdir(parents=True, exist_ok=True)  # type: ignore

    IMAGE_PATH = str(IMAGE_PATH.absolute()) + "/"  # type: ignore
    VOICE_PATH = str(VOICE_PATH.absolute()) + "/"  # type: ignore
    TEXT_PATH = str(TEXT_PATH.absolute()) + "/"  # type: ignore
    TEMPLATE_PATH = str(TEMPLATE_PATH.absolute()) + "\\"  # type: ignore
    FONT_PATH = str(FONT_PATH.absolute()) + "/"  # type: ignore
    LOG_PATH = str(LOG_PATH.absolute()) + "/"  # type: ignore
    TEMP_PATH = str(TEMP_PATH.absolute()) + "\\"  # type: ignore
    DATABASE_PATH = str(DATABASE_PATH.absolute()) + "/"  # type: ignore


init_path()
