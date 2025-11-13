"""Module adjusted to satisfy style checks."""

import tkinter as tk
from tkinter import messagebox, ttk

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

    def __init__(self, db: MemoryDB):

        super().__init__()
        self.title("甜鱼 商城系统")
        self.geometry("300x500")
        self.db = db

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
        self.show_login()

    def show_login(self):
        """切换到登录界面"""
        if self.active_frame:
            self.active_frame.destroy()
        self.active_frame = LoginFrame(self, self.auth)
        self.active_frame.pack(fill="both", expand=True)

    def show_main(self, user):
        """根据角色切换界面"""
        if self.active_frame:
            self.active_frame.destroy()
        self.current_user = user
        if user.role.name == "ADMIN":
            self.active_frame = AdminFrame(self, user)
        else:
            self.active_frame = MainFrame(self, user)
        self.active_frame.pack(fill="both", expand=True)


class LoginFrame(ttk.Frame):
    """登录界面"""

    def __init__(self, master: SweetFishApp, auth_service: AuthService):
        super().__init__(master)
        self.master_app = master
        self.auth = auth_service
        ttk.Label(self, text="甜鱼 登录", font=("Arial", 18, "bold")).pack(pady=20)
        form = ttk.Frame(self)
        form.pack(pady=40)
        ttk.Label(form, text="手机号:").grid(row=0, column=0, pady=5, padx=5)
        self.phone_entry = ttk.Entry(form)
        self.phone_entry.grid(row=0, column=1)
        ttk.Label(form, text="密码:").grid(row=1, column=0, pady=5, padx=5)
        self.pass_entry = ttk.Entry(form, show="*")
        self.pass_entry.grid(row=1, column=1)

        ttk.Button(self, text="登录", command=self.login).pack(pady=10)
        ttk.Button(self, text="注册新用户", command=self.register).pack(pady=5)

    def login(self):
        phone = self.phone_entry.get().strip()
        password = self.pass_entry.get().strip()
        user = self.auth.authenticate(phone, password)
        if user:
            messagebox.showinfo("登录成功", f"欢迎 {user.name}")
            self.master_app.show_main(user)
        else:
            messagebox.showerror("登录失败", "手机号或密码错误")

    def register(self):
        phone = self.phone_entry.get().strip()
        password = self.pass_entry.get().strip()
        if not phone or not password:
            messagebox.showwarning("输入错误", "请输入手机号与密码")
            return
        try:
            user = self.auth.register_user(phone, phone, password)
            messagebox.showinfo("注册成功", f"您的ID: {user.user_id}")
        except Exception as e:
            messagebox.showerror("注册失败", str(e))


