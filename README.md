# ClassIn Downloader
## 项目说明
本项目用于下载`classin`平台录制的视频课程

## 项目功能
1. 根据课程日期检测课程列表
2. 下载课程视频
3. 下载视频时按照课程名称对课程进行重命名
4. 对下载后的课程进行分类保存

## 技术栈
1. `selenium` + `chromedirver`
2. `requests`

## 项目思路
1. 使用账号密码登录
2. 保存`cookies`
3. 根据课程时间筛选课程信息
4. 获取到视频下载地址
5. 下载视频并重命名

## 项目结构
```
├── README.md
├── config
│ └── config.py
├── data
├── main.py
├── pyproject.toml
└── src
    ├── downloader.py
    └── spider.py
```

