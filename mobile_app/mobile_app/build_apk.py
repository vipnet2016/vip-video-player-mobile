#!/usr/bin/env python3
"""
VIP多线路播放器 - APK构建脚本
用于简化APK构建过程
"""

import os
import sys
import subprocess
import platform
from pathlib import Path


def check_dependencies():
    """检查依赖项"""
    print("检查依赖项...")
    
    # 检查Python版本
    if sys.version_info < (3, 7):
        print("错误: 需要Python 3.7或更高版本")
        return False
    
    # 检查buildozer
    try:
        import buildozer
        print("✓ Buildozer 已安装")
    except ImportError:
        print("× Buildozer 未安装")
        print("请运行: pip install buildozer")
        return False
    
    return True


def create_placeholder_images():
    """创建占位符图片"""
    import io
    try:
        from PIL import Image, ImageDraw, ImageFont
        
        # 创建图标 (512x512)
        icon = Image.new('RGB', (512, 512), color='white')
        draw = ImageDraw.Draw(icon)
        draw.rectangle([0, 0, 512, 512], outline='black', width=5)
        draw.text((100, 200), 'VIP', fill='black', font_size=60)
        draw.text((80, 280), '播放器', fill='black', font_size=50)
        icon.save('icon.png')
        print("✓ 创建了图标文件 icon.png")
        
        # 创建启动画面 (1920x1080)
        splash = Image.new('RGB', (1920, 1080), color='#f0f0f0')
        draw = ImageDraw.Draw(splash)
        draw.rectangle([0, 0, 1920, 1080], outline='#cccccc', width=10)
        draw.text((800, 400), 'VIP', fill='#2196F3', font_size=120)
        draw.text((650, 600), '多线路播放器', fill='#2196F3', font_size=80)
        splash.save('splash.png')
        print("✓ 创建了启动画面 splash.png")
        
    except ImportError:
        print("⚠️  提示: 未安装PIL/Pillow，跳过创建占位符图片")
        print("   如需自定义图片，请运行: pip install Pillow")
        print("   然后手动添加 icon.png 和 splash.png 文件")


def build_apk(debug=True):
    """构建APK"""
    print("\n开始构建APK...")
    
    if not Path('buildozer.spec').exists():
        print("错误: 未找到 buildozer.spec 文件")
        return False
    
    # 创建占位符图片（如果不存在）
    if not Path('icon.png').exists() or not Path('splash.png').exists():
        create_placeholder_images()
    
    # 确定构建命令
    cmd = ['buildozer', 'android', 'debug' if debug else 'release']
    
    print(f"运行命令: {' '.join(cmd)}")
    
    try:
        # 运行构建命令
        result = subprocess.run(cmd, check=True, cwd=os.getcwd())
        print("✓ APK构建成功!")
        
        # 查找生成的APK文件
        apk_files = list(Path('.').rglob('*.apk'))
        if apk_files:
            print(f"生成的APK文件: {apk_files[0]}")
        else:
            print("警告: 未找到生成的APK文件")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"× APK构建失败: {e}")
        return False
    except FileNotFoundError:
        print("× 未找到 buildozer 命令")
        print("请确保已安装 buildozer 并在PATH中")
        return False


def main():
    print("VIP多线路播放器 - APK构建工具")
    print("="*40)
    
    # 检查运行环境
    system = platform.system().lower()
    if system != 'linux':
        print(f"⚠️  警告: 当前系统为 {system}, Buildozer 在Linux上运行效果最好")
        print("   建议在Linux或WSL2上运行此脚本")
    
    # 检查依赖
    if not check_dependencies():
        return
    
    # 构建APK
    if build_apk(debug=True):
        print("\n🎉 构建完成!")
        print("APK文件已生成，可以安装到Android设备上使用")
    else:
        print("\n❌ 构建失败，请检查错误信息")
        print("可能需要:")
        print("- 检查网络连接")
        print("- 确保有足够的磁盘空间")
        print("- 确保已安装所有必要的依赖")


if __name__ == '__main__':
    main()