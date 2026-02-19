# ClassIn Downloader

一个用于批量下载 [ClassIn](https://www.eeo.cn/) 平台录制视频课程的自动化工具。

## ✨ 功能特性

- 🔐 自动登录 ClassIn 平台，支持 Cookie 持久化
- 📅 按时间范围筛选课程列表
- 📥 批量下载课程回放视频
- 📝 自动按课程名称重命名视频文件
- 📊 下载进度条实时显示
- 📁 视频自动分类保存

## 🛠️ 技术栈

- **Python 3.14+**
- **Selenium** - 浏览器自动化，处理登录流程
- **Requests** - HTTP 请求，下载视频
- **Loguru** - 日志记录
- **tqdm** - 下载进度条显示
- **lxml** - HTML 解析

## 📁 项目结构

```
ClassinDownloader/
├── main.py              # 程序入口
├── pyproject.toml       # 项目配置与依赖
├── README.md
├── config/
│   └── config.py        # 配置文件（账号、路径等）
├── src/
│   ├── auth.py          # 登录认证模块
│   ├── spider.py        # 课程信息爬取模块
│   └── downloader.py    # 视频下载模块
├── utils/
│   ├── browser.py       # 浏览器管理
│   ├── cookies.py       # Cookie 管理
│   └── logger.py        # 日志配置
├── data/                # 数据目录
│   ├── cookies.json     # Cookie 存储
│   └── videos/          # 视频下载目录
└── logs/                # 日志目录
```

## 🚀 快速开始

### 1. 环境准备

- Python 3.14+
- Chrome 浏览器
- ChromeDriver（需与 Chrome 版本匹配）

### 2. 安装依赖

```bash
# 使用 uv（推荐）
uv sync

# 或使用 pip
pip install -r requirements.txt
```

### 3. 配置账号

编辑 `config/config.py`，填入你的 ClassIn 账号信息：

```python
CLASSIN_USERNAME = "your_username"
CLASSIN_PASSWORD = "your_password"
```

> ⚠️ 建议将敏感信息改为环境变量方式配置

### 4. 运行程序

```bash
python main.py
```

程序会：
1. 启动 Chrome 浏览器进行登录（首次需要手动完成验证码）
2. 保存登录 Cookie，后续可自动登录
3. 提示输入起始和结束时间（格式：`YYYY-MM-DD`）
4. 自动获取时间范围内的课程列表
5. 批量下载所有课程视频

## ⚙️ 配置说明

`config/config.py` 中的主要配置项：

| 配置项 | 说明 | 默认值 |
|--------|------|--------|
| `CLASSIN_USERNAME` | ClassIn 账号 | - |
| `CLASSIN_PASSWORD` | ClassIn 密码 | - |
| `DOWNLOAD_DIR` | 视频下载目录 | `data/videos` |
| `COOKIE_FILE` | Cookie 存储路径 | `data/cookies.json` |
| `PAGE_LOAD_TIMEOUT` | 页面加载超时时间 | 30s |
| `DATE_FORMAT` | 日期格式 | `%Y-%m-%d` |

## 📝 使用示例

```
$ python main.py
2025-02-04 18:30:00 | INFO | 程序启动
2025-02-04 18:30:02 | INFO | Chrome 浏览器已启动 (headless=False)
2025-02-04 18:30:05 | INFO | cookies 已加载，验证登录状态
请输入起始时间：2025-01-01
请输入结束时间：2025-02-04
2025-02-04 18:30:10 | INFO | 当前课程总数：15
2025-02-04 18:30:12 | INFO | 开始下载: 高等数学第一讲-1.mp4
高等数学第一讲-1.mp4: 100%|██████████| 256M/256M [02:30<00:00, 1.70MB/s]
```

## 🔧 工作原理

1. **登录认证** - 使用 Selenium 模拟浏览器登录，获取认证 Cookie
2. **Cookie 持久化** - 将 Cookie 保存到本地，下次启动自动加载
3. **课程获取** - 调用 ClassIn API 获取指定时间范围内的课程列表
4. **视频下载** - 解析视频地址，使用 Requests 流式下载

## ⚠️ 注意事项

- 首次登录可能需要手动完成滑块验证码
- Cookie 过期后需要重新登录
- 下载大量视频时请注意磁盘空间
- 请遵守 ClassIn 平台的使用条款，仅下载自己有权访问的课程

## 📄 License

MIT License

