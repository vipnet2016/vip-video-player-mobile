# VIP多线路播放器 - 移动版

这是VIP多线路播放器的移动版本，使用Kivy框架开发，可打包为Android APK。

## 构建说明

### 环境要求
- Linux系统（或WSL2）
- Python 3.7+
- Buildozer

### 安装Buildozer
```bash
pip install buildozer
```

### 初始化并构建
```bash
cd /path/to/mobile_app
buildozer init
buildozer android debug
```

### 构建发布版本
```bash
buildozer android release
```

## 功能说明

- 视频链接解析播放
- 多线路选择
- 自动线路匹配
- 历史记录管理
- 网络连接检测

## 在线构建方案

如果本地构建遇到问题，可以使用GitHub Actions进行在线构建：

1. 创建GitHub仓库并推送代码
2. GitHub Actions将自动构建APK
3. 在Actions页面下载构建产物

详情请参考 ONLINE_BUILD.md 文件。

## 注意事项

- 首次构建会下载大量Android SDK和NDK组件，可能需要较长时间
- 确保网络连接稳定
- 构建过程中需要足够的磁盘空间

## 文件说明

- `mobile_video_player.py` - 主应用代码
- `buildozer.spec` - 构建配置文件
- `icon.png` - 应用图标（需要提供）
- `splash.png` - 启动画面（需要提供）