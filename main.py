"""
VIP多线路播放器 - 移动端入口文件
此文件作为Kivy应用的入口点
"""

try:
    from mobile_video_player import MobileVideoPlayerApp
    app = MobileVideoPlayerApp
except ImportError:
    # Fallback to simple test app if main app fails to import
    from simple_test import SimpleTestApp as MobileVideoPlayerApp

MobileVideoPlayerApp().run()

if __name__ == '__main__':
    MobileVideoPlayerApp().run()