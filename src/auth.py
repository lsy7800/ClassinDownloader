# src/auth.py
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from config.config import CLASSIN_USERNAME, CLASSIN_PASSWORD
from utils.logger import logger
from utils.cookies import CookieManager


class LoginManager:
    def __init__(self, driver: WebDriver, cookie_manager: CookieManager):
        self.driver = driver
        self.cookie_manager = cookie_manager

    def login(self) -> bool:
        logger.info("开始登录 ClassIn")
        # 先清理旧的 cookies
        self.cookie_manager.clear(self.driver)
        self.driver.get("https://www.eeo.cn/cn/login")
        time.sleep(5)
        try:
            username_input = self.driver.find_element(By.ID, "accountInput")
            password_input = self.driver.find_element(By.XPATH, "//input[@type='password']")
            checkbox = self.driver.find_element(By.CSS_SELECTOR, ".agreement-wrap input.el-checkbox__original")
            submit_btn = self.driver.find_element(By.CLASS_NAME, "submit-btn")
        except Exception as e:
            logger.error("未找到登录表单元素: {}", e)
            return False

        username_input.clear()
        username_input.send_keys(CLASSIN_USERNAME)

        password_input.clear()
        password_input.send_keys(CLASSIN_PASSWORD)

        self.driver.execute_script("arguments[0].click();", checkbox)

        submit_btn.click()
        time.sleep(15)

        if self._check_login_success():
            logger.info("登录成功，保存 cookies")
            self.cookie_manager.save(self.driver)
            return True
        else:
            logger.error("登录失败，请检查账号密码或验证码")
            return False

    def _check_login_success(self) -> bool:
        current_url = self.driver.current_url
        return "login" not in current_url
