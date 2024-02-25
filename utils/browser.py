from typing import Optional
from nonebot import get_driver

from nonebot import logger
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import WebDriver
from webdriver_manager.chrome import ChromeDriverManager

driver = get_driver()

_browser: Optional[WebDriver] = None


@driver.on_startup
async def start_browser():
    logger.info("准备初始化selenium")
    global _browser
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # 无头模式，没有界面打开浏览器
    options.add_argument('--disable-gpu')  # 禁用GPU加速，某些情况下需要
    _browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    logger.info("selenium已初始化")


@driver.on_shutdown
async def shutdown_browser():
    if _browser:
        _browser.quit()
        logger.info("selenium已关闭")


def get_browser() -> WebDriver:
    if not _browser:
        logger.error("selenium is not initalized")
        raise RuntimeError("selenium is not initalized")

    return _browser
