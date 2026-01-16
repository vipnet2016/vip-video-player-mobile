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

## Flet版本构建（推荐）

我们已提供使用Flet框架的版本，这是更现代和稳定的跨平台解决方案。

### 快速开始

1. **安装依赖**：
   ```bash
   pip install flet
   ```

2. **运行开发版本**：
   ```bash
   python flet_app.py
   ```

3. **构建APK**：
   ```bash
   python build_flet.py --build
   ```

### Flet版本特性

- 更简单的部署流程
- 更好的跨平台兼容性
- 更少的环境依赖问题
- 现代化的UI体验

## 替代构建方案

由于云端构建遇到了一些技术限制，我们提供了以下替代构建方案：

1. **本地Docker构建**：使用官方的Kivy构建Docker镜像进行本地构建
   ```bash
   docker run --rm -v "$PWD":/home/user/hostcwd kivy/buildozer android debug
   ```

2. **使用Flet框架**：将应用重构为Flet应用，提供更好的跨平台兼容性

3. **GitHub Codespaces**：在GitHub Codespaces中进行构建

4. **第三方APK构建服务**：使用在线APK构建平台

详情请参考 BUILD_ISSUES.md 文件。

## 注意事项

- 首次构建会下载大量Android SDK和NDK组件，可能需要较长时间
- 确保网络连接稳定
- 构建过程中需要足够的磁盘空间

## 文件说明

- `mobile_video_player.py` - 主应用代码
- `buildozer.spec` - 构建配置文件
- `icon.png` - 应用图标（需要提供）
- `splash.png` - 启动画面（需要提供）# Workflow trigger 01/15/2026 19:07:20
