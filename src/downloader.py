from tqdm import tqdm
import requests
from pathlib import Path

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

    def download(self, url: str, filename: str) -> Path | None:
        save_path = self.download_dir / filename

        logger.info("开始下载: {}", filename)

        try:
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

            logger.info("下载完成: {}", save_path)
            return save_path

        except Exception as e:
            logger.error("下载失败 {}: {}", filename, e)
            return None


if __name__ == "__main__":
    cookie = CookieManager()
    downloader = Downloader(cookie)
    video_href = "https://playback.eeo.cn/794b4a11vodbj1252412222/040a79705145403714463441300/f0.mp4"
    downloader.download(url=video_href, filename="video-1.mp4")