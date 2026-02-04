# src/spider.py
from datetime import datetime
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

