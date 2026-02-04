# main.py
import time
from utils.browser import Browser
from utils.cookies import CookieManager
from utils.logger import logger
from src.auth import LoginManager
from src.spider import Spider
from src.downloader import Downloader

def main():
    logger.info("程序启动")

    # 1. 启动浏览器
    browser = Browser(headless=False)
    driver = browser.driver

    # 2. 初始化 cookies 管理器
    cookie_manager = CookieManager()

    # 3. 尝试加载 cookies
    if cookie_manager.load(driver, "https://www.eeo.cn/cn"):
        logger.info("cookies 已加载，验证登录状态")
        driver.get("https://www.eeo.cn/cn")
        time.sleep(2)

        if "login" in driver.current_url:
            logger.warning("cookies 已过期，重新登录")
            login_manager = LoginManager(driver, cookie_manager)
            login_manager.login()
    else:
        login_manager = LoginManager(driver, cookie_manager)
        login_manager.login()

    # 4. 关闭浏览器
    browser.quit()

    # ===== spider =====
    logger.info("登录流程完成，开始构建信息")

    # 初始化spider
    spider = Spider(cookie_manager)
    # 初始化downloader
    downloader = Downloader(cookie_manager)
    try:
        start = input("请输入起始时间：")
        end = input("请输入结束时间：")
        res = spider.get_courses_by_api(1, per_page=100, start_time=start, end_time=end)
        for course in res:
            logger.info(course)
            course_id = course["courseId"]
            class_id = course["id"]
            url_list = spider.get_video(course_id, class_id)
            for index, url in enumerate(url_list):
                logger.info(url)
                class_name = course["className"].replace(" ", "") + "-" + str(index+1) + ".mp4"
                logger.info(class_name)
                downloader.download(url, class_name)
    except Exception as e:
        logger.error(e)

    logger.info("程序结束")


if __name__ == "__main__":
    main()
