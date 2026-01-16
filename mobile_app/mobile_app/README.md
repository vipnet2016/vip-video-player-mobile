# VIP多线路播放器 - Flet版本

使用Flet框架构建的跨平台VIP视频播放器应用。

## 特性

- 支持多视频线路播放
- 自动线路匹配
- 历史记录管理
- 现代化UI界面
- 跨平台支持（Web、桌面、移动端）

## 快速开始

### 运行开发版本

1. 安装Flet：
   ```bash
   pip install flet
   ```

2. 运行应用：
   ```bash
   python flet_app.py
   ```

### 构建APK（Android应用）

#### 本地构建（需要完整Android环境）

本地构建APK需要完整的Android开发环境，包括：

- Java Development Kit (JDK)
- Android SDK
- Android NDK
- Android Virtual Device (AVD) 或真实设备

如果您的本地环境尚未配置Android开发环境，可以使用以下命令安装必要组件：

```bash
# 安装Android SDK和相关工具
# 请参考官方Android开发文档进行环境配置
```

然后运行构建命令：

```bash
python build_flet.py --build
```

#### 云端构建（推荐）

由于本地Android环境配置较为复杂，我们推荐使用云端构建：

1. 将代码推送到GitHub仓库
2. GitHub Actions会自动运行Flet构建工作流
3. 构建完成后，APK文件会作为构建产物提供下载

## 文件结构

- `flet_app.py` - Flet应用主文件
- `build_flet.py` - Flet构建脚本
- `.github/workflows/flet-build-apk.yml` - GitHub Actions构建工作流

## Flet构建脚本使用方法

```bash
# 运行开发服务器
python build_flet.py --dev

# 构建APK
python build_flet.py --build
```

## 技术说明

此应用是从原始的tkinter应用重构而来，使用Flet框架提供更好的跨平台体验。相比之前的Buildozer方案，Flet提供了：

- 更简单的开发体验
- 更少的环境依赖问题
- 现代化的UI组件
- 更好的跨平台兼容性

## 注意事项

- 本地APK构建需要较复杂的Android环境配置
- 推荐使用云端构建获得最佳体验
- 应用功能与原始版本完全一致

## 替代方案

如果Flet构建仍然存在问题，项目还保留了Kivy/Buildozer实现的历史版本（在.git历史中），但Flet是当前推荐的实现方案。