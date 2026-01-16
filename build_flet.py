"""
Flet应用构建脚本
用于构建VIP多线路播放器的跨平台应用
"""
import subprocess
import sys
import os
from pathlib import Path

def build_flet_app():
    """构建Flet应用"""
    print("开始构建Flet应用...")
    
    # 检查flet是否已安装
    try:
        import flet
        print(f"Flet版本: {flet.__version__}")
    except ImportError:
        print("错误: Flet未安装，请运行 'pip install flet'")
        return False

    # 构建命令
    build_cmd = [
        sys.executable, "-m", "flet.build",
        "flet_app.py",  # 主应用文件
        "--target", "apk",  # 构建Android APK
        "--project-name", "VIP多线路播放器",
        "--app-id", "com.vip.videoplayer",
        "--version", "1.0.0",
        "--description", "VIP多线路视频播放器",
        "--publish"
    ]
    
    try:
        print("执行构建命令...")
        result = subprocess.run(build_cmd, cwd=os.getcwd(), check=True, capture_output=True, text=True)
        print("构建输出:")
        print(result.stdout)
        
        if result.stderr:
            print("构建警告/错误:")
            print(result.stderr)
            
        print("Flet应用构建成功!")
        print("APK文件应该在 build/ 目录中")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"构建失败: {e}")
        print(f"错误输出: {e.stderr}")
        return False
    except FileNotFoundError:
        print("错误: 找不到flet.build命令")
        print("请确保Flet已正确安装: pip install flet")
        return False

def run_dev_server():
    """运行开发服务器"""
    print("启动Flet开发服务器...")
    
    try:
        import flet
        print(f"Flet版本: {flet.__version__}")
    except ImportError:
        print("错误: Flet未安装，请运行 'pip install flet'")
        return False

    dev_cmd = [sys.executable, "-m", "flet", "flet_app.py"]
    
    try:
        print("启动开发服务器...")
        subprocess.run(dev_cmd, cwd=os.getcwd())
        return True
    except Exception as e:
        print(f"启动开发服务器失败: {e}")
        return False

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Flet应用构建工具')
    parser.add_argument('--build', action='store_true', help='构建APK')
    parser.add_argument('--dev', action='store_true', help='运行开发服务器')
    
    args = parser.parse_args()
    
    if args.build:
        build_flet_app()
    elif args.dev:
        run_dev_server()
    else:
        print("使用方法:")
        print("  python build_flet.py --build  # 构建APK")
        print("  python build_flet.py --dev    # 运行开发服务器")
        print("")
        
        # 默认运行开发服务器
        print("运行开发服务器进行测试...")
        run_dev_server()