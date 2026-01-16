# 安装说明

## 在Linux/WSL2上构建

### 1. 安装依赖

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install -y build-essential git python3 python3-pip python3-dev

# 安装 Cython 和其他构建依赖
pip3 install cython

# 安装 Buildozer
pip3 install buildozer
```

### 2. 初始化 Buildozer

```bash
cd /path/to/mobile_app
buildozer init
```

### 3. 构建 APK

```bash
buildozer android debug
```

生成的 APK 文件将在 `bin/` 目录中。

## 关于 WSL2 (Windows Subsystem for Linux)

如果您在 Windows 上开发，强烈建议使用 WSL2：

1. 安装 WSL2 并 Ubuntu
2. 在 WSL2 中克隆项目
3. 按照上面的 Linux 步骤操作

## 故障排除

### 构建失败

- 确保有足够的磁盘空间（至少 2GB）
- 确保网络连接稳定
- 检查 Java 版本（需要 JDK 8）

### 缺少依赖

如果遇到特定的 Python 包缺失，在 `buildozer.spec` 的 requirements 中添加它们。

## 重要说明

- 首次构建会下载 Android SDK、NDK 等组件，可能需要很长时间
- 请确保网络连接稳定
- 构建过程可能需要 1-2GB 的额外空间