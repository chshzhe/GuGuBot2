import os
import requests
import ujson
from io import BytesIO
from typing import Union, Optional, List
from jinja2 import Environment, FileSystemLoader
import urllib.parse
from nonebot import logger
from nonebot.adapters.onebot.v11.message import MessageSegment
from configs.path_config import IMAGE_PATH, VOICE_PATH, TEMPLATE_PATH, TEMP_PATH
from configs.config import HTTP_API_URL
from utils.browser import get_browser

endpoint_upload = '/upload_file'
endpoint_download = '/download_file'


def image(
        img_file: str = None,
        path: str = "",
        abspath: Optional[str] = None,
        c: Optional[Union[str, bytes, BytesIO]] = None,
) -> MessageSegment:
    if abspath:
        if os.path.exists(abspath):
            return MessageSegment.image("file:///" + abspath)
        else:
            return text("")
    elif c:
        if isinstance(c, str):
            if c.find("base64://") != -1:
                return MessageSegment.image(c)
            else:
                return MessageSegment.image("base64://" + c)
        else:
            return MessageSegment.image(c)
    else:
        img_file = str(img_file)
        if img_file.find("http") == -1:
            if len(img_file.split(".")) == 1:
                img_file += ".jpg"
            if os.path.exists(IMAGE_PATH + path + "/" + img_file):
                return MessageSegment.image(
                    "file:///" + IMAGE_PATH + path + "/" + img_file
                )
            else:
                logger.warning(f"图片 {path}/{img_file} 不存在")
                return text("")
        else:
            return MessageSegment.image(img_file)


def at(qq: Union[int, str]) -> MessageSegment:
    return MessageSegment.at(qq)


def record(voice_name: str = "", path: Optional[str] = "") -> MessageSegment:
    if len(voice_name.split(".")) == 1:
        voice_name += ".mp3"
    if path == "":
        name = VOICE_PATH + "{}.".format(voice_name)
    else:
        name = VOICE_PATH + "{}/{}".format(path, voice_name)
    if voice_name.find("http") == -1:
        if os.path.exists(name):
            result = MessageSegment.record("file:///" + name)
            return result
        else:
            logger.warning(f"语音{path}/{voice_name} 不存在")
            return text("")
    else:
        return MessageSegment.record(voice_name)


def text(msg: str) -> MessageSegment:
    return MessageSegment.text(msg)


def contact_user(qq: int) -> MessageSegment:
    return MessageSegment.contact_user(qq)


def share(
        url: str = "",
        title: str = "",
        content: Optional[str] = None,
        image_url: Optional[str] = None,
) -> MessageSegment:
    return MessageSegment.share(url, title, content, image_url)


def xml(data: str) -> MessageSegment:
    return MessageSegment.xml(data)


def json(data: str) -> MessageSegment:
    data = ujson.dumps(data)
    return MessageSegment.json(data)


def face(id_: int) -> MessageSegment:
    return MessageSegment.face(id_)


def poke(id_: str) -> MessageSegment:
    return MessageSegment.poke("", id_)


def music_163(id_: int) -> MessageSegment:
    return MessageSegment("music", {"type": "163", "id": id_})


def reply(id_: int) -> MessageSegment:
    return MessageSegment.reply(id_)


# async def upload_for_shamrock(path: str, filename: str) -> Union[MessageSegment, None]:
#     if os.path.exists(path + filename):
#         try:
#             with open(path + filename, 'rb') as f:
#                 response = requests.post(HTTP_API_URL + endpoint_upload, files={'file': f}).json()
#             if response['status'] == 'ok':
#                 temp_name = response['data']['file']
#                 md5 = response['data']['md5']
#                 logger.info(f"图片{filename}上传缓存成功，返回的文件名为{md5}")
#                 return MessageSegment.image("file://" + temp_name)
#             else:
#                 logger.error(f"图片上传缓存失败，返回的信息为{response}")
#                 return None
#         except Exception as e:
#             logger.error(f"图片上传缓存失败，错误信息为{e}")
#             return None
#     else:
#         logger.warning(f"图片{filename}不存在")
#         return None


async def template_to_image(
        template_name: str,
        img_name: str,
        **kwargs
) -> None:
    try:
        env = Environment(loader=FileSystemLoader(TEMPLATE_PATH))
        template = env.get_template(f"{template_name}.html")
        html_str = template.render(kwargs)
        with open(f'{TEMPLATE_PATH}{template_name}.css', 'r', encoding='utf-8') as f:
            css_str = f.read()
        html_with_css = f"<html>\n<style>\n{css_str}\n</style>\n{html_str}\n"
        browser = get_browser()
        encoded_html = urllib.parse.quote(html_with_css)
        data_url = f"data:text/html;charset=utf-8,{encoded_html}"
        browser.get(data_url)
        width = browser.execute_script("return document.body.scrollWidth")
        height = browser.execute_script("return document.body.scrollHeight")
        logger.debug(f"页面width: {width}, height: {height}")
        browser.set_window_size(840, height)
        browser.save_screenshot(f"{TEMP_PATH}{img_name}.png")
        logger.info(f"模板{template_name}生成图片{img_name}成功")
    except Exception as e:
        logger.error(f"模板{template_name}生成图片{img_name}失败，错误信息为{e}")
