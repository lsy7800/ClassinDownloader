# config/config.py
from pathlib import Path

# =========================
# 项目根目录
# =========================
BASE_DIR = Path(__file__).resolve().parent.parent


# =========================
# ClassIn 账号信息
# ⚠️ 建议后续改为环境变量
# =========================
CLASSIN_USERNAME = "15620939846"
CLASSIN_PASSWORD = "jay13403630587"


# =========================
# 路径配置
# =========================
DATA_DIR = BASE_DIR / "data"
COOKIE_FILE = DATA_DIR / "cookies.json"
DOWNLOAD_DIR = DATA_DIR / "videos"


# =========================
# 浏览器 & 爬虫配置
# =========================
CHROME_DRIVER_PATH = None  # 如果已加入 PATH，可保持 None
PAGE_LOAD_TIMEOUT = 30
IMPLICIT_WAIT = 10


# =========================
# 课程筛选相关
# =========================
DATE_FORMAT = "%Y-%m-%d"

# =========================
# 课程接口地址
COURSE_DATA_API = "https://dynamic.eeo.cn/saasajax/course.ajax.php"
# =========================

# =========================
# 学校接口地址
# =========================
SCHOOL_DATA_API = "https://dynamic.eeo.cn/saasajax/school.ajax.php"