# src/spider.py
from datetime import datetime, timedelta
import json
import requests
from utils.cookies import CookieManager
from utils.logger import logger
from config.config import COURSE_DATA_API, SCHOOL_DATA_API, DATE_FORMAT


class Spider:
    def __init__(self, cookie_manager: CookieManager):
        self.cookie_manager = cookie_manager
        self.session = requests.Session()
        self.session.cookies.update(cookie_manager.to_requests_cookies())
        self.courses_api = COURSE_DATA_API
        self.school_api = SCHOOL_DATA_API

    def get_courses_by_api(self, page: int=1, per_page:int=20, start_time: str = "2025-12-30",
                           end_time: str = datetime.today().strftime(DATE_FORMAT)) -> list[dict]:
        logger.info("访问api 获取到课程信息")
        f_start_time = int(datetime.strptime(start_time, DATE_FORMAT).timestamp())
        f_end_time = int(datetime.strptime(end_time, DATE_FORMAT).timestamp())
        logger.info(f"起始日期: {f_start_time}, 结束时间: {f_end_time}")
        data = {
            "withAuth": 1,
            "classStatus": 3,
            "page": page,
            "perpage": per_page,
            "timeRange": json.dumps({
                "startTime": f_start_time,
                "endTime": f_end_time
            }),
            "sort":json.dumps({
                "sortName": "classBtime",
                "sortValue": 2
            })
        }
        result = self.session.post(self.courses_api, data=data, params={"action": "getClassListNew"})
        courses_content = json.loads(result.text)
        logger.info(f"当前课程总数：{courses_content.get("data").get("totalClassNum")}")
        return courses_content.get("data").get("classList")


    def get_video(self, course_id:int, class_id: int, page: int=1, per_page: int=100):
        """根据id获取到视频地址数据"""
        logger.info(f"开始获取视频地址:{course_id}-{class_id}")
        data = {
            "courseId": course_id,
            "classId": class_id,
            "page": page,
            "perpage": per_page,
        }

        result = self.session.post(self.school_api, data=data, params={'action': 'getClassVodList'})
        video_content = json.loads(result.content.decode("utf-8-sig"))
        video_infos = video_content.get("data").get("VodInfo").get("FileList")
        video_list = []
        for video_info in video_infos:
            video_list.append(video_info.get("Playset")[0].get("Url"))
        return video_list

    def get_courses_by_single_day(self, date: str) -> list[dict]:
        """
        获取某一天的所有课程（处理分页）
        
        :param date: 日期，格式为 "年-月-日"，如 "2025-03-09"
        :return: 该天的所有课程列表
        """
        logger.info(f"开始获取 {date} 的课程")
        
        # 将日期转换为该天的时间戳范围
        day_start = int(datetime.strptime(date, DATE_FORMAT).timestamp())
        day_end = day_start + 86400 - 1  # 该天的最后一秒
        
        all_courses = []
        page = 1
        
        while True:
            logger.info(f"获取 {date} 第 {page} 页的课程")
            data = {
                "withAuth": 1,
                "classStatus": 3,
                "page": page,
                "perpage": 100,
                "timeRange": json.dumps({
                    "startTime": day_start,
                    "endTime": day_end
                }),
                "sort": json.dumps({
                    "sortName": "classBtime",
                    "sortValue": 2
                })
            }
            
            try:
                result = self.session.post(self.courses_api, data=data, params={"action": "getClassListNew"})
                courses_content = json.loads(result.text)
                courses = courses_content.get("data", {}).get("classList", [])
                
                if not courses:
                    logger.info(f"{date} 已获取全部课程，共 {len(all_courses)} 条")
                    break
                
                all_courses.extend(courses)
                logger.info(f"{date} 第 {page} 页获取 {len(courses)} 条课程")
                
                # 如果返回的课程数少于100条，说明已经是最后一页
                if len(courses) < 100:
                    break
                
                page += 1
            except Exception as e:
                logger.error(f"获取 {date} 第 {page} 页课程失败: {e}")
                break
        
        return all_courses

    def get_courses_by_date_range(self, start_date: str, end_date: str) -> list[dict]:
        """
        获取时间段内每一天的所有课程
        
        :param start_date: 开始日期，格式为 "年-月-日"，如 "2025-03-09"
        :param end_date: 结束日期，格式为 "年-月-日"，如 "2025-03-15"
        :return: 时间段内的所有课程列表
        """
        logger.info(f"开始获取 {start_date} 到 {end_date} 的课程")
        
        all_courses = []
        current_date = datetime.strptime(start_date, DATE_FORMAT)
        end_datetime = datetime.strptime(end_date, DATE_FORMAT)
        
        while current_date <= end_datetime:
            date_str = current_date.strftime(DATE_FORMAT)
            courses = self.get_courses_by_single_day(date_str)
            all_courses.extend(courses)
            current_date += timedelta(days=1)
        
        logger.info(f"共获取 {len(all_courses)} 条课程")
        return all_courses

