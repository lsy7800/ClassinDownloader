# utils/cookies.py
import json
from pathlib import Path
from selenium.webdriver.remote.webdriver import WebDriver

from config.config import COOKIE_FILE
from utils.logger import logger

class CookieManager:
    def __init__(self, cookie_file: Path = COOKIE_FILE):
        self.cookie_file = cookie_file

    def save(self, driver: WebDriver) -> None:
        """
        从 selenium driver 中读取 cookies 并保存到文件
        """
        cookies = driver.get_cookies()

        if not cookies:
            logger.warning("未获取到任何 cookies，跳过保存")
            return

        self.cookie_file.parent.mkdir(exist_ok=True)

        try:
            with open(self.cookie_file, "w", encoding="utf-8") as f:
                json.dump(cookies, f, ensure_ascii=False, indent=2)
            logger.info("cookies 已保存，共 {} 条", len(cookies))
        except Exception as e:
            logger.error("保存 cookies 失败: {}", e)


    def load(self, driver: WebDriver, domain: str) -> bool:
        """
        将 cookies 文件注入到 selenium driver

        :param domain: 如 https://www.eeo.cn/
        """
        if not self.cookie_file.exists():
            logger.info("cookies 文件不存在")
            return False

        try:
            with open(self.cookie_file, "r", encoding="utf-8") as f:
                cookies = json.load(f)
        except Exception as e:
            logger.error("读取 cookies 文件失败: {}", e)
            return False

        driver.get(domain)

        success_count = 0
        for cookie in cookies:
            cookie.pop("sameSite", None)
            try:
                driver.add_cookie(cookie)
                success_count += 1
            except Exception as e:
                logger.debug(
                    "注入 cookie 失败: {} -> {}",
                    cookie.get("name"),
                    e
                )

        logger.info(
            "cookies 加载完成，成功 {} / {}",
            success_count,
            len(cookies)
        )
        return success_count > 0

    def clear(self, driver):
        """
        清空浏览器中的 cookies，并删除本地 cookies 文件
        """
        logger.warning("清理旧 cookies")

        try:
            driver.delete_all_cookies()
        except Exception as e:
            logger.debug("浏览器 cookies 清理失败: {}", e)

        if self.cookie_file.exists():
            try:
                self.cookie_file.unlink()
                logger.info("本地 cookies 文件已删除")
            except Exception as e:
                logger.error("删除 cookies 文件失败: {}", e)

    def to_requests_cookies(self) -> dict:
        """
        将本地 cookies 转换为 requests 可用的 cookies dict
        """
        if not self.cookie_file.exists():
            logger.warning("cookies 文件不存在，无法转换")
            return {}

        try:
            with open(self.cookie_file, "r", encoding="utf-8") as f:
                cookies = json.load(f)
        except Exception as e:
            logger.error("读取 cookies 文件失败: {}", e)
            return {}

        return {c["name"]: c["value"] for c in cookies}
