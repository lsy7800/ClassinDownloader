# utils/browser.py
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from config.config import (
    CHROME_DRIVER_PATH,
    PAGE_LOAD_TIMEOUT,
    IMPLICIT_WAIT,
)
from utils.logger import logger


class Browser:
    def __init__(self, headless: bool = False):
        self.headless = headless
        self.driver = self._create_driver()

    def _create_driver(self) -> webdriver.Chrome:
        options = Options()

        if self.headless:
            options.add_argument("--headless=new")

        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--start-maximized")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        if CHROME_DRIVER_PATH:
            service = Service(CHROME_DRIVER_PATH)
            driver = webdriver.Chrome(service=service, options=options)
        else:
            driver = webdriver.Chrome(options=options)

        driver.set_page_load_timeout(PAGE_LOAD_TIMEOUT)
        driver.implicitly_wait(IMPLICIT_WAIT)

        logger.info("Chrome 浏览器已启动 (headless={})", self.headless)
        return driver

    def quit(self):
        if self.driver:
            logger.info("关闭浏览器")
            self.driver.quit()
