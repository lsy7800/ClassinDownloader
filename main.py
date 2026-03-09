# main.py
import sys
import time
from utils.browser import Browser
from utils.cookies import CookieManager
from utils.logger import logger
from utils.date_validator import validate_date_format, validate_date_range
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
    try:
        if cookie_manager.load(driver, "https://www.eeo.cn/cn"):
            logger.info("cookies 已加载，检查是否过期")
            
            # 先检查 cookies 文件中是否有过期的 cookie
            if cookie_manager.is_cookie_expired():
                logger.warning("cookies 已过期，清除并重新登录")
                login_manager = LoginManager(driver, cookie_manager)
                if not login_manager.login(clear_old_cookies=True):
                    logger.error("登录失败，程序退出")
                    browser.quit()
                    sys.exit(1)
            else:
                # cookies 未过期，验证登录状态
                driver.get("https://www.eeo.cn/cn")
                time.sleep(2)

                if "login" in driver.current_url:
                    logger.warning("cookies 验证失败（URL 包含 login），重新登录")
                    login_manager = LoginManager(driver, cookie_manager)
                    if not login_manager.login(clear_old_cookies=True):
                        logger.error("登录失败，程序退出")
                        browser.quit()
                        sys.exit(1)
                else:
                    logger.info("cookies 验证成功，可以继续使用")
        else:
            logger.info("cookies 文件不存在，需要重新登录")
            login_manager = LoginManager(driver, cookie_manager)
            if not login_manager.login(clear_old_cookies=False):
                logger.error("登录失败，程序退出")
                browser.quit()
                sys.exit(1)
    except Exception as e:
        logger.error("登录过程异常: {}", e)
        browser.quit()
        sys.exit(1)

    # 4. 关闭浏览器
    browser.quit()

    # ===== spider =====
    logger.info("登录流程完成，开始构建信息")

    # 初始化spider
    spider = Spider(cookie_manager)
    # 初始化downloader
    downloader = Downloader(cookie_manager)
    
    try:
        # 显示菜单
        while True:
            print("\n" + "="*50)
            print("请选择查询方式:")
            print("1. 下载单日课程")
            print("2. 下载多日课程")
            print("="*50)
            
            choice = input("请输入选项 (1 或 2): ").strip()
            
            if choice == "1":
                # 单日课程
                while True:
                    date = input("请输入日期 (格式: 年-月-日，如 2025-03-09): ").strip()
                    if validate_date_format(date):
                        logger.info(f"开始获取 {date} 的课程")
                        res = spider.get_courses_by_single_day(date)
                        break
                    else:
                        print("日期格式错误，请重新输入")
                
                if not res:
                    logger.warning(f"{date} 没有课程")
                    continue
                
                logger.info(f"获取到 {len(res)} 条课程")
                break
            
            elif choice == "2":
                # 多日课程
                while True:
                    start_date = input("请输入开始日期 (格式: 年-月-日，如 2025-03-09): ").strip()
                    end_date = input("请输入结束日期 (格式: 年-月-日，如 2025-03-15): ").strip()
                    
                    if validate_date_range(start_date, end_date):
                        logger.info(f"开始获取 {start_date} 到 {end_date} 的课程")
                        res = spider.get_courses_by_date_range(start_date, end_date)
                        break
                    else:
                        print("日期格式或范围错误，请重新输入")
                
                if not res:
                    logger.warning(f"{start_date} 到 {end_date} 没有课程")
                    continue
                
                logger.info(f"获取到 {len(res)} 条课程")
                break
            
            else:
                print("选项错误，请输入 1 或 2")
        
        # 下载课程
        for course in res:
            logger.info(course)
            course_id = course["courseId"]
            class_id = course["id"]
            # 提取课程文件夹名称
            course_folder_name = course["className"].split(" ")[0]
            
            url_list = spider.get_video(course_id, class_id)
            for index, url in enumerate(url_list):
                logger.info(url)
                class_name = course["className"].replace(" ", "") + "-" + str(index+1) + ".mp4"
                logger.info(class_name)
                # 传入子文件夹名称
                downloader.download(url, class_name, subdirectory=course_folder_name)
    except Exception as e:
        logger.error(e)

    logger.info("程序结束")


if __name__ == "__main__":
    main()
