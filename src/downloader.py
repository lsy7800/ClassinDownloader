from tqdm import tqdm
import requests
from pathlib import Path
from tenacity import retry, stop_after_attempt, wait_fixed, before_sleep_log
import logging

from utils.logger import logger
from config.config import DOWNLOAD_DIR
from utils.cookies import CookieManager


class Downloader:
    def __init__(self, cookie_manager: CookieManager, download_dir: Path = DOWNLOAD_DIR):
        self.download_dir = download_dir
        self.download_dir.mkdir(exist_ok=True)
        self.cookie_manager = cookie_manager

        self.session = requests.Session()
        self.session.cookies.update(self.cookie_manager.to_requests_cookies())

    @retry(
        stop=stop_after_attempt(3),  # 最多重试3次
        wait=wait_fixed(2),  # 每次重试间隔2秒
        before_sleep=before_sleep_log(logging.getLogger(__name__), logging.WARNING),  # 重试前记录日志
        reraise=True  # 最终失败时抛出异常
    )
    def _do_download(self, url: str, save_path: Path, filename: str) -> None:
        """实际的下载逻辑（带重试机制）"""
        # 清理可能存在的残留文件
        if save_path.exists():
            save_path.unlink()
            logger.debug("清理残留文件: {}", save_path)

        with self.session.get(url, stream=True, timeout=30) as r:
            r.raise_for_status()

            total_size = int(r.headers.get("Content-Length", 0))
            chunk_size = 8192

            with open(save_path, "wb") as f, tqdm(
                total=total_size,
                unit="B",
                unit_scale=True,
                desc=filename,
            ) as bar:
                for chunk in r.iter_content(chunk_size=chunk_size):
                    if chunk:
                        f.write(chunk)
                        bar.update(len(chunk))

    def download(self, url: str, filename: str, subdirectory: str = None) -> Path | None:
        """下载文件，失败后自动重试最多3次"""
        # 如果指定了子文件夹，则在 download_dir 下创建该文件夹
        if subdirectory:
            save_dir = self.download_dir / subdirectory
            save_dir.mkdir(exist_ok=True)
        else:
            save_dir = self.download_dir
        
        save_path = save_dir / filename

        logger.info("开始下载: {}", filename)

        try:
            self._do_download(url, save_path, filename)
            logger.info("下载完成: {}", save_path)
            return save_path

        except Exception as e:
            logger.error("下载最终失败 (已重试3次): {}, 错误: {}", filename, e)
            # 清理失败的文件
            if save_path.exists():
                save_path.unlink()
            return None


if __name__ == "__main__":
    cookie = CookieManager()
    downloader = Downloader(cookie)
    video_href = "https://playback.eeo.cn/794b4a11vodbj1252412222/040a79705145403714463441300/f0.mp4"
    downloader.download(url=video_href, filename="video-1.mp4")