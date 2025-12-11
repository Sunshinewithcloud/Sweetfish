"""Module adjusted to satisfy style checks."""

import tkinter as tk
from tkinter import messagebox, ttk
from tkinter.font import Font
from datetime import datetime

from ..db import MemoryDB
from ..services.auth import AuthService
from ..services.bargain import BargainService
from ..services.credit import CreditSystem
from ..services.notification import NotificationService
from ..services.order import OrderService
from ..services.payment import PaymentGateway
from ..services.product import ProductService
from ..services.recommend import RecommendationEngine


class SweetFishApp(tk.Tk):
    """甜鱼商城系统主应用"""

    def __init__(self, db: MemoryDB):
        super().__init__()
        self.title("🐟 甜鱼商城系统")
        self.geometry("1000x750")
        self.minsize(900, 600)
        self.db = db

        # 设置应用主题色 - 柔和现代配色
        self.colors = {
            "primary": "#2D6A4F",     # 主绿色
            "secondary": "#40916C",   # 次要绿色
            "accent": "#FF9E00",      # 强调橙色
            "light": "#F8F9FA",       # 浅背景
            "card": "#FFFFFF",        # 卡片背景
            "dark": "#212529",        # 深色文字
            "success": "#2E7D32",     # 成功绿
            "warning": "#ED6C02",     # 警告橙
            "error": "#D32F2F",       # 错误红
            "info": "#0288D1",        # 信息蓝
            "border": "#E0E0E0",      # 边框色
            "hover": "#F5F5F5",       # 悬停背景
        }

        # 设置字体
        self.fonts = {
            "title": ("Microsoft YaHei", 24, "bold"),
            "subtitle": ("Microsoft YaHei", 16, "bold"),
            "header": ("Microsoft YaHei", 14, "bold"),
            "normal": ("Microsoft YaHei", 11),
            "small": ("Microsoft YaHei", 10),
            "mono": ("Consolas", 10),  # 用于显示代码/ID
        }

        # 设置窗口图标和背景
        self.configure(bg=self.colors["light"])

        # 配置ttk样式
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.configure_styles()

        # 初始化服务
        self.notification = NotificationService(db)
        self.payment = PaymentGateway(db, self.notification)
        self.credit = CreditSystem(db)
        self.recommend = RecommendationEngine(db)
        self.auth = AuthService(db)
        self.prodsvc = ProductService(db)
        self.bargain = BargainService(db, self.notification)
        self.ordersvc = OrderService(
            db, self.payment, self.notification, self.credit, self.recommend
        )
        self.current_user = None
        self.active_frame = None

        # 设置窗口居中
        self.center_window()

        # 绑定关闭事件
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.show_login()

    def center_window(self):
        """将窗口居中显示"""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')

    def on_closing(self):
        """窗口关闭事件处理"""
        if messagebox.askokcancel("退出", "确定要退出甜鱼商城吗？"):
            self.destroy()

    def configure_styles(self):
        """配置ttk组件的样式"""

        # 配置基础框架样式
        self.style.configure(
            "Card.TFrame",
            background=self.colors["card"],
            relief="solid",
            borderwidth=1,
        )

        self.style.configure(
            "Elevated.TFrame",
            background=self.colors["card"],
            relief="solid",
            borderwidth=0,
        )

        # 配置标签样式
        self.style.configure(
            "Title.TLabel",
            font=self.fonts["title"],
            background=self.colors["light"],
            foreground=self.colors["primary"],
        )

        self.style.configure(
            "Subtitle.TLabel",
            font=self.fonts["subtitle"],
            background=self.colors["card"],
            foreground=self.colors["dark"],
        )

        self.style.configure(
            "Header.TLabel",
            font=self.fonts["header"],
            background=self.colors["card"],
            foreground=self.colors["primary"],
        )

        self.style.configure(
            "Muted.TLabel",
            font=self.fonts["small"],
            background=self.colors["card"],
            foreground="#6C757D",  # 灰色文字
        )

        self.style.configure(
            "Success.TLabel",
            font=self.fonts["small"],
            background=self.colors["card"],
            foreground=self.colors["success"],
        )

        self.style.configure(
            "Warning.TLabel",
            font=self.fonts["small"],
            background=self.colors["card"],
            foreground=self.colors["warning"],
        )

        self.style.configure(
            "Info.TLabel",
            font=self.fonts["small"],
            background=self.colors["card"],
            foreground=self.colors["info"],
        )

        # 配置按钮样式
        self.style.configure(
            "Primary.TButton",
            background=self.colors["primary"],
            foreground="white",
            font=self.fonts["normal"],
            padding=10,
            borderwidth=0,
            focusthickness=0,
            focuscolor="none"
        )
        self.style.map(
            "Primary.TButton",
            background=[
                ("active", self.colors["secondary"]),
                ("pressed", self.colors["primary"]),
                ("disabled", "#CCCCCC")
            ],
            foreground=[
                ("disabled", "#999999")
            ]
        )

        self.style.configure(
            "Secondary.TButton",
            background="white",
            foreground=self.colors["primary"],
            font=self.fonts["normal"],
            padding=8,
            borderwidth=1,
            relief="solid"
        )
        self.style.map(
            "Secondary.TButton",
            background=[
                ("active", self.colors["hover"]),
                ("pressed", "#E9ECEF")
            ]
        )

        self.style.configure(
            "Accent.TButton",
            background=self.colors["accent"],
            foreground="white",
            font=self.fonts["normal"],
            padding=10,
            borderwidth=0,
        )
        self.style.map(
            "Accent.TButton",
            background=[
                ("active", "#FFB74D"),
                ("pressed", self.colors["accent"])
            ]
        )

        # 配置输入框样式
        self.style.configure(
            "Modern.TEntry",
            fieldbackground="white",
            foreground=self.colors["dark"],
            borderwidth=1,
            relief="solid",
            padding=8,
        )
        self.style.map(
            "Modern.TEntry",
            fieldbackground=[
                ("focus", "white"),
                ("disabled", "#F8F9FA")
            ],
            bordercolor=[
                ("focus", self.colors["primary"]),
                ("invalid", self.colors["error"])
            ]
        )

        # 配置Treeview样式
        self.style.configure(
            "Treeview",
                background="white",
                foreground=self.colors["dark"],
                fieldbackground="white",
                borderwidth=0,
                rowheight=25
        )
        self.style.configure(
            "Treeview.Heading",
                background="#F8F9FA",
                foreground=self.colors["dark"],
                relief="flat",
                font=self.fonts["small"],
                padding=5
        )
        self.style.map(
            "Treeview.Heading",
                background=[("active", "#E9ECEF")]
        )

        self.style.configure(
            "Treeview.Treeitem",
                padding=5
        )
        self.style.map(
            "Treeview.Treeitem",
                background=[("selected", "#E8F5E9")]
        )

        # 配置滚动条样式
        self.style.configure(
            "Modern.Vertical.TScrollbar",
                background="#F8F9FA",
                darkcolor="#F8F9FA",
                lightcolor="#F8F9FA",
                troughcolor="#F8F9FA",
                bordercolor="#F8F9FA",
                arrowcolor=self.colors["dark"],
                gripcount=0
        )
        self.style.map(
            "Modern.Vertical.TScrollbar",
                background=[("active", "#E9ECEF")],
                arrowcolor=[("active", self.colors["primary"])]
        )

    def show_login(self):
        """切换到登录界面"""
        self.current_user = None  # 清除当前用户

        if self.active_frame:
            self.active_frame.destroy()

        self.active_frame = LoginFrame(self, self.auth)
        self.active_frame.pack(fill="both", expand=True, padx=40, pady=40)

    def show_main(self, user):
        """切换到主界面"""
        if self.active_frame:
            self.active_frame.destroy()

        self.current_user = user

        if user.role.name == "ADMIN":
            self.active_frame = AdminFrame(self, user)
        elif user.role.name == "MERCHANT":
            self.active_frame = MerchantFrame(self, user)
        else:
            self.active_frame = MainFrame(self, user)

        self.active_frame.pack(fill="both", expand=True, padx=20, pady=20)

    def show_register(self):
        """切换到注册界面"""
        if self.active_frame:
            self.active_frame.destroy()

        self.active_frame = RegisterFrame(self, self.auth)
        self.active_frame.pack(fill="both", expand=True, padx=40, pady=40)

    def logout(self):
        """登出当前用户"""
        if self.current_user:
            confirm = messagebox.askyesno(
                "确认退出",
                f"确定要退出账号 {self.current_user.name} 吗？",
                icon="question"
            )
            if confirm:
                self.show_login()


