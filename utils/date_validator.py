# utils/date_validator.py
from datetime import datetime
from config.config import DATE_FORMAT
from utils.logger import logger


def validate_date_format(date_str: str) -> bool:
    """
    验证日期格式是否正确
    
    :param date_str: 日期字符串，应为 "年-月-日" 格式
    :return: 格式正确返回 True，否则返回 False
    """
    try:
        datetime.strptime(date_str, DATE_FORMAT)
        return True
    except ValueError:
        logger.error(f"日期格式错误: {date_str}，应为 {DATE_FORMAT} 格式")
        return False


def validate_date_range(start_date: str, end_date: str) -> bool:
    """
    验证日期范围是否合法
    
    :param start_date: 开始日期
    :param end_date: 结束日期
    :return: 合法返回 True，否则返回 False
    """
    if not validate_date_format(start_date) or not validate_date_format(end_date):
        return False
    
    start = datetime.strptime(start_date, DATE_FORMAT)
    end = datetime.strptime(end_date, DATE_FORMAT)
    
    if start > end:
        logger.error(f"开始日期 {start_date} 不能晚于结束日期 {end_date}")
        return False
    
    return True