class MainFrame(ttk.Frame):

    # 主界面
    def __init__(self, master: SweetFishApp, user):
        super().__init__(master)
        self.master_app = master
        self.user = user
        self.prodsvc = master.prodsvc
        self.ordersvc = master.ordersvc
        self.notification = master.notification
        self.setup_ui()

    def setup_ui(self):
        top = ttk.Frame(self)
        top.pack(fill="x", pady=5)
        ttk.Label(
            top, text=f"当前用户: {self.user.name} ({self.user.role.value})", font=("Arial", 12)
        ).pack(side="left", padx=8)
        ttk.Button(top, text="登出", command=self.logout).pack(side="right", padx=8)

        # 搜索区
        body = ttk.Frame(self)
        body.pack(fill="both", expand=True)
        left = ttk.Frame(body)
        left.pack(side="left", fill="y", padx=5, pady=5)
        ttk.Label(left, text="搜索商品").pack()
        self.search_entry = ttk.Entry(left)
        self.search_entry.pack()
        ttk.Button(left, text="搜索", command=self.search_products).pack(pady=5)
        ttk.Button(left, text="创建订单", command=self.create_order_from_selection).pack(pady=5)
        ttk.Button(left, text="支付订单", command=self.pay_selected_order).pack(pady=5)
        ttk.Button(left, text="查看通知", command=self.show_notifications).pack(pady=5)

        # 商品区
        center = ttk.Frame(body)
        center.pack(side="left", fill="both", expand=True)
        ttk.Label(center, text="商品列表").pack()
        self.product_tree = ttk.Treeview(
            center, columns=("title", "price", "stock"), show="headings", selectmode="browse"
        )
        for c in ("title", "price", "stock"):
            self.product_tree.heading(c, text=c.capitalize())
        self.product_tree.pack(fill="both", expand=True)

        # 订单区
        right = ttk.Frame(body)
        right.pack(side="right", fill="y")
        ttk.Label(right, text="订单").pack()
        self.order_tree = ttk.Treeview(right, columns=("id", "total", "status"), show="headings")
        for c in ("id", "total", "status"):
            self.order_tree.heading(c, text=c.capitalize())
        self.order_tree.pack(fill="y", expand=True)

        self.populate_demo_data()

    def logout(self):
        # 登出
        confirm = messagebox.askyesno("确认", "确定要登出吗？")
        if confirm:
            self.master_app.show_login()

    def populate_demo_data(self):
        # 当前为示例商品
        m = (
            self.master_app.auth.register_merchant("13800000002", "Bob", "bobpwd", "BobShop")
            if not self.master_app.db.get_user_by_phone("13800000002")
            else self.master_app.db.get_user_by_phone("13800000002")
        )
        if not self.master_app.db.products:
            self.prodsvc.create_product(
                m.user_id, "Vintage Lamp", "A warm lamp.", 1999, stock=3, tags={"lamp"}
            )
            self.prodsvc.create_product(
                m.user_id, "Used Phone", "Good condition.", 8999, stock=5, tags={"phone"}
            )
        self.refresh_products()

    def refresh_products(self, products=None):
        for row in self.product_tree.get_children():
            self.product_tree.delete(row)
        products = products or list(self.master_app.db.products.values())
        for p in products:
            self.product_tree.insert(
                "", "end", iid=p.product_id, values=(p.title, f"{p.price_cents / 100:.2f}", p.stock)
            )

    def search_products(self):
        kw = self.search_entry.get().strip()
        self.refresh_products(self.prodsvc.search(kw))

    def create_order_from_selection(self):
        sel = self.product_tree.selection()
        if not sel:
            messagebox.showwarning("未选择", "请选择商品")
            return
        pid = sel[0]
        try:
            order = self.ordersvc.create_order(self.user.user_id, [(pid, 1)])
            self.order_tree.insert(
                "",
                "end",
                iid=order.order_id,
                values=(order.order_id, f"{order.total_cents / 100:.2f}", order.status.value),
            )
            messagebox.showinfo("下单成功", f"订单号: {order.order_id}")
        except Exception as e:
            messagebox.showerror("错误", str(e))

    def pay_selected_order(self):
        sel = self.order_tree.selection()
        if not sel:
            messagebox.showwarning("未选择", "请选择订单")
            return
        oid = sel[0]
        try:
            pay = self.ordersvc.pay_order(oid, succeed_rate=0.98)
            self.order_tree.set(oid, "status", self.master_app.db.get_order(oid).status.value)
            messagebox.showinfo("支付结果", f"支付 {pay.status}")
        except Exception as e:
            messagebox.showerror("错误", str(e))

    def show_notifications(self):
        notes = self.notification.get_notifications_for_user(self.user.user_id)
        if not notes:
            messagebox.showinfo("通知", "暂无消息")
            return
        msg = "\n".join([f"{t:%Y-%m-%d %H:%M} | {m}" for (m, t) in notes])
        messagebox.showinfo("通知", msg)


# 管理员界面
class AdminFrame(ttk.Frame):

    def __init__(self, master: SweetFishApp, user):
        super().__init__(master)
        self.master_app = master
        self.user = user
        ttk.Label(
            self, text="SweetFish 后台管理系统", font=("Arial", 18, "bold"), foreground="red"
        ).pack(pady=20)
        ttk.Label(self, text=f"当前登录管理员：{user.name}").pack(pady=5)

        ttk.Button(self, text="查看用户数", command=self.show_user_count).pack(pady=5)
        ttk.Button(self, text="查看商品数", command=self.show_product_count).pack(pady=5)
        ttk.Button(self, text="查看订单数", command=self.show_order_count).pack(pady=5)
        ttk.Button(self, text="查看系统通知", command=self.show_notifications).pack(pady=5)
        ttk.Button(self, text="登出", command=self.logout).pack(pady=10)

    def show_user_count(self):
        count = len(self.master_app.db.users)
        messagebox.showinfo("统计结果", f"当前系统用户总数：{count}")

    def show_product_count(self):
        count = len(self.master_app.db.products)
        messagebox.showinfo("统计结果", f"当前系统商品数量：{count}")

    def show_order_count(self):
        count = len(self.master_app.db.orders)
        messagebox.showinfo("统计结果", f"当前系统订单数量：{count}")

    def show_notifications(self):
        count = len(self.master_app.db.notifications)
        messagebox.showinfo("统计结果", f"系统已发送通知数量：{count}")

    def logout(self):
        confirm = messagebox.askyesno("确认", "确定要登出管理员账号吗？")
        if confirm:
            self.master_app.show_login()
