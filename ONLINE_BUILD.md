# 在线构建APK

由于本地构建可能遇到各种环境问题，我们提供了在线构建方案。

## 使用GitHub Actions构建

### 步骤：

1. **创建GitHub仓库**
   - 登录GitHub账户
   - 创建新仓库（例如命名为 "vip-video-player-mobile"）

2. **推送代码到仓库**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPOSITORY_NAME.git
   git branch -M main
   git push -u origin main
   ```

3. **触发构建**
   - 推送代码后，GitHub Actions会自动开始构建
   - 转到 "Actions" 标签页查看构建进度

4. **下载APK文件**
   - 构建完成后，转到 "Actions" 页面
   - 点击最近的构建作业
   - 在 "Artifacts" 部分下载生成的APK文件

## 其他在线构建服务

### 1. Replit
1. 访问 https://replit.com
2. 创建新项目
3. 上传所有项目文件
4. 在控制台中运行构建命令

### 2. Gitpod
1. 安装Gitpod浏览器扩展
2. 访问您的GitHub仓库
3. 使用Gitpod打开项目
4. 在终端中运行构建命令

## 注意事项

- 确保所有必需的文件都已提交到仓库
- 检查 `buildozer.spec` 文件配置正确
- 构建过程可能需要30分钟到数小时
- 确保网络连接稳定

## 故障排除

如果构建失败：
1. 检查GitHub Actions日志中的错误信息
2. 确认所有依赖项都已正确配置
3. 验证Android SDK许可证已接受
4. 确保API版本设置正确