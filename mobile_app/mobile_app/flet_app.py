"""
VIP多线路播放器 - Flet版本
使用Flet框架构建的跨平台应用
"""
import flet as ft
import json
import threading
import webbrowser
from urllib.parse import quote, urlparse
from pathlib import Path
import os


class VIPVideoPlayer:
    def __init__(self):
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

    def get_app_data_dir(self):
        """获取应用数据目录"""
        try:
            # 尝试获取用户数据目录
            if os.name == 'nt':  # Windows
                base_dir = Path(os.environ.get('APPDATA', Path.home()))
            else:  # Unix-like
                base_dir = Path.home()
            
            path = base_dir / '.video_player'
        except:
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
                    match_domains = []
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
                if self.lines:
                    self.selected_line = self.lines[0]['name']

        except Exception as e:
            print(f"加载线路失败: {e}")
            self.lines = []

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

    def validate_url(self, url):
        """验证URL"""
        url = url.strip()
        if not url:
            return None
        
        parsed = urlparse(url)
        if parsed.scheme in ('http', 'https') and parsed.netloc:
            return url
        
        return None

    def extract_domain(self, url: str):
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

    def domain_matches(self, domain: str, pattern: str):
        """检查域名是否匹配模式"""
        pattern = pattern.strip().lower().lstrip('.')
        if not pattern:
            return False
        return domain == pattern or domain.endswith('.' + pattern)

    def try_auto_select_line(self, url):
        """尝试自动选择线路"""
        validated_url = self.validate_url(url)
        if not validated_url:
            return None

        domain = self.extract_domain(validated_url)
        if not domain:
            return None

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

        return best['name'] if best else None

    def normalize_url(self, url, strip_query=False, strip_fragment=False):
        """标准化URL"""
        from urllib.parse import urlsplit, urlunsplit
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

    def open_in_browser(self, url, selected_line_name):
        """在浏览器中打开"""
        validated_url = self.validate_url(url)
        if not validated_url:
            return False, "请输入正确的网址（以 http:// 或 https:// 开头）"

        # 获取选定线路
        selected_line = None
        for line in self.lines:
            if line['name'] == selected_line_name:
                selected_line = line
                break

        if not selected_line:
            return False, "请先选择线路，或打开配置文件添加线路"

        # 构建目标URL
        normalized_url = self.normalize_url(
            validated_url,
            selected_line.get('strip_query', False),
            selected_line.get('strip_fragment', False)
        )
        target = self.build_target_url(normalized_url, selected_line['template'])

        # 打开URL
        try:
            webbrowser.open(target)
            self.add_to_history(validated_url)
            return True, f"已打开：{target}"
        except Exception as e:
            return False, f"打开失败：{e}"

    def add_to_history(self, url):
        """添加到历史记录"""
        if url in self.history_items:
            self.history_items.remove(url)
        self.history_items.insert(0, url)
        if len(self.history_items) > 20:
            self.history_items = self.history_items[:20]
        self.save_history()


def main(page: ft.Page):
    page.title = "VIP多线路播放器"
    page.window_width = 400
    page.window_height = 800
    page.padding = 10
    page.scroll = ft.ScrollMode.ADAPTIVE

    # 创建播放器实例
    player = VIPVideoPlayer()

    # URL输入框
    url_input = ft.TextField(
        label="请输入或粘贴视频网址",
        expand=True,
        dense=True
    )

    # 线路选择下拉框
    line_options = [ft.dropdown.Option(line['name']) for line in player.lines]
    line_dropdown = ft.Dropdown(
        label="选择线路",
        options=line_options,
        value=player.selected_line if player.lines else None,
        expand=True
    )

    # 状态文本
    status_text = ft.Text(value="就绪", size=12, color="grey")  # 使用字符串颜色值

    # 历史记录列表
    history_list = ft.Column(spacing=5, scroll=ft.ScrollMode.ADAPTIVE)

    def update_history_display():
        """更新历史记录显示"""
        history_list.controls.clear()
        for item in player.history_items:
            btn = ft.FilledButton(
                text=item[:50] + "..." if len(item) > 50 else item,
                on_click=lambda e, url=item: fill_from_history(e, url),
                style=ft.ButtonStyle(padding=ft.padding.all(5)),
                height=40
            )
            history_list.controls.append(btn)
        page.update()

    def fill_from_history(e, url):
        """从历史记录填充"""
        url_input.value = url
        auto_select_line()
        page.update()

    def auto_select_line():
        """自动选择线路"""
        if url_input.value:
            auto_selected = player.try_auto_select_line(url_input.value)
            if auto_selected and auto_selected != line_dropdown.value:
                line_dropdown.value = auto_selected

    def paste_url(e):
        """粘贴URL（Flet中模拟）"""
        # 在桌面环境中，我们直接显示提示
        page.snack_bar = ft.SnackBar(ft.Text("请直接复制URL并粘贴到输入框"))
        page.snack_bar.open = True
        page.update()

    def open_video(e):
        """打开视频"""
        if not url_input.value:
            page.snack_bar = ft.SnackBar(ft.Text("请输入视频网址"))
            page.snack_bar.open = True
            page.update()
            return

        if not line_dropdown.value:
            page.snack_bar = ft.SnackBar(ft.Text("请选择线路"))
            page.snack_bar.open = True
            page.update()
            return

        success, message = player.open_in_browser(url_input.value, line_dropdown.value)
        if success:
            status_text.value = message
        else:
            page.snack_bar = ft.SnackBar(ft.Text(message))
            page.snack_bar.open = True

        update_history_display()
        page.update()

    def check_line(e):
        """检测线路"""
        page.snack_bar = ft.SnackBar(ft.Text("线路检测功能在Flet版本中暂时不可用"))
        page.snack_bar.open = True
        page.update()

    def clear_input(e):
        """清空输入"""
        url_input.value = ""
        page.update()

    def clear_history(e):
        """清空历史记录"""
        player.history_items = []
        player.save_history()
        update_history_display()
        status_text.value = "历史记录已清空"
        page.update()

    # 更新历史记录显示
    update_history_display()

    # 主要布局
    main_column = ft.Column(
        controls=[
            ft.Text("VIP多线路视频播放器", size=24, weight=ft.FontWeight.BOLD),
            ft.Text("粘贴视频网址 → 线路自动打开播放 | 播放历史记录 → 回填", size=14),
            
            ft.Row([url_input, ft.FilledButton("粘贴", on_click=paste_url, width=60)], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            
            ft.Row([line_dropdown, ft.FilledButton("刷新", on_click=lambda e: None, width=60)], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            
            ft.Row([
                ft.FilledButton("打开", on_click=open_video, bgcolor="green", color="white"),
                ft.FilledButton("检测", on_click=check_line, bgcolor="orange", color="white"),
                ft.FilledButton("清空", on_click=clear_input, bgcolor="red", color="white"),
                ft.FilledButton("退出", on_click=lambda e: page.window_close(), bgcolor="grey", color="white")
            ], alignment=ft.MainAxisAlignment.SPACE_AROUND),

            ft.Divider(thickness=1),
            ft.Text("历史记录", size=18, weight=ft.FontWeight.BOLD),
            history_list,
            
            ft.Row([
                ft.FilledButton("回填选中", on_click=lambda e: None),
                ft.FilledButton("清空历史", on_click=clear_history, bgcolor="red", color="white")
            ], alignment=ft.MainAxisAlignment.SPACE_AROUND),

            status_text
        ],
        spacing=10,
        scroll=ft.ScrollMode.ADAPTIVE
    )

    page.add(main_column)


if __name__ == "__main__":
    ft.run(main)  # 使用新推荐的入口方法