# utils/logger.py
from loguru import logger
import sys
from pathlib import Path

from config.config import BASE_DIR

# =========================
# 日志目录
# =========================
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)

LOG_FILE = LOG_DIR / "classin.log"

# =========================
# 移除 loguru 默认配置
# =========================
logger.remove()

# =========================
# 控制台日志
# =========================
logger.add(
    sys.stdout,
    level="INFO",
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
           "<level>{level}</level> | "
           "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
           "<level>{message}</level>",
)

# =========================
# 文件日志
# =========================
logger.add(
    LOG_FILE,
    level="DEBUG",
    encoding="utf-8",
    rotation="10 MB",
    retention="7 days",
    compression="zip",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} - {message}",
)

__all__ = ["logger"]