class LoginFrame(ttk.Frame):
    """登录界面"""

    def __init__(self, master: SweetFishApp, auth_service: AuthService):
        super().__init__(master, style="Card.TFrame")
        self.master_app = master
        self.auth = auth_service
        self.login_btn = None  # 初始化login_btn为None

        # 主容器
        container = ttk.Frame(self)
        container.pack(pady=30, padx=30)

        # 左侧品牌区域
        brand_frame = ttk.Frame(container)
        brand_frame.pack(side="left", fill="y", padx=(0, 50))

        # 品牌标识
        brand_inner = ttk.Frame(brand_frame)
        brand_inner.pack(pady=50)

        ttk.Label(
            brand_inner,
            text="🐟",
            font=("Segoe UI Emoji", 72),
            foreground=master.colors["primary"]
        ).pack()

        ttk.Label(
            brand_inner,
            text="甜鱼商城",
            style="Title.TLabel"
        ).pack(pady=(10, 5))

        ttk.Label(
            brand_inner,
            text="让闲置物品找到新主人",
            font=master.fonts["normal"],
            foreground=master.colors["dark"],
            wraplength=200
        ).pack()

        # 右侧登录表单
        form_frame = ttk.Frame(container, style="Card.TFrame")
        form_frame.pack(side="right", fill="both", expand=True, ipadx=30, ipady=30)

        # 表单标题
        title_frame = ttk.Frame(form_frame)
        title_frame.pack(pady=(0, 30))

        ttk.Label(
            title_frame,
            text="欢迎回来",
            style="Subtitle.TLabel"
        ).pack()

        ttk.Label(
            title_frame,
            text="请登录您的账户",
            font=master.fonts["normal"],
            foreground="#6C757D"
        ).pack(pady=(5, 0))

        # 表单字段
        form_inner = ttk.Frame(form_frame)
        form_inner.pack(fill="x", padx=20)

        # 手机号输入
        phone_frame = ttk.Frame(form_inner)
        phone_frame.pack(fill="x", pady=(0, 20))

        ttk.Label(
            phone_frame,
            text="手机号",
            font=master.fonts["small"],
            foreground=master.colors["dark"]
        ).pack(anchor="w", pady=(0, 5))

        self.phone_entry = ttk.Entry(
            phone_frame,
            style="Modern.TEntry",
            font=master.fonts["normal"],
            width=30
        )
        self.phone_entry.pack(fill="x", ipady=10)
        self.phone_entry.bind("<Return>", lambda e: self.login())

        # 密码输入
        pass_frame = ttk.Frame(form_inner)
        pass_frame.pack(fill="x", pady=(0, 30))

        ttk.Label(
            pass_frame,
            text="密码",
            font=master.fonts["small"],
            foreground=master.colors["dark"]
        ).pack(anchor="w", pady=(0, 5))

        self.pass_entry = ttk.Entry(
            pass_frame,
            style="Modern.TEntry",
            font=master.fonts["normal"],
            show="●",
            width=30
        )
        self.pass_entry.pack(fill="x", ipady=10)
        self.pass_entry.bind("<Return>", lambda e: self.login())

        # 按钮区域
        btn_frame = ttk.Frame(form_inner)
        btn_frame.pack(fill="x")

        self.login_btn = ttk.Button(
            btn_frame,
            text="登录",
            style="Primary.TButton",
            command=self.login
        )
        self.login_btn.pack(fill="x", pady=(0, 15))

        # 注册链接
        register_frame = ttk.Frame(btn_frame)
        register_frame.pack()

        ttk.Label(
            register_frame,
            text="还没有账户？",
            font=master.fonts["small"],
            foreground="#6C757D"
        ).pack(side="left")

        ttk.Button(
            register_frame,
            text="立即注册",
            style="Secondary.TButton",
            command=self.register
        ).pack(side="left", padx=(5, 0))

        # 设置焦点
        self.phone_entry.focus_set()

    def login(self):
        """执行登录操作"""
        phone = self.phone_entry.get().strip()
        password = self.pass_entry.get().strip()

        if not phone or not password:
            messagebox.showwarning("输入错误", "请填写手机号和密码")
            return

        # 禁用登录按钮
        if self.login_btn and self.login_btn.winfo_exists():
            self.login_btn.config(state="disabled")
        self.update_idletasks()

        try:
            user = self.auth.authenticate(phone, password)
            if user:
                messagebox.showinfo("登录成功", f"欢迎回来，{user.name}！")
                # 延迟切换界面，避免Tkinter回调问题
                self.after(100, lambda: self.master_app.show_main(user))
            else:
                messagebox.showerror("登录失败", "手机号或密码错误，请重试")
                # 重新启用登录按钮
                if self.login_btn and self.login_btn.winfo_exists():
                    self.login_btn.config(state="normal")
        except Exception as e:
            messagebox.showerror("登录错误", f"登录过程中发生错误：\n{str(e)}")
            # 重新启用登录按钮
            if self.login_btn and self.login_btn.winfo_exists():
                self.login_btn.config(state="normal")

    def register(self):
        """跳转到完整注册页面"""
        self.master_app.show_register()


