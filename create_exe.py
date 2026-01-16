"""
创建VIP多线路播放器的EXE可执行文件
使用PyInstaller将Flet应用打包为独立的EXE文件
"""
import os
import sys
from pathlib import Path

def create_exe():
    """创建EXE文件"""
    try:
        import PyInstaller
        print(f"PyInstaller版本: {PyInstaller.__version__}")
    except ImportError:
        print("PyInstaller未安装，正在安装...")
        os.system("pip install pyinstaller")
    
    # 获取项目根目录
    project_dir = Path(__file__).parent
    app_file = project_dir / "flet_app.py"
    
    # 检查应用文件是否存在
    if not app_file.exists():
        print(f"错误: 找不到应用文件 {app_file}")
        return False
    
    # 尝试查找图标文件（只查找真正的图标文件）
    icon_file = None
    possible_icon_paths = [
        project_dir / "icon.ico",      # ICO格式图标
        project_dir / "icon.png",      # PNG格式图标
        project_dir.parent / "icon.ico",  # 上级目录的ICO图标
        project_dir.parent / "icon.png",  # 上级目录的PNG图标
        project_dir / "app_icon.ico",     # 应用图标
        project_dir / "app_icon.png",     # 应用图标
    ]
    
    for icon_path in possible_icon_paths:
        if icon_path.exists():
            # 检查是否为真正的图标文件（而不是Python文件）
            if icon_path.suffix.lower() in ['.ico', '.png', '.jpg', '.jpeg']:
                icon_file = icon_path
                print(f"找到图标文件: {icon_file}")
                break
    
    # 构建PyInstaller命令
    cmd_parts = [
        "pyinstaller",
        "--onefile",  # 打包成单个文件
        "--windowed",  # 不显示控制台窗口
        "--name", "VIP多线路播放器",  # 应用名称
        "--distpath", str(project_dir / "dist"),  # 输出目录
        "--workpath", str(project_dir / "build_temp"),  # 临时工作目录
        "--specpath", str(project_dir / "specs"),  # spec文件目录
        "--clean",  # 清理临时文件
    ]
    
    # 如果找到图标文件，添加图标参数
    if icon_file:
        cmd_parts.extend(["--icon", str(icon_file)])
    else:
        print("未找到图标文件，将使用默认图标")
    
    # 添加主应用文件
    cmd_parts.append(str(app_file))
    
    # 组建完整命令
    cmd = " ".join(cmd_parts)
    
    print(f"执行打包命令: {cmd}")
    print("开始打包...")
    
    # 执行打包命令
    result = os.system(cmd)
    
    if result == 0:
        print("\nEXE文件打包成功!")
        exe_path = project_dir / "dist" / "VIP多线路播放器.exe"
        if exe_path.exists():
            print(f"EXE文件位置: {exe_path}")
            print(f"文件大小: {exe_path.stat().st_size / (1024*1024):.2f} MB")
        else:
            print("警告: 未找到预期的EXE文件")
        return True
    else:
        print(f"\n打包失败，返回码: {result}")
        return False

def create_spec_file():
    """创建PyInstaller规范文件以进行更精细的控制"""
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-
import sys
from pathlib import Path

# 获取项目路径
project_dir = Path(__file__).parent

block_cipher = None

a = Analysis(
    ['flet_app.py'],
    pathex=[str(project_dir)],
    binaries=[],
    datas=[
        # 如果有其他资源文件需要包含，可以在这里添加
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='VIP多线路播放器',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # 如果有图标文件，可以在这里指定路径
)
'''
    
    project_dir = Path(__file__).parent
    spec_file = project_dir / "vip_video_player.spec"
    
    with open(spec_file, 'w', encoding='utf-8') as f:
        f.write(spec_content)
    
    print(f"SPEC文件已创建: {spec_file}")
    return spec_file

if __name__ == "__main__":
    print("VIP多线路播放器 - EXE打包工具")
    print("="*40)
    
    # 创建SPEC文件
    spec_file = create_spec_file()
    
    # 执行打包
    success = create_exe()
    
    if success:
        print("\n打包完成! 您可以在 dist/ 目录中找到 EXE 文件。")
    else:
        print("\n打包失败，请检查错误信息。")
        
    print("\n提示: 如果需要使用特定图标，请确保图标文件存在于项目目录中，")
    print("然后修改 create_exe.py 中的图标路径设置。")