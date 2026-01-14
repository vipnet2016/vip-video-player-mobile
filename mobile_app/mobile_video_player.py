import json
import os
import threading
import webbrowser
from urllib.parse import quote, urlparse, urlsplit, urlunsplit
from pathlib import Path
from typing import List, Optional
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.uix.checkbox import CheckBox
from kivy.core.clipboard import Clipboard
from kivy.clock import Clock
from kivy.network.urlrequest import UrlRequest
import ssl
# 禁用SSL验证（在移动设备上可能需要）
ssl._create_default_https_context = ssl._create_unverified_context


class MobileVideoPlayerApp(App):
    def build(self):
        self.title = 'VIP多线路播放器'
        
        # 初始化数据
        self.lines = []
        self.history_items = []
        self.current_url = ""
        self.selected_line = ""
        
        # 创建应用数据目录
        self.app_data_dir = self.get_app_data_dir()
        self.config_path = self.app_data_dir / 'video_lines.json'
        self.history_path = self.app_data_dir / 'video_history.json'
        
        # 加载配置
        self.load_lines()
        self.load_history()
        
        # 创建主布局
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # 标题
        title_label = Label(text='VIP多线路视频播放器', size_hint_y=None, height=60, 
                           font_size=24, bold=True, color=(0.2, 0.4, 0.8, 1))
        main_layout.add_widget(title_label)
        
        subtitle_label = Label(
            text='粘贴视频网址 → 线路自动打开播放 | 播放历史记录 → 回填', 
            size_hint_y=None, height=30, font_size=14, color=(0.5, 0.5, 0.5, 1)
        )
        main_layout.add_widget(subtitle_label)
        
        # URL输入区域
        url_input_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50)
        self.url_input = TextInput(hint_text='请输入或粘贴视频网址', multiline=False, font_size=16)
        url_input_layout.add_widget(self.url_input)
        
        paste_btn = Button(text='粘贴', size_hint_x=None, width=80, 
                          background_color=(0.2, 0.6, 1, 1))
        paste_btn.bind(on_press=self.paste_url)
        url_input_layout.add_widget(paste_btn)
        
        main_layout.add_widget(url_input_layout)
        
        # 线路选择
        line_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50)
        line_label = Label(text='线路:', size_hint_x=None, width=60, font_size=16)
        line_layout.add_widget(line_label)
        
        line_names = [line['name'] for line in self.lines] if self.lines else ['无线路']
        self.line_spinner = Spinner(
            text=line_names[0],
            values=line_names,
            size_hint_x=2,
            font_size=16
        )
        line_layout.add_widget(self.line_spinner)
        
        refresh_btn = Button(text='刷新', size_hint_x=None, width=80, 
                           background_color=(0.5, 0.7, 1, 1))
        refresh_btn.bind(on_press=self.reload_lines)
        line_layout.add_widget(refresh_btn)
        
        main_layout.add_widget(line_layout)
        
        # 选项复选框
        options_layout = GridLayout(cols=2, size_hint_y=None, height=40)
        self.auto_select_checkbox = CheckBox(active=True)
        auto_select_label = Label(text='自动选线路', halign='left')
        options_layout.add_widget(auto_select_label)
        options_layout.add_widget(self.auto_select_checkbox)
        
        self.auto_open_checkbox = CheckBox(active=True)
        auto_open_label = Label(text='粘贴后自动打开', halign='left')
        options_layout.add_widget(auto_open_label)
        options_layout.add_widget(self.auto_open_checkbox)
        
        main_layout.add_widget(options_layout)
        
        # 功能按钮区域
        button_layout = GridLayout(cols=4, spacing=5, size_hint_y=None, height=60)
        
        open_btn = Button(text='打开', background_color=(0.2, 0.6, 0.2, 1), font_size=16)
        open_btn.bind(on_press=self.open_in_browser)
        button_layout.add_widget(open_btn)
        
        check_btn = Button(text='检测', background_color=(0.8, 0.6, 0.2, 1), font_size=16)
        check_btn.bind(on_press=self.check_line)
        button_layout.add_widget(check_btn)
        
        clear_btn = Button(text='清空', background_color=(0.8, 0.2, 0.2, 1), font_size=16)
        clear_btn.bind(on_press=self.clear_input)
        button_layout.add_widget(clear_btn)
        
        quit_btn = Button(text='退出', background_color=(0.5, 0.5, 0.5, 1), font_size=16)
        quit_btn.bind(on_press=self.stop)
        button_layout.add_widget(quit_btn)
        
        main_layout.add_widget(button_layout)
        
        # 历史记录标题
        history_title = Label(text='历史记录', size_hint_y=None, height=40, 
                             font_size=18, bold=True, color=(0.2, 0.4, 0.8, 1))
        main_layout.add_widget(history_title)
        
        # 创建历史记录列表
        self.history_scroll = ScrollView(size_hint_y=0.4)
        self.history_grid = GridLayout(cols=1, spacing=5, size_hint_y=None, padding=5)
        self.history_grid.bind(minimum_height=self.history_grid.setter('height'))
        
        for item in self.history_items:
            history_btn = Button(
                text=item, 
                size_hint_y=None, 
                height=40,
                background_color=(0.9, 0.9, 0.9, 1),
                color=(0, 0, 0, 1)
            )
            history_btn.bind(on_press=lambda x, url=item: self.fill_from_history(url))
            self.history_grid.add_widget(history_btn)
        
        self.history_scroll.add_widget(self.history_grid)
        main_layout.add_widget(self.history_scroll)
        
        # 历史记录操作按钮
        hist_button_layout = GridLayout(cols=2, spacing=5, size_hint_y=None, height=50)
        
        fill_btn = Button(text='回填选中', background_color=(0.6, 0.4, 0.8, 1))
        fill_btn.bind(on_press=self.fill_from_history_selected)
        hist_button_layout.add_widget(fill_btn)
        
        clear_hist_btn = Button(text='清空历史', background_color=(0.8, 0.4, 0.6, 1))
        clear_hist_btn.bind(on_press=self.clear_history)
        hist_button_layout.add_widget(clear_hist_btn)
        
        main_layout.add_widget(hist_button_layout)
        
        # 状态栏
        self.status_label = Label(
            text='就绪', 
            size_hint_y=None, 
            height=40, 
            font_size=14,
            halign='left',
            text_size=(None, 40)
        )
        main_layout.add_widget(self.status_label)
        
        # 监听URL输入变化，实现自动选择线路
        self.url_input.bind(text=self.on_url_text_change)
        
        return main_layout

    def get_app_data_dir(self):
        """获取应用数据目录"""
        try:
            from kivy.utils import platform
            if platform == 'android':
                from android.storage import app_storage_path
                path = Path(app_storage_path()) / '.video_player'
            else:
                path = Path.home() / '.video_player'
        except ImportError:
            path = Path.home() / '.video_player'
        
        path.mkdir(parents=True, exist_ok=True)
        return path

    def load_lines(self):
        """加载线路配置"""
        try:
            if not self.config_path.exists():
                # 创建默认配置
                default_config = {
                    'lines': [
                        {
                            'name': '视频线路',
                            'template': 'https://jx.xmflv.com/?url={url}',
                            'priority': 5,
                            'match_domains': [
                                'iqiyi.com',
                                'v.qq.com',
                                'youku.com',
                                'mgtv.com',
                                'sohu.com',
                                'bilibili.com',
                                'pptv.com',
                                'wasu.cn',
                                '1905.com',
                            ],
                        }
                    ]
                }
                self.config_path.write_text(
                    json.dumps(default_config, ensure_ascii=False, indent=2), 
                    encoding='utf-8'
                )
            
            with open(self.config_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                lines = data.get('lines', [])
                
                # 验证和标准化线路数据
                normalized_lines = []
                for item in lines:
                    if not isinstance(item, dict):
                        continue
                    name = str(item.get('name', '')).strip()
                    template = str(item.get('template', '')).strip()
                    if not name or not template:
                        continue
                    strip_query = bool(item.get('strip_query', False))
                    strip_fragment = bool(item.get('strip_fragment', False))
                    priority_raw = item.get('priority', 0)
                    try:
                        priority = int(priority_raw)
                    except Exception:
                        priority = 0

                    match_domains_raw = item.get('match_domains', [])
                    match_domains: List[str] = []
                    if isinstance(match_domains_raw, list):
                        for d in match_domains_raw:
                            if isinstance(d, str) and d.strip():
                                match_domains.append(d.strip().lower().lstrip('.'))
                    
                    normalized_lines.append({
                        'name': name,
                        'template': template,
                        'strip_query': strip_query,
                        'strip_fragment': strip_fragment,
                        'priority': priority,
                        'match_domains': match_domains,
                    })

                self.lines = normalized_lines
                
                # 更新spinner值
                if hasattr(self, 'line_spinner'):
                    line_names = [line['name'] for line in self.lines] if self.lines else ['无线路']
                    self.line_spinner.values = line_names
                    if self.lines:
                        self.line_spinner.text = self.lines[0]['name']

        except Exception as e:
            print(f"加载线路失败: {e}")
            self.lines = []
            if hasattr(self, 'line_spinner'):
                self.line_spinner.values = ['无线路']
                self.line_spinner.text = '无线路'

    def load_history(self):
        """加载历史记录"""
        try:
            if self.history_path.exists():
                with open(self.history_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    items = data.get('items', [])
                    if isinstance(items, list):
                        # 过滤并规范化URL
                        normalized = []
                        for x in items:
                            if isinstance(x, str):
                                u = x.strip()
                                if u:
                                    normalized.append(u)
                        self.history_items = normalized[:20]  # 最多20条历史记录
                    else:
                        self.history_items = []
            else:
                self.history_items = []
        except Exception as e:
            print(f"加载历史记录失败: {e}")
            self.history_items = []

    def save_history(self):
        """保存历史记录"""
        try:
            payload = {'items': self.history_items[:20]}
            self.history_path.write_text(
                json.dumps(payload, ensure_ascii=False, indent=2), 
                encoding='utf-8'
            )
        except Exception as e:
            print(f"保存历史记录失败: {e}")

    def update_history_display(self):
        """更新历史记录显示"""
        self.history_grid.clear_widgets()
        for item in self.history_items:
            history_btn = Button(
                text=item, 
                size_hint_y=None, 
                height=40,
                background_color=(0.9, 0.9, 0.9, 1),
                color=(0, 0, 0, 1)
            )
            history_btn.bind(on_press=lambda x, url=item: self.fill_from_history(url))
            self.history_grid.add_widget(history_btn)

    def paste_url(self, instance):
        """从剪贴板粘贴URL"""
        try:
            clipboard_text = Clipboard.paste()
            if clipboard_text:
                self.url_input.text = clipboard_text
                self.status_label.text = '已从剪贴板粘贴'
                
                # 如果启用了粘贴后自动打开，则自动打开
                if self.auto_open_checkbox.active:
                    self.open_in_browser(None)
        except Exception as e:
            self.status_label.text = f'粘贴失败: {e}'

    def reload_lines(self, instance):
        """刷新线路"""
        self.load_lines()
        if self.lines:
            self.status_label.text = f'已加载 {len(self.lines)} 条线路'
        else:
            self.status_label.text = '未加载到任何线路'

    def validate_url(self, url):
        """验证URL"""
        url = url.strip()
        if not url:
            return None
        
        parsed = urlparse(url)
        if parsed.scheme in ('http', 'https') and parsed.netloc:
            return url
        
        return None

    def extract_domain(self, url: str) -> Optional[str]:
        """提取域名"""
        try:
            parsed = urlparse(url)
            host = (parsed.netloc or '').strip().lower()
            if not host:
                return None
            if '@' in host:
                host = host.split('@', 1)[-1]
            if ':' in host:
                host = host.split(':', 1)[0]
            if host.startswith('www.'):
                host = host[4:]
            return host or None
        except Exception:
            return None

    def domain_matches(self, domain: str, pattern: str) -> bool:
        """检查域名是否匹配模式"""
        pattern = pattern.strip().lower().lstrip('.')
        if not pattern:
            return False
        return domain == pattern or domain.endswith('.' + pattern)

    def try_auto_select_line(self):
        """尝试自动选择线路"""
        if not self.auto_select_checkbox.active:
            return

        url = self.url_input.text.strip()
        validated_url = self.validate_url(url)
        if not validated_url:
            return

        domain = self.extract_domain(validated_url)
        if not domain:
            return

        best = None
        best_priority = None
        for idx, line in enumerate(self.lines):
            patterns = line.get('match_domains', [])
            if not patterns:
                continue
            if any(self.domain_matches(domain, p) for p in patterns):
                pri = int(line.get('priority', 0))
                key = (pri, -idx)
                if best is None or key > best_priority:
                    best = line
                    best_priority = key

        if best is not None:
            if self.line_spinner.text != best['name']:
                self.line_spinner.text = best['name']
                self.status_label.text = f'已自动选择线路：{best["name"]}（{domain}）'

    def on_url_text_change(self, instance, value):
        """当URL输入改变时触发"""
        self.try_auto_select_line()

    def normalize_url(self, url, strip_query=False, strip_fragment=False):
        """标准化URL"""
        parts = list(urlsplit(url))
        if strip_query:
            parts[3] = ''
        if strip_fragment:
            parts[4] = ''
        return urlunsplit(parts)

    def build_target_url(self, url, template):
        """构建目标URL"""
        encoded_url = quote(url, safe=':/?&=%')
        if '{url}' in template:
            target = template.replace('{url}', encoded_url)
        else:
            target = template + encoded_url

        if '{title}' in target:
            target = target.replace('{title}', '')
        return target

    def open_in_browser(self, instance):
        """在浏览器中打开"""
        url = self.validate_url(self.url_input.text)
        if not url:
            self.show_popup('提示', '请输入正确的网址（以 http:// 或 https:// 开头）')
            return

        # 获取选定线路
        selected_line_name = self.line_spinner.text
        selected_line = None
        for line in self.lines:
            if line['name'] == selected_line_name:
                selected_line = line
                break

        if not selected_line:
            self.show_popup('提示', '请先选择线路，或打开配置文件添加线路')
            return

        # 构建目标URL
        normalized_url = self.normalize_url(
            url, 
            selected_line.get('strip_query', False), 
            selected_line.get('strip_fragment', False)
        )
        target = self.build_target_url(normalized_url, selected_line['template'])

        # 打开URL
        try:
            webbrowser.open(target)
            self.add_to_history(url)
            self.status_label.text = f'已打开：{target}'
        except Exception as e:
            self.status_label.text = f'打开失败：{e}'

    def check_line(self, instance):
        """检测线路"""
        url = self.validate_url(self.url_input.text)
        if not url:
            self.show_popup('提示', '请输入正确的网址（以 http:// 或 https:// 开头）')
            return

        selected_line_name = self.line_spinner.text
        selected_line = None
        for line in self.lines:
            if line['name'] == selected_line_name:
                selected_line = line
                break

        if not selected_line:
            self.show_popup('提示', '请先选择线路，或打开配置文件添加线路')
            return

        normalized_url = self.normalize_url(
            url, 
            selected_line.get('strip_query', False), 
            selected_line.get('strip_fragment', False)
        )
        target = self.build_target_url(normalized_url, selected_line['template'])

        self.status_label.text = '检测中，请稍候...'

        # 在后台线程中检测
        t = threading.Thread(target=self.check_target_worker, args=(target,))
        t.start()

    def check_target_worker(self, target):
        """在线程中检测目标URL"""
        try:
            import urllib.request
            req = urllib.request.Request(target, method='HEAD', 
                                       headers={'User-Agent': 'Mozilla/5.0'})
            response = urllib.request.urlopen(req, timeout=6)
            status_code = response.getcode()
            success = 200 <= status_code < 400
            detail = f'HTTP {status_code}'
        except urllib.error.HTTPError as e:
            success = False
            detail = f'HTTP {e.code}'
        except urllib.error.URLError as e:
            success = False
            detail = str(e.reason)
        except Exception as e:
            success = False
            detail = str(e)

        # 在主线程中更新UI
        Clock.schedule_once(lambda dt: self.show_check_result(success, detail, target), 0)

    def show_check_result(self, success, detail, target):
        """显示检测结果"""
        if success:
            self.status_label.text = f'检测通过：{detail}'
            self.show_popup('检测结果', f'线路可用（或可访问）\n\n{detail}\n\n目标地址：\n{target}')
        else:
            self.status_label.text = f'检测失败：{detail}'
            self.show_popup('检测结果', f'线路可能不可用或不可访问\n\n{detail}\n\n目标地址：\n{target}')

    def clear_input(self, instance):
        """清空输入"""
        self.url_input.text = ''
        self.status_label.text = '输入已清空'

    def fill_from_history(self, url):
        """从历史记录填充"""
        self.url_input.text = url
        self.status_label.text = '已从历史记录回填'
        self.try_auto_select_line()
        if self.auto_open_checkbox.active:
            self.open_in_browser(None)

    def fill_from_history_selected(self, instance):
        """填充选中的历史记录"""
        # 对于简单实现，我们使用第一个历史记录
        if self.history_items:
            self.fill_from_history(self.history_items[0])
        else:
            self.status_label.text = '没有历史记录可填充'

    def clear_history(self, instance):
        """清空历史记录"""
        self.history_items = []
        self.update_history_display()
        try:
            if self.history_path.exists():
                self.history_path.unlink()
        except Exception:
            pass
        self.status_label.text = '历史记录已清空'

    def show_popup(self, title, message):
        """显示弹窗"""
        popup_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        popup_label = Label(text=message, text_size=(400, None), halign='center')
        close_btn = Button(text='确定', size_hint_y=None, height=50)
        
        popup_layout.add_widget(popup_label)
        popup_layout.add_widget(close_btn)
        
        popup = Popup(title=title, content=popup_layout, 
                     size_hint=(0.8, 0.6), auto_dismiss=False)
        close_btn.bind(on_press=popup.dismiss)
        
        popup.open()


MobileVideoPlayerApp().run()