class MainFrame(ttk.Frame):
    """主用户界面"""

    def __init__(self, master: SweetFishApp, user):
        super().__init__(master)
        self.master_app = master
        self.user = user
        self.prodsvc = master.prodsvc
        self.ordersvc = master.ordersvc
        self.notification = master.notification

        # 当前视图模式：'products' 或 'orders'
        self.current_view = 'products'

        # 创建主布局
        self.setup_ui()
        self.populate_demo_data()
        self.load_user_orders()  # 新增：加载用户订单

    def setup_ui(self):
        """设置用户界面"""

        # 创建主容器
        main_container = ttk.Frame(self)
        main_container.pack(fill="both", expand=True)

        # 顶部导航栏
        self.create_top_bar(main_container)

        # 主内容区域
        content_container = ttk.Frame(main_container)
        content_container.pack(fill="both", expand=True, pady=(10, 0))

        # 左侧边栏
        self.create_sidebar(content_container)

        # 中间主显示区域（商品/订单）
        self.create_main_display_section(content_container)

    def create_top_bar(self, parent):
        """创建顶部导航栏"""
        top_bar = ttk.Frame(parent, style="Card.TFrame")
        top_bar.pack(fill="x", pady=(0, 10))

        # 左侧用户信息
        user_info_frame = ttk.Frame(top_bar)
        user_info_frame.pack(side="left", padx=20, pady=15)

        # 用户头像和名称
        avatar_frame = ttk.Frame(user_info_frame)
        avatar_frame.pack(side="left")

        # 模拟头像
        avatar_label = ttk.Label(
            avatar_frame,
            text="👤",
            font=("Segoe UI Emoji", 24),
            background=self.master_app.colors["light"]
        )
        avatar_label.pack(padx=(0, 10))

        # 用户详情
        user_details = ttk.Frame(user_info_frame)
        user_details.pack(side="left")

        ttk.Label(
            user_details,
            text=self.user.name,
            font=self.master_app.fonts["header"],
            foreground=self.master_app.colors["primary"]
        ).pack(anchor="w")

        ttk.Label(
            user_details,
            text=f"普通用户 • ID: {self.user.user_id}",
            font=self.master_app.fonts["small"],
            foreground="#6C757D"
        ).pack(anchor="w", pady=(2, 0))

        # 右侧操作按钮
        action_frame = ttk.Frame(top_bar)
        action_frame.pack(side="right", padx=20, pady=15)

        # 视图切换按钮
        view_btn = ttk.Button(
            action_frame,
            text="📋 查看订单" if self.current_view == 'products' else "🛍️ 查看商品",
            style="Secondary.TButton",
            command=self.toggle_view,
            width=12
        )
        view_btn.pack(side="left", padx=(0, 10))

        # 通知按钮
        notif_btn = ttk.Button(
            action_frame,
            text="🔔 通知",
            style="Secondary.TButton",
            command=self.show_notifications,
            width=10
        )
        notif_btn.pack(side="left", padx=(0, 10))

        # 登出按钮
        logout_btn = ttk.Button(
            action_frame,
            text="退出登录",
            style="Secondary.TButton",
            command=self.master_app.logout,
            width=10
        )
        logout_btn.pack(side="left")

    def create_sidebar(self, parent):
        """创建左侧边栏"""
        sidebar = ttk.Frame(parent, style="Card.TFrame", width=250)
        sidebar.pack(side="left", fill="y", padx=(0, 10))
        sidebar.pack_propagate(False)  # 固定宽度

        sidebar_inner = ttk.Frame(sidebar, padding=20)
        sidebar_inner.pack(fill="both", expand=True)

        # 搜索区域
        search_card = ttk.Frame(sidebar_inner, style="Card.TFrame")
        search_card.pack(fill="x", pady=(0, 20))

        search_inner = ttk.Frame(search_card, padding=15)
        search_inner.pack(fill="x")

        ttk.Label(
            search_inner,
            text="🔍 搜索",
            style="Header.TLabel"
        ).pack(anchor="w", pady=(0, 10))

        # 搜索输入框
        search_input_frame = ttk.Frame(search_inner)
        search_input_frame.pack(fill="x", pady=(0, 10))

        self.search_entry = ttk.Entry(
            search_input_frame,
            style="Modern.TEntry",
            font=self.master_app.fonts["normal"]
        )
        self.search_entry.pack(fill="x", side="left", expand=True, ipady=8)
        self.search_entry.bind("<Return>", lambda e: self.search_products())

        # 搜索按钮
        search_btn = ttk.Button(
            search_input_frame,
            text="搜索",
            style="Primary.TButton",
            command=self.search_products,
            width=8
        )
        search_btn.pack(side="right", padx=(5, 0))

        # 快速操作区域
        actions_card = ttk.Frame(sidebar_inner, style="Card.TFrame")
        actions_card.pack(fill="x")

        actions_inner = ttk.Frame(actions_card, padding=15)
        actions_inner.pack(fill="x")

        ttk.Label(
            actions_inner,
            text="⚡ 快速操作",
            style="Header.TLabel"
        ).pack(anchor="w", pady=(0, 15))

        # 根据当前视图显示不同的操作按钮
        if self.current_view == 'products':
            actions = [
                ("📝 创建订单", self.create_order_from_selection, "Primary.TButton"),
                ("🔄 刷新列表", self.refresh_products, "Secondary.TButton"),
                ("📊 我的统计", self.show_stats, "Secondary.TButton"),
            ]
        else:
            actions = [
                ("💳 支付订单", self.pay_selected_order, "Accent.TButton"),
                ("🔄 刷新列表", self.load_user_orders, "Secondary.TButton"),
                ("📊 订单统计", self.show_order_stats, "Secondary.TButton"),
            ]

        for text, command, style_name in actions:
            btn = ttk.Button(
                actions_inner,
                text=text,
                style=style_name,
                command=command
            )
            btn.pack(fill="x", pady=5)

    def create_main_display_section(self, parent):
        """创建主显示区域（商品或订单）"""
        self.main_display = ttk.Frame(parent, style="Card.TFrame")
        self.main_display.pack(side="left", fill="both", expand=True)

        # 创建标题栏
        self.display_header = ttk.Frame(self.main_display, padding=20)
        self.display_header.pack(fill="x")

        self.display_title = ttk.Label(
            self.display_header,
            text="",
            style="Header.TLabel"
        )
        self.display_title.pack(side="left")

        # 创建表格容器
        self.table_container = ttk.Frame(self.main_display)
        self.table_container.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        # 根据当前视图初始化显示内容
        self.update_display_view()

    def update_display_view(self):
        """更新显示区域的内容"""
        # 清除现有内容
        for widget in self.display_header.winfo_children():
            if widget != self.display_title:
                widget.destroy()

        for widget in self.table_container.winfo_children():
            widget.destroy()

        # 更新标题
        if self.current_view == 'products':
            self.display_title.config(text="🛍️ 所有商品")
            self.create_product_table()
        else:
            self.display_title.config(text="📋 我的订单")
            self.create_order_table()

    def create_product_table(self):
        """创建商品表格"""
        # 刷新按钮
        refresh_btn = ttk.Button(
            self.display_header,
            text="🔄 刷新",
            style="Secondary.TButton",
            command=self.refresh_products,
            width=10
        )
        refresh_btn.pack(side="right")

        # 创建滚动条
        scrollbar_y = ttk.Scrollbar(self.table_container, style="Modern.Vertical.TScrollbar")
        scrollbar_y.pack(side="right", fill="y")

        scrollbar_x = ttk.Scrollbar(self.table_container, orient="horizontal")
        scrollbar_x.pack(side="bottom", fill="x")

        # 创建Treeview
        self.product_tree = ttk.Treeview(
            self.table_container,
            columns=("title", "price", "stock", "merchant", "status"),
            show="headings",
            selectmode="browse",
            yscrollcommand=scrollbar_y.set,
            xscrollcommand=scrollbar_x.set,
            style="Treeview"
        )

        # 配置列
        columns = [
            ("title", "商品名称", 200),
            ("price", "价格(元)", 100),
            ("stock", "库存", 80),
            ("merchant", "商家", 120),
            ("status", "状态", 100),
        ]

        for col_id, text, width in columns:
            self.product_tree.heading(col_id, text=text, anchor="w")
            self.product_tree.column(col_id, width=width, minwidth=width, anchor="w")

        self.product_tree.pack(side="left", fill="both", expand=True)

        scrollbar_y.config(command=self.product_tree.yview)
        scrollbar_x.config(command=self.product_tree.xview)

        # 绑定双击事件
        self.product_tree.bind("<Double-Button-1>", lambda e: self.create_order_from_selection())

    def create_order_table(self):
        """创建订单表格"""
        # 刷新按钮
        refresh_btn = ttk.Button(
            self.display_header,
            text="🔄 刷新",
            style="Secondary.TButton",
            command=self.load_user_orders,
            width=10
        )
        refresh_btn.pack(side="right")

        # 创建滚动条
        order_scrollbar = ttk.Scrollbar(self.table_container, style="Modern.Vertical.TScrollbar")
        order_scrollbar.pack(side="right", fill="y")

        # 创建Treeview
        self.order_tree = ttk.Treeview(
            self.table_container,
            columns=("id", "product", "total", "status", "date"),
            show="headings",
            selectmode="browse",
            yscrollcommand=order_scrollbar.set,
            style="Treeview"
        )

        # 配置列
        order_columns = [
            ("id", "订单号", 120),
            ("product", "商品", 150),
            ("total", "总金额", 100),
            ("status", "状态", 100),
            ("date", "日期", 120),
        ]

        for col_id, text, width in order_columns:
            self.order_tree.heading(col_id, text=text, anchor="w")
            self.order_tree.column(col_id, width=width, minwidth=width, anchor="w")

        self.order_tree.pack(side="left", fill="both", expand=True)
        order_scrollbar.config(command=self.order_tree.yview)

        # 绑定双击事件
        self.order_tree.bind("<Double-Button-1>", lambda e: self.pay_selected_order())

    def toggle_view(self):
        """切换视图模式"""
        if self.current_view == 'products':
            self.current_view = 'orders'
        else:
            self.current_view = 'products'

        # 重新创建边栏和主显示区域
        for widget in self.winfo_children():
            widget.destroy()
        self.setup_ui()
        self.load_user_orders() if self.current_view == 'orders' else self.refresh_products()

    def load_user_orders(self):
        """加载当前用户的订单"""
        if not hasattr(self, 'order_tree'):
            return

        # 清空现有数据
        for row in self.order_tree.get_children():
            self.order_tree.delete(row)

        # 获取当前用户的所有订单
        user_orders = []
        for order in self.master_app.db.orders.values():
            if hasattr(order, 'buyer_id') and order.buyer_id == self.user.user_id:
                user_orders.append(order)

        # 按创建时间倒序排序
        user_orders.sort(key=lambda x: x.created_at if hasattr(x, 'created_at') else "", reverse=True)

        for order in user_orders:
            # 获取商品信息
            product_names = []
            for item in order.items:
                product = self.master_app.db.get_product(item.product_id)
                if product:
                    product_names.append(product.title)

            # 格式化日期
            if hasattr(order, 'created_at'):
                order_date = order.created_at.strftime("%Y-%m-%d")
            else:
                order_date = "未知日期"

            # 确定订单状态样式
            status = order.status.value
            if status == "PAID":
                status_tag = "paid"
            elif status == "PENDING":
                status_tag = "pending"
            elif status == "FAILED":
                status_tag = "failed"
            else:
                status_tag = "other"

            self.order_tree.insert(
                "", "end",
                iid=order.order_id,
                values=(
                    order.order_id,
                    ", ".join(product_names[:2]) + ("..." if len(product_names) > 2 else ""),
                    f"¥{order.total_cents / 100:.2f}",
                    status,
                    order_date
                ),
                tags=(status_tag,)
            )

        # 设置标签样式
        self.order_tree.tag_configure("paid", foreground="#28A745")  # 绿色
        self.order_tree.tag_configure("pending", foreground="#FFC107")  # 黄色
        self.order_tree.tag_configure("failed", foreground="#DC3545")  # 红色
        self.order_tree.tag_configure("other", foreground="#6C757D")  # 灰色

    def populate_demo_data(self):
        """加载示例数据"""
        # 创建示例商家（如果不存在）
        merchant_phone = "13800000002"

        # 检查商家是否已存在
        existing_merchant = self.master_app.db.get_user_by_phone(merchant_phone)

        if not existing_merchant:
            try:
                # 使用auth服务的register方法创建商家
                merchant = self.master_app.auth.register(merchant_phone, "bobpwd", "MERCHANT")

                # 由于register方法使用phone作为name，我们需要更新商家的name和shop_name
                merchant.name = "Bob"
                # 检查是否是Merchant类型（有shop_name属性）
                if hasattr(merchant, 'shop_name'):
                    merchant.shop_name = "Bob's Shop"
                m = merchant
            except Exception as e:
                # 如果注册失败，使用一个默认的商家ID
                print(f"注册商家失败: {e}")
                # 创建一个虚拟的商家对象用于演示
                from ..models import Merchant
                m = Merchant(
                    user_id="m_demo_001",
                    phone=merchant_phone,
                    name="Bob",
                    password_hash="",
                    shop_name="Bob's Shop"
                )
        else:
            m = existing_merchant

        # 创建示例商品（如果不存在）
        if not self.master_app.db.products:
            products_data = [
                (m.user_id, "复古台灯", "温暖氛围的复古风格台灯", 1999, 3, {"lamp", "复古"}),
                (m.user_id, "二手iPhone 12", "九成新，功能完好", 8999, 5, {"手机", "数码", "苹果"}),
                (m.user_id, "MacBook Air", "轻薄本，适合办公学习", 32999, 2, {"电脑", "数码", "苹果"}),
                (m.user_id, "实木书架", "优质实木制作，坚固耐用", 4999, 1, {"家具", "实木", "收纳"}),
                (m.user_id, "无线耳机", "全新未拆封，蓝牙5.0", 1299, 8, {"数码", "耳机", "音频"}),
                (m.user_id, "Python编程书籍", "经典编程教材，九五新", 499, 4, {"书籍", "编程", "教育"}),
            ]

            for data in products_data:
                try:
                    self.prodsvc.create_product(*data)
                except Exception as e:
                    print(f"创建商品失败: {e}")

        self.refresh_products()

    def refresh_products(self, products=None):
        """刷新商品列表"""
        # 确保product_tree存在
        if not hasattr(self, 'product_tree'):
            return

        # 清空现有数据
        for row in self.product_tree.get_children():
            self.product_tree.delete(row)

        products = products or list(self.master_app.db.products.values())

        for p in products:
            merchant = self.master_app.db.get_user_by_id(p.merchant_id)
            merchant_name = merchant.name if merchant else "未知商家"

            # 确定商品状态
            if p.stock <= 0:
                status = "缺货"
                status_tag = "out_of_stock"
            elif p.stock < 3:
                status = "库存紧张"
                status_tag = "low_stock"
            else:
                status = "有货"
                status_tag = "in_stock"

            self.product_tree.insert(
                "", "end",
                iid=p.product_id,
                values=(
                    p.title,
                    f"¥{p.price_cents / 100:.2f}",
                    p.stock,
                    merchant_name,
                    status
                ),
                tags=(status_tag,)
            )

        # 设置标签样式
        self.product_tree.tag_configure("out_of_stock", foreground="#DC3545")  # 红色
        self.product_tree.tag_configure("low_stock", foreground="#FFC107")  # 黄色
        self.product_tree.tag_configure("in_stock", foreground="#28A745")  # 绿色

    def search_products(self):
        """搜索商品"""
        keyword = self.search_entry.get().strip()
        if not keyword:
            self.refresh_products()
        else:
            results = self.prodsvc.search(keyword)
            self.refresh_products(results)

    def create_order_from_selection(self):
        """从选择创建订单"""
        if not hasattr(self, 'product_tree'):
            return

        selection = self.product_tree.selection()
        if not selection:
            messagebox.showwarning(
                "未选择商品",
                "请先在商品列表中选择一个商品",
                icon="warning"
            )
            return

        product_id = selection[0]
        product = self.master_app.db.get_product(product_id)

        if product.stock <= 0:
            messagebox.showerror(
                "库存不足",
                "抱歉，该商品已售罄，请选择其他商品",
                icon="error"
            )
            return

        # 创建确认对话框
        confirm_msg = f"""
        确认购买以下商品：

        商品名称：{product.title}
        商品价格：¥{product.price_cents / 100:.2f}
        商家：{self.master_app.db.get_user_by_id(product.merchant_id).name}
        当前库存：{product.stock}

        确定要下单吗？
        """

        confirm = messagebox.askyesno(
            "确认下单",
            confirm_msg,
            icon="question"
        )

        if not confirm:
            return

        try:
            # 创建订单
            order = self.ordersvc.create_order(self.user.user_id, [(product_id, 1)])

            # 显示成功消息
            messagebox.showinfo(
                "下单成功",
                f"""
                ✅ 订单创建成功！

                订单号：{order.order_id}
                商品名称：{product.title}
                总金额：¥{order.total_cents / 100:.2f}
                订单状态：{order.status.value}

                请及时支付订单。
                """
            )

            # 刷新商品列表和订单列表
            self.refresh_products()
            if hasattr(self, 'order_tree'):
                self.load_user_orders()

            # 提示切换到订单视图
            if self.current_view == 'products':
                if messagebox.askyesno("查看订单", "订单创建成功！是否切换到订单视图查看？"):
                    self.current_view = 'orders'
                    for widget in self.winfo_children():
                        widget.destroy()
                    self.setup_ui()
                    self.load_user_orders()

        except Exception as e:
            messagebox.showerror(
                "下单失败",
                f"创建订单时出错：\n\n{str(e)}",
                icon="error"
            )

    def pay_selected_order(self):
        """支付选中订单"""
        if not hasattr(self, 'order_tree'):
            return

        selection = self.order_tree.selection()
        if not selection:
            messagebox.showwarning(
                "未选择订单",
                "请先在订单列表中选择一个订单进行支付",
                icon="warning"
            )
            return

        order_id = selection[0]
        order = self.master_app.db.get_order(order_id)

        if order.status.value == "PAID":
            messagebox.showinfo(
                "订单已支付",
                "该订单已完成支付，无需重复支付",
                icon="info"
            )
            return

        # 创建确认对话框
        confirm_msg = f"""
        确认支付以下订单：

        订单号：{order_id}
        支付金额：¥{order.total_cents / 100:.2f}
        当前状态：{order.status.value}

        确定要支付吗？
        """

        confirm = messagebox.askyesno(
            "确认支付",
            confirm_msg,
            icon="question"
        )

        if not confirm:
            return

        try:
            # 执行支付
            payment_result = self.ordersvc.pay_order(order_id, succeed_rate=0.98)

            # 刷新订单列表
            self.load_user_orders()

            if payment_result.status.upper() == "SUCCESS":
                messagebox.showinfo(
                    "支付成功",
                    f"""
                    ✅ 支付成功！

                    订单号：{order_id}
                    支付金额：¥{order.total_cents / 100:.2f}
                    支付时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

                    感谢您的购买！
                    """
                )
            else:
                messagebox.showerror(
                    "支付失败",
                    f"❌ 支付失败：{payment_result.status}\n\n请稍后重试或联系客服。",
                    icon="error"
                )

        except Exception as e:
            messagebox.showerror(
                "支付错误",
                f"支付过程中出错：\n\n{str(e)}",
                icon="error"
            )

    def show_notifications(self):
        """显示通知"""
        notes = self.notification.get_notifications_for_user(self.user.user_id)

        # 创建通知窗口
        notif_window = tk.Toplevel(self)
        notif_window.title("🔔 我的通知")
        notif_window.geometry("500x600")
        notif_window.configure(bg="white")

        # 使通知窗口居中
        notif_window.transient(self)
        notif_window.grab_set()

        x = self.winfo_x() + (self.winfo_width() // 2) - 250
        y = self.winfo_y() + (self.winfo_height() // 2) - 300
        notif_window.geometry(f"+{x}+{y}")

        # 标题栏
        title_frame = ttk.Frame(notif_window, style="Card.TFrame")
        title_frame.pack(fill="x", pady=(20, 10), padx=20)

        ttk.Label(
            title_frame,
            text=f"🔔 通知中心",
            font=self.master_app.fonts["header"],
            foreground=self.master_app.colors["primary"]
        ).pack(pady=10)

        # 通知数量
        count_label = ttk.Label(
            title_frame,
            text=f"共 {len(notes)} 条通知",
            font=self.master_app.fonts["small"],
            foreground="#6C757D"
        )
        count_label.pack(pady=(0, 10))

        # 通知列表容器
        list_container = ttk.Frame(notif_window)
        list_container.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        # 创建Canvas用于滚动
        canvas = tk.Canvas(list_container, bg="white", highlightthickness=0)
        scrollbar = ttk.Scrollbar(list_container, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # 显示通知
        if not notes:
            empty_frame = ttk.Frame(scrollable_frame, padding=30)
            empty_frame.pack(fill="x", pady=20)

            ttk.Label(
                empty_frame,
                text="📭",
                font=("Segoe UI Emoji", 48),
                foreground="#D0D0D0"
            ).pack()

            ttk.Label(
                empty_frame,
                text="暂无通知",
                font=self.master_app.fonts["normal"],
                foreground="#6C757D"
            ).pack(pady=10)
        else:
            for i, (message, timestamp) in enumerate(reversed(notes[-20:])):  # 只显示最近20条
                # 创建通知卡片
                note_card = ttk.Frame(
                    scrollable_frame,
                    style="Card.TFrame",
                    padding=15
                )
                note_card.pack(fill="x", pady=5)

                # 通知内容
                content_frame = ttk.Frame(note_card)
                content_frame.pack(fill="x")

                # 通知图标
                icon_label = ttk.Label(
                    content_frame,
                    text="📢",
                    font=("Segoe UI Emoji", 16)
                )
                icon_label.pack(side="left", padx=(0, 10))

                # 通知文本和时间
                text_frame = ttk.Frame(content_frame)
                text_frame.pack(side="left", fill="x", expand=True)

                ttk.Label(
                    text_frame,
                    text=message,
                    font=self.master_app.fonts["normal"],
                    wraplength=350,
                    justify="left"
                ).pack(anchor="w")

                ttk.Label(
                    text_frame,
                    text=timestamp.strftime("%Y-%m-%d %H:%M"),
                    font=self.master_app.fonts["small"],
                    foreground="#6C757D"
                ).pack(anchor="w", pady=(5, 0))

        # 布局Canvas和Scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # 绑定鼠标滚轮事件 - 使用安全的方式
        def _on_mousewheel(event):
            try:
                canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
            except tk.TclError:
                # Canvas已经被销毁，忽略这个事件
                pass

        # 只绑定到当前窗口，而不是整个应用
        notif_window.bind("<MouseWheel>", _on_mousewheel)

        # 关闭按钮
        btn_frame = ttk.Frame(notif_window)
        btn_frame.pack(fill="x", padx=20, pady=(0, 20))

        ttk.Button(
            btn_frame,
            text="关闭",
            style="Primary.TButton",
            command=notif_window.destroy
        ).pack()

    def show_stats(self):
        """显示用户统计"""
        # 获取统计数据 - 修复：使用buyer_id而不是user_id
        total_orders = len([o for o in self.master_app.db.orders.values()
                            if hasattr(o, 'buyer_id') and o.buyer_id == self.user.user_id])

        total_spent = sum([o.total_cents for o in self.master_app.db.orders.values()
                           if hasattr(o, 'buyer_id') and o.buyer_id == self.user.user_id and o.status.value == "PAID"])

        active_orders = len([o for o in self.master_app.db.orders.values()
                             if
                             hasattr(o, 'buyer_id') and o.buyer_id == self.user.user_id and o.status.value != "PAID"])

        # 显示统计信息
        stats_msg = f"""
        📊 我的统计

        用户信息：
        • 用户名：{self.user.name}
        • 用户ID：{self.user.user_id}
        • 注册时间：2024-01-01（示例）

        交易统计：
        • 总订单数：{total_orders} 笔
        • 已支付订单：{total_orders - active_orders} 笔
        • 待支付订单：{active_orders} 笔
        • 总消费金额：¥{total_spent / 100:.2f}

        其他信息：
        • 信用积分：{self.master_app.credit.get_score(self.user.user_id)}
        • 未读通知：{len(self.notification.get_notifications_for_user(self.user.user_id))} 条
        """

        messagebox.showinfo("我的统计", stats_msg)

    def show_order_stats(self):
        """显示订单统计"""
        # 获取用户的所有订单
        user_orders = []
        for order in self.master_app.db.orders.values():
            if hasattr(order, 'buyer_id') and order.buyer_id == self.user.user_id:
                user_orders.append(order)

        total_orders = len(user_orders)
        paid_orders = len([o for o in user_orders if o.status.value == "PAID"])
        pending_orders = len([o for o in user_orders if o.status.value == "PENDING"])
        total_spent = sum([o.total_cents for o in user_orders if o.status.value == "PAID"])

        stats_msg = f"""
        📊 订单统计

        订单总数：{total_orders} 笔
        已支付订单：{paid_orders} 笔
        待支付订单：{pending_orders} 笔
        总消费金额：¥{total_spent / 100:.2f}

        最近订单：
        """

        # 显示最近5个订单
        recent_orders = sorted(user_orders,
                               key=lambda x: x.created_at if hasattr(x, 'created_at') else "",
                               reverse=True)[:5]

        for i, order in enumerate(recent_orders, 1):
            product_names = []
            for item in order.items:
                product = self.master_app.db.get_product(item.product_id)
                if product:
                    product_names.append(product.title[:10])

            order_date = order.created_at.strftime("%Y-%m-%d") if hasattr(order, 'created_at') else "未知日期"
            stats_msg += f"\n{i}. {order.order_id[:8]}... - {', '.join(product_names)} - ¥{order.total_cents / 100:.2f} - {order.status.value} - {order_date}"

        messagebox.showinfo("订单统计", stats_msg)

class AdminFrame(ttk.Frame):
    """管理员界面"""

    def __init__(self, master: SweetFishApp, user):
        super().__init__(master)
        self.master_app = master
        self.user = user
        self._mousewheel_binding = None  # 用于存储鼠标滚轮事件绑定

        # 创建主布局
        self.setup_ui()

    def setup_ui(self):
        """设置管理员界面"""

        # 创建主容器
        main_container = ttk.Frame(self)
        main_container.pack(fill="both", expand=True)

        # 顶部导航栏
        self.create_top_bar(main_container)

        # 创建带滚动条的主内容区域
        self.create_scrollable_content(main_container)

    def create_top_bar(self, parent):
        """创建顶部导航栏"""
        top_bar = ttk.Frame(parent, style="Card.TFrame")
        top_bar.pack(fill="x", pady=(0, 10))

        # 左侧用户信息
        user_info_frame = ttk.Frame(top_bar)
        user_info_frame.pack(side="left", padx=20, pady=15)

        # 用户头像和名称
        avatar_frame = ttk.Frame(user_info_frame)
        avatar_frame.pack(side="left")

        # 模拟头像
        avatar_label = ttk.Label(
            avatar_frame,
            text="👑",
            font=("Segoe UI Emoji", 24),
            background=self.master_app.colors["light"]
        )
        avatar_label.pack(padx=(0, 10))

        # 用户详情
        user_details = ttk.Frame(user_info_frame)
        user_details.pack(side="left")

        ttk.Label(
            user_details,
            text=self.user.name,
            font=self.master_app.fonts["header"],
            foreground=self.master_app.colors["primary"]
        ).pack(anchor="w")

        ttk.Label(
            user_details,
            text=f"管理员 • ID: {self.user.user_id}",
            font=self.master_app.fonts["small"],
            foreground="#6C757D"
        ).pack(anchor="w", pady=(2, 0))

        # 右侧操作按钮
        action_frame = ttk.Frame(top_bar)
        action_frame.pack(side="right", padx=20, pady=15)

        # 登出按钮
        logout_btn = ttk.Button(
            action_frame,
            text="退出登录",
            style="Secondary.TButton",
            command=self.master_app.logout,
            width=10
        )
        logout_btn.pack(side="left")

    def create_scrollable_content(self, parent):
        """创建带滚动条的内容区域"""
        # 创建Canvas和滚动条
        self.canvas = tk.Canvas(parent, bg=self.master_app.colors["light"], highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(parent, orient="vertical", command=self.canvas.yview, style="Modern.Vertical.TScrollbar")

        # 创建可滚动的内部框架
        self.scrollable_frame = ttk.Frame(self.canvas, style="Card.TFrame")

        # 配置Canvas
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        # 在Canvas中创建窗口
        self.canvas_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        # 配置Canvas滚动
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # 布局Canvas和滚动条
        self.canvas.pack(side="left", fill="both", expand=True, padx=(20, 0), pady=20)
        self.scrollbar.pack(side="right", fill="y", padx=(0, 20), pady=20)

        # 绑定鼠标滚轮事件 - 使用安全的方式
        def _on_mousewheel(event):
            try:
                if hasattr(self, 'canvas') and self.canvas.winfo_exists():
                    self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
            except tk.TclError:
                # Canvas已经被销毁，忽略这个事件
                pass

        # 绑定鼠标滚轮事件到Canvas
        self._mousewheel_binding = self.canvas.bind("<MouseWheel>", _on_mousewheel)

        # 确保Canvas窗口宽度跟随Canvas调整
        def configure_canvas_window(event):
            if hasattr(self, 'canvas') and self.canvas.winfo_exists():
                self.canvas.itemconfig(self.canvas_window, width=event.width)

        self.canvas.bind("<Configure>", configure_canvas_window)

        # 创建管理员控制面板
        self.create_admin_panel()

    def destroy(self):
        """重写destroy方法以解除事件绑定"""
        # 解除鼠标滚轮事件绑定
        if hasattr(self, '_mousewheel_binding') and self._mousewheel_binding:
            try:
                self.canvas.unbind("<MouseWheel>", self._mousewheel_binding)
            except:
                pass

        # 调用父类的destroy方法
        super().destroy()

    def create_admin_panel(self):
        """创建管理员控制面板"""
        # 主内容容器
        container = ttk.Frame(self.scrollable_frame)
        container.pack(pady=20, padx=20, fill="both", expand=True)

        container_inner = ttk.Frame(container)
        container_inner.pack(pady=20, padx=20, fill="both", expand=True)

        # 标题区域
        title_frame = ttk.Frame(container_inner)
        title_frame.pack(pady=(0, 30))

        ttk.Label(
            title_frame,
            text="👑 甜鱼商城管理系统",
            style="Title.TLabel"
        ).pack()

        ttk.Label(
            title_frame,
            text="管理员控制面板",
            font=self.master_app.fonts["normal"],
            foreground=self.master_app.colors["dark"]
        ).pack(pady=(5, 0))

        # 管理员信息
        info_card = ttk.Frame(container_inner, style="Card.TFrame")
        info_card.pack(fill="x", pady=(0, 30), ipady=15, ipadx=15)

        ttk.Label(
            info_card,
            text=f"当前登录：{self.user.name}",
            font=self.master_app.fonts["header"],
            foreground=self.master_app.colors["primary"]
        ).pack(anchor="w")

        ttk.Label(
            info_card,
            text="管理员ID：" + str(self.user.user_id),
            font=self.master_app.fonts["small"],
            foreground=self.master_app.colors["dark"]
        ).pack(anchor="w", pady=(2, 0))

        # 统计卡片区域
        stats_frame = ttk.Frame(container_inner)
        stats_frame.pack(fill="x", pady=(0, 30))

        # 创建统计卡片
        stats_data = [
            ("👥 用户总数", len(self.master_app.db.users), self.master_app.colors["primary"]),
            ("🛍️ 商品总数", len(self.master_app.db.products), self.master_app.colors["secondary"]),
            ("📋 订单总数", len(self.master_app.db.orders), self.master_app.colors["accent"]),
            ("🔔 通知总数", len(self.master_app.db.notifications), self.master_app.colors["success"]),
        ]

        for i, (title, count, color) in enumerate(stats_data):
            card = self.create_stat_card(stats_frame, title, count, color)
            if i < 2:
                card.grid(row=0, column=i, padx=(0, 15), pady=5, sticky="ew")
            else:
                card.grid(row=1, column=i-2, padx=(0, 15), pady=(15, 0), sticky="ew")

        # 操作按钮区域
        action_frame = ttk.Frame(container_inner)
        action_frame.pack(fill="x", pady=(0, 20))

        ttk.Label(
            action_frame,
            text="系统操作",
            style="Header.TLabel"
        ).pack(anchor="w", pady=(0, 15))

        # 操作按钮
        operations = [
            ("📊 查看用户统计", self.show_user_count),
            ("📦 查看商品统计", self.show_product_count),
            ("📈 查看订单统计", self.show_order_count),
            ("📢 查看通知统计", self.show_notifications),
            ("🔍 查看系统日志", self.show_system_logs),
            ("⚙️ 系统设置", self.show_system_settings),
        ]

        for text, command in operations:
            btn = ttk.Button(
                action_frame,
                text=text,
                command=command,
                style="Secondary.TButton"
            )
            btn.pack(fill="x", pady=5, ipady=10)

        # 底部说明
        bottom_frame = ttk.Frame(container_inner)
        bottom_frame.pack(fill="x", pady=(30, 0))

        ttk.Label(
            bottom_frame,
            text="💡 提示：使用鼠标滚轮或拖动滚动条查看所有内容",
            font=self.master_app.fonts["small"],
            foreground="#6C757D"
        ).pack()

    def create_stat_card(self, parent, title, count, color):
        """创建统计卡片"""
        card = ttk.Frame(parent, style="Card.TFrame")

        inner = ttk.Frame(card)
        inner.pack(pady=15, padx=15, fill="both", expand=True)

        # 标题
        ttk.Label(
            inner,
            text=title,
            font=self.master_app.fonts["small"],
            foreground=self.master_app.colors["dark"]
        ).pack(anchor="w")

        # 数量
        ttk.Label(
            inner,
            text=str(count),
            font=("Microsoft YaHei", 24, "bold"),
            foreground=color
        ).pack(anchor="w", pady=(5, 0))

        return card

    def show_user_count(self):
        count = len(self.master_app.db.users)
        messagebox.showinfo(
            "用户统计",
            f"👥 当前系统用户总数：{count} 人",
            icon="info"
        )

    def show_product_count(self):
        count = len(self.master_app.db.products)
        messagebox.showinfo(
            "商品统计",
            f"🛍️ 当前系统商品数量：{count} 件",
            icon="info"
        )

    def show_order_count(self):
        count = len(self.master_app.db.orders)
        messagebox.showinfo(
            "订单统计",
            f"📋 当前系统订单数量：{count} 笔",
            icon="info"
        )

    def show_notifications(self):
        count = len(self.master_app.db.notifications)
        messagebox.showinfo(
            "通知统计",
            f"🔔 系统已发送通知数量：{count} 条",
            icon="info"
        )

    def show_system_logs(self):
        """显示系统日志（示例功能）"""
        messagebox.showinfo(
            "系统日志",
            "系统日志功能\n\n"
            "这里可以显示系统操作日志、错误日志等。\n"
            "当前为演示版本，完整功能需要进一步开发。"
        )

    def show_system_settings(self):
        """显示系统设置（示例功能）"""
        messagebox.showinfo(
            "系统设置",
            "系统设置功能\n\n"
            "这里可以进行系统参数配置、权限管理等。\n"
            "当前为演示版本，完整功能需要进一步开发。"
        )


class RegisterFrame(ttk.Frame):
    """注册界面"""

    def __init__(self, master: SweetFishApp, auth_service: AuthService):
        super().__init__(master, style="Card.TFrame")
        self.master_app = master
        self.auth = auth_service

        container = ttk.Frame(self)
        container.pack(pady=30, padx=30)

        # 品牌标识
        brand_frame = ttk.Frame(container)
        brand_frame.pack(pady=(0, 20))

        ttk.Label(
            brand_frame,
            text="🐟 甜鱼商城",
            style="Title.TLabel"
        ).pack()

        ttk.Label(
            brand_frame,
            text="创建您的账户",
            font=master.fonts["normal"],
            foreground=master.colors["dark"]
        ).pack(pady=(5, 0))

        # 表单区域
        form = ttk.Frame(container, style="Card.TFrame")
        form.pack(padx=20, pady=20)

        inner = ttk.Frame(form, padding=30)
        inner.pack()

        # 手机号
        phone_frame = ttk.Frame(inner)
        phone_frame.pack(fill="x", pady=(0, 15))

        ttk.Label(
            phone_frame,
            text="手机号",
            font=master.fonts["small"],
            foreground=master.colors["dark"]
        ).pack(anchor="w", pady=(0, 5))

        self.phone_entry = ttk.Entry(
            phone_frame,
            style="Modern.TEntry",
            font=master.fonts["normal"]
        )
        self.phone_entry.pack(fill="x", ipady=8)

        # 密码
        pass_frame = ttk.Frame(inner)
        pass_frame.pack(fill="x", pady=(0, 15))

        ttk.Label(
            pass_frame,
            text="密码",
            font=master.fonts["small"],
            foreground=master.colors["dark"]
        ).pack(anchor="w", pady=(0, 5))

        self.pass_entry = ttk.Entry(
            pass_frame,
            style="Modern.TEntry",
            font=master.fonts["normal"],
            show="●"
        )
        self.pass_entry.pack(fill="x", ipady=8)

        # 角色选择
        role_frame = ttk.Frame(inner)
        role_frame.pack(fill="x", pady=(0, 25))

        ttk.Label(
            role_frame,
            text="选择角色",
            font=master.fonts["small"],
            foreground=master.colors["dark"]
        ).pack(anchor="w", pady=(0, 5))

        self.role_var = tk.StringVar(value="USER")
        role_combo = ttk.Combobox(
            role_frame,
            textvariable=self.role_var,
            values=["USER", "MERCHANT", "ADMIN"],
            state="readonly",
            style="Modern.TEntry",
            font=master.fonts["normal"]
        )
        role_combo.pack(fill="x", ipady=8)

        # 注册按钮
        btn_frame = ttk.Frame(inner)
        btn_frame.pack(fill="x", pady=(10, 0))

        ttk.Button(
            btn_frame,
            text="注册账户",
            style="Primary.TButton",
            command=self.register
        ).pack(fill="x", pady=(0, 10))

        ttk.Button(
            btn_frame,
            text="返回登录",
            style="Secondary.TButton",
            command=lambda: master.show_login()
        ).pack(fill="x")

    def register(self):
        """执行注册操作"""
        phone = self.phone_entry.get().strip()
        password = self.pass_entry.get().strip()
        role = self.role_var.get().strip()

        if not phone or not password:
            messagebox.showwarning("输入错误", "请填写手机号和密码")
            return

        if not role:
            messagebox.showwarning("输入错误", "请选择角色")
            return

        try:
            user = self.auth.register(phone, password, role)
            messagebox.showinfo(
                "注册成功",
                f"✅ 注册成功！\n\n用户名：{user.name}\n角色：{user.role.value}\n\n请使用您的账户登录。"
            )
            self.master_app.show_login()
        except Exception as e:
            messagebox.showerror(
                "注册失败",
                f"注册过程中出错：\n\n{str(e)}",
                icon="error"
            )


class MerchantFrame(ttk.Frame):
    """商户后台界面"""

    def __init__(self, master: SweetFishApp, user):
        super().__init__(master)
        self.master_app = master
        self.user = user
        self.prodsvc = master.prodsvc
        self._mousewheel_binding = None  # 用于存储鼠标滚轮事件绑定

        # 创建主布局
        self.setup_ui()

    def setup_ui(self):
        """设置商户界面"""

        # 创建主容器
        main_container = ttk.Frame(self)
        main_container.pack(fill="both", expand=True)

        # 顶部导航栏
        self.create_top_bar(main_container)

        # 创建带滚动条的主内容区域
        self.create_scrollable_content(main_container)

    def create_top_bar(self, parent):
        """创建顶部导航栏"""
        top_bar = ttk.Frame(parent, style="Card.TFrame")
        top_bar.pack(fill="x", pady=(0, 10))

        # 左侧用户信息
        user_info_frame = ttk.Frame(top_bar)
        user_info_frame.pack(side="left", padx=20, pady=15)

        # 用户头像和名称
        avatar_frame = ttk.Frame(user_info_frame)
        avatar_frame.pack(side="left")

        # 模拟头像
        avatar_label = ttk.Label(
            avatar_frame,
            text="🏪",
            font=("Segoe UI Emoji", 24),
            background=self.master_app.colors["light"]
        )
        avatar_label.pack(padx=(0, 10))

        # 用户详情
        user_details = ttk.Frame(user_info_frame)
        user_details.pack(side="left")

        ttk.Label(
            user_details,
            text=self.user.name,
            font=self.master_app.fonts["header"],
            foreground=self.master_app.colors["primary"]
        ).pack(anchor="w")

        shop_name = getattr(self.user, 'shop_name', '未设置商店名称')
        ttk.Label(
            user_details,
            text=f"商家 • {shop_name}",
            font=self.master_app.fonts["small"],
            foreground="#6C757D"
        ).pack(anchor="w", pady=(2, 0))

        # 右侧操作按钮
        action_frame = ttk.Frame(top_bar)
        action_frame.pack(side="right", padx=20, pady=15)

        # 登出按钮
        logout_btn = ttk.Button(
            action_frame,
            text="退出登录",
            style="Secondary.TButton",
            command=self.master_app.logout,
            width=10
        )
        logout_btn.pack(side="left")

    def create_scrollable_content(self, parent):
        """创建带滚动条的内容区域"""
        # 创建Canvas和滚动条
        self.canvas = tk.Canvas(parent, bg=self.master_app.colors["light"], highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(parent, orient="vertical", command=self.canvas.yview, style="Modern.Vertical.TScrollbar")

        # 创建可滚动的内部框架
        self.scrollable_frame = ttk.Frame(self.canvas, style="Card.TFrame")

        # 配置Canvas
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        # 在Canvas中创建窗口
        self.canvas_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        # 配置Canvas滚动
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # 布局Canvas和滚动条
        self.canvas.pack(side="left", fill="both", expand=True, padx=(20, 0), pady=20)
        self.scrollbar.pack(side="right", fill="y", padx=(0, 20), pady=20)

        # 绑定鼠标滚轮事件 - 使用安全的方式
        def _on_mousewheel(event):
            try:
                if hasattr(self, 'canvas') and self.canvas.winfo_exists():
                    self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
            except tk.TclError:
                # Canvas已经被销毁，忽略这个事件
                pass

        # 绑定鼠标滚轮事件到Canvas
        self._mousewheel_binding = self.canvas.bind("<MouseWheel>", _on_mousewheel)

        # 确保Canvas窗口宽度跟随Canvas调整
        def configure_canvas_window(event):
            if hasattr(self, 'canvas') and self.canvas.winfo_exists():
                self.canvas.itemconfig(self.canvas_window, width=event.width)

        self.canvas.bind("<Configure>", configure_canvas_window)

        # 创建商户控制面板
        self.create_merchant_panel()

    def destroy(self):
        """重写destroy方法以解除事件绑定"""
        # 解除鼠标滚轮事件绑定
        if hasattr(self, '_mousewheel_binding') and self._mousewheel_binding:
            try:
                self.canvas.unbind("<MouseWheel>", self._mousewheel_binding)
            except:
                pass

        # 调用父类的destroy方法
        super().destroy()

    def create_merchant_panel(self):
        """创建商户控制面板"""
        # 主内容容器
        container = ttk.Frame(self.scrollable_frame)
        container.pack(pady=20, padx=20, fill="both", expand=True)

        container_inner = ttk.Frame(container)
        container_inner.pack(pady=20, padx=20, fill="both", expand=True)

        # 标题区域
        title_frame = ttk.Frame(container_inner)
        title_frame.pack(pady=(0, 30))

        ttk.Label(
            title_frame,
            text="🏪 商家后台",
            style="Title.TLabel"
        ).pack()

        ttk.Label(
            title_frame,
            text=f"欢迎回来，{self.user.name}",
            font=self.master_app.fonts["normal"],
            foreground=self.master_app.colors["dark"]
        ).pack(pady=(5, 0))

        # 商家信息卡片
        info_card = ttk.Frame(container_inner, style="Card.TFrame")
        info_card.pack(fill="x", pady=(0, 30), ipady=15, ipadx=15)

        shop_name = getattr(self.user, 'shop_name', '未设置')
        ttk.Label(
            info_card,
            text=f"商店名称：{shop_name}",
            font=self.master_app.fonts["header"],
            foreground=self.master_app.colors["primary"]
        ).pack(anchor="w", pady=(0, 10))

        # 获取商家统计数据
        my_products = [p for p in self.master_app.db.products.values() if p.merchant_id == self.user.user_id]
        total_sales = len([o for p in my_products for o in self.master_app.db.orders.values()
                          if p.product_id in [item.product_id for item in o.items]])

        ttk.Label(
            info_card,
            text=f"在售商品：{len(my_products)} 件 • 总销量：{total_sales} 单",
            font=self.master_app.fonts["small"],
            foreground=self.master_app.colors["dark"]
        ).pack(anchor="w")

        # 店铺管理区域
        management_frame = ttk.Frame(container_inner)
        management_frame.pack(fill="x", pady=(0, 20))

        ttk.Label(
            management_frame,
            text="店铺管理",
            style="Header.TLabel"
        ).pack(anchor="w", pady=(0, 15))

        # 店铺管理操作按钮
        management_operations = [
            ("➕ 上架商品", self.create_product),
            ("📦 我的商品", self.show_my_products),
            ("✏️ 编辑商品", self.edit_products),
            ("🗑️ 下架商品", self.delete_products),
        ]

        for text, command in management_operations:
            btn = ttk.Button(
                management_frame,
                text=text,
                command=command,
                style="Secondary.TButton"
            )
            btn.pack(fill="x", pady=5, ipady=10)

        # 订单管理区域
        order_frame = ttk.Frame(container_inner)
        order_frame.pack(fill="x", pady=(0, 20))

        ttk.Label(
            order_frame,
            text="订单管理",
            style="Header.TLabel"
        ).pack(anchor="w", pady=(0, 15))

        # 订单管理操作按钮
        order_operations = [
            ("💰 待处理订单", self.show_pending_orders),
            ("🚚 发货管理", self.manage_shipments),
            ("📦 已发货订单", self.show_shipped_orders),
            ("↩️ 退款处理", self.handle_refunds),
        ]

        for text, command in order_operations:
            btn = ttk.Button(
                order_frame,
                text=text,
                command=command,
                style="Secondary.TButton"
            )
            btn.pack(fill="x", pady=5, ipady=10)

        # 统计分析区域
        stats_frame = ttk.Frame(container_inner)
        stats_frame.pack(fill="x", pady=(0, 20))

        ttk.Label(
            stats_frame,
            text="统计分析",
            style="Header.TLabel"
        ).pack(anchor="w", pady=(0, 15))

        # 统计分析操作按钮
        stats_operations = [
            ("📊 销售统计", self.show_stats),
            ("📈 销售趋势", self.show_sales_trend),
            ("💰 收入报表", self.show_income_report),
            ("👥 客户分析", self.show_customer_analysis),
        ]

        for text, command in stats_operations:
            btn = ttk.Button(
                stats_frame,
                text=text,
                command=command,
                style="Secondary.TButton"
            )
            btn.pack(fill="x", pady=5, ipady=10)

        # 店铺设置区域
        settings_frame = ttk.Frame(container_inner)
        settings_frame.pack(fill="x", pady=(0, 20))

        ttk.Label(
            settings_frame,
            text="店铺设置",
            style="Header.TLabel"
        ).pack(anchor="w", pady=(0, 15))

        # 店铺设置操作按钮
        settings_operations = [
            ("🏪 店铺信息", self.edit_shop_info),
            ("🎨 店铺装修", self.customize_shop),
            ("📢 营销活动", self.create_promotion),
            ("🔔 消息通知", self.manage_notifications),
        ]

        for text, command in settings_operations:
            btn = ttk.Button(
                settings_frame,
                text=text,
                command=command,
                style="Secondary.TButton"
            )
            btn.pack(fill="x", pady=5, ipady=10)

        # 底部说明
        bottom_frame = ttk.Frame(container_inner)
        bottom_frame.pack(fill="x", pady=(30, 0))

        ttk.Label(
            bottom_frame,
            text="💡 提示：使用鼠标滚轮或拖动滚动条查看所有功能",
            font=self.master_app.fonts["small"],
            foreground="#6C757D"
        ).pack()

    def create_product(self):
        """创建商品（示例功能）"""
        messagebox.showinfo(
            "功能说明",
            "商品创建功能\n\n"
            "这里可以实现完整的商品创建界面，包括：\n"
            "• 商品名称和描述输入\n"
            "• 价格和库存设置\n"
            "• 图片上传功能\n"
            "• 分类标签选择\n\n"
            "当前为演示版本，完整功能需要进一步开发。"
        )

    def show_my_products(self):
        """显示我的商品（示例功能）"""
        my_products = [p for p in self.master_app.db.products.values()
                      if p.merchant_id == self.user.user_id]

        if not my_products:
            messagebox.showinfo("我的商品", "您还没有上架任何商品")
            return

        product_list = "\n".join([
            f"• {p.title} - ¥{p.price_cents/100:.2f} (库存：{p.stock})"
            for p in my_products[:10]  # 只显示前10个
        ])

        if len(my_products) > 10:
            product_list += f"\n\n... 还有 {len(my_products) - 10} 个商品"

        messagebox.showinfo(
            "我的商品",
            f"共 {len(my_products)} 个商品：\n\n{product_list}"
        )

    def edit_products(self):
        """编辑商品（示例功能）"""
        messagebox.showinfo(
            "编辑商品",
            "商品编辑功能\n\n"
            "这里可以批量编辑商品信息，包括：\n"
            "• 修改商品价格\n"
            "• 更新商品库存\n"
            "• 修改商品描述\n"
            "• 批量操作\n\n"
            "当前为演示版本，完整功能需要进一步开发。"
        )

    def delete_products(self):
        """下架商品（示例功能）"""
        messagebox.showinfo(
            "下架商品",
            "商品下架功能\n\n"
            "这里可以选择商品进行下架操作。\n"
            "下架的商品将不再对用户可见。\n\n"
            "当前为演示版本，完整功能需要进一步开发。"
        )

    def show_pending_orders(self):
        """显示待处理订单（示例功能）"""
        messagebox.showinfo(
            "待处理订单",
            "待处理订单功能\n\n"
            "这里可以查看所有待处理的订单，\n"
            "并进行发货或退款等操作。\n\n"
            "当前为演示版本，完整功能需要进一步开发。"
        )

    def manage_shipments(self):
        """发货管理（示例功能）"""
        messagebox.showinfo(
            "发货管理",
            "发货管理功能\n\n"
            "这里可以处理订单的发货操作，\n"
            "包括填写物流单号、发货状态等。\n\n"
            "当前为演示版本，完整功能需要进一步开发。"
        )

    def show_shipped_orders(self):
        """显示已发货订单（示例功能）"""
        messagebox.showinfo(
            "已发货订单",
            "已发货订单功能\n\n"
            "这里可以查看所有已发货的订单，\n"
            "并跟踪物流状态。\n\n"
            "当前为演示版本，完整功能需要进一步开发。"
        )

    def handle_refunds(self):
        """退款处理（示例功能）"""
        messagebox.showinfo(
            "退款处理",
            "退款处理功能\n\n"
            "这里可以处理客户的退款申请，\n"
            "进行退款审核和操作。\n\n"
            "当前为演示版本，完整功能需要进一步开发。"
        )

    def show_stats(self):
        """显示销售统计"""
        my_products = [p for p in self.master_app.db.products.values()
                      if p.merchant_id == self.user.user_id]

        if not my_products:
            messagebox.showinfo("销售统计", "您还没有上架任何商品")
            return

        # 计算统计数据
        total_products = len(my_products)
        total_stock = sum(p.stock for p in my_products)
        total_value = sum(p.price_cents * p.stock for p in my_products) / 100

        # 找出最畅销的商品
        product_sales = {}
        for p in my_products:
            sales = len([o for o in self.master_app.db.orders.values()
                        if any(item.product_id == p.product_id for item in o.items)])
            product_sales[p.title] = sales

        best_seller = max(product_sales.items(), key=lambda x: x[1], default=("无", 0))

        stats_msg = f"""
        📊 销售统计
        
        店铺信息：
        • 店铺名称：{getattr(self.user, 'shop_name', '未设置')}
        • 商家ID：{self.user.user_id}
        
        商品统计：
        • 在售商品：{total_products} 件
        • 总库存量：{total_stock} 个
        • 库存总价值：¥{total_value:.2f}
        
        销售统计：
        • 最畅销商品：{best_seller[0]}
        • 销量：{best_seller[1]} 单
        
        其他信息：
        • 建议优化库存结构
        • 定期更新商品信息
        • 关注客户反馈
        """

        messagebox.showinfo("销售统计", stats_msg)

    def show_sales_trend(self):
        """显示销售趋势（示例功能）"""
        messagebox.showinfo(
            "销售趋势",
            "销售趋势分析功能\n\n"
            "这里可以查看店铺的销售趋势图表，\n"
            "包括日、周、月销售额变化等。\n\n"
            "当前为演示版本，完整功能需要进一步开发。"
        )

    def show_income_report(self):
        """显示收入报表（示例功能）"""
        messagebox.showinfo(
            "收入报表",
            "收入报表功能\n\n"
            "这里可以生成详细的收入报表，\n"
            "包括总收入、净利润、各项支出等。\n\n"
            "当前为演示版本，完整功能需要进一步开发。"
        )

    def show_customer_analysis(self):
        """显示客户分析（示例功能）"""
        messagebox.showinfo(
            "客户分析",
            "客户分析功能\n\n"
            "这里可以分析客户购买行为，\n"
            "包括客户画像、购买偏好等。\n\n"
            "当前为演示版本，完整功能需要进一步开发。"
        )

    def edit_shop_info(self):
        """编辑店铺信息（示例功能）"""
        messagebox.showinfo(
            "店铺信息",
            "店铺信息编辑功能\n\n"
            "这里可以修改店铺名称、简介、\n"
            "联系方式等基本信息。\n\n"
            "当前为演示版本，完整功能需要进一步开发。"
        )

    def customize_shop(self):
        """店铺装修（示例功能）"""
        messagebox.showinfo(
            "店铺装修",
            "店铺装修功能\n\n"
            "这里可以自定义店铺的外观，\n"
            "包括主题颜色、布局、横幅等。\n\n"
            "当前为演示版本，完整功能需要进一步开发。"
        )

    def create_promotion(self):
        """创建营销活动（示例功能）"""
        messagebox.showinfo(
            "营销活动",
            "营销活动创建功能\n\n"
            "这里可以创建各种营销活动，\n"
            "如折扣、满减、优惠券等。\n\n"
            "当前为演示版本，完整功能需要进一步开发。"
        )

    def manage_notifications(self):
        """管理消息通知（示例功能）"""
        messagebox.showinfo(
            "消息通知",
            "消息通知管理功能\n\n"
            "这里可以设置接收哪些类型的通知，\n"
            "如订单通知、系统通知等。\n\n"
            "当前为演示版本，完整功能需要进一步开发。"
        )