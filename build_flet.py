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
        print(f"Flet版本: {flet.__version__ if hasattr(flet, '__version__') else 'Unknown'}")
    except ImportError:
        print("错误: Flet未安装，请运行 'pip install flet'")
        return False

    # 检查flet-cli是否已安装
    try:
        result = subprocess.run([sys.executable, "-m", "pip", "show", "flet-cli"], 
                              capture_output=True, text=True)
        if result.returncode != 0:
            print("flet-cli未找到，正在安装...")
            subprocess.run([sys.executable, "-m", "pip", "install", "flet-cli"])
    except Exception as e:
        print(f"安装flet-cli时出错: {e}")

    # 尝试使用正确的flet build命令格式
    build_cmd = [
        sys.executable, "-m", "flet.cli", "build",
        "apk",  # 目标平台放在前面
        ".",    # 当前目录作为应用路径
        "--project-name", "VIP多线路播放器",
        "--app-id", "com.vip.videoplayer",
        "--description", "VIP多线路视频播放器",
        "--module-name", "flet_app"  # 指定模块名
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
        
        # 尝试备用构建命令格式
        print("\n尝试备用构建方法...")
        return build_with_correct_format()
    except FileNotFoundError:
        print("错误: 找不到flet构建命令")
        print("请确保Flet已正确安装: pip install flet")
        return build_with_correct_format()

def build_with_correct_format():
    """使用正确的格式构建应用"""
    try:
        # 尝试正确的命令格式
        build_cmd = [
            sys.executable, "-m", "flet.cli", "build",
            "apk",  # 平台名称
            ".",    # 当前目录
            "--project", "VIP多线路播放器",
            "--bundle-id", "com.vip.videoplayer",
            "--module-name", "flet_app"
        ]
        
        print("执行备用构建命令...")
        result = subprocess.run(build_cmd, cwd=os.getcwd(), check=True, capture_output=True, text=True)
        print("构建输出:")
        print(result.stdout)
        
        if result.stderr:
            print("构建警告/错误:")
            print(result.stderr)
            
        print("Flet应用构建成功!")
        print("APK文件应该在 build/ 目录中")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print(f"备用构建方法也失败: {e}")
        print("\n提示: Flet构建APK需要额外的Android开发环境配置。")
        print("您也可以在本地开发模式下运行应用: python flet_app.py")
        print("或者使用云端构建工作流，它会在云端环境中自动配置所需的Android SDK。")
        return False

def run_dev_server():
    """运行开发服务器"""
    print("启动Flet开发服务器...")
    
    try:
        import flet
        print(f"Flet版本: {flet.__version__ if hasattr(flet, '__version__') else 'Unknown'}")
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