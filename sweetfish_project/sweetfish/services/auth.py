"""Unified AuthService with role-based registration."""

from ..db import MemoryDB
from ..models import Admin, BaseUser, Merchant, gen_id


class AuthService:

    def __init__(self, db: MemoryDB) -> None:
        self.db = db

    # =============================
    #     统一注册入口（关键）
    # =============================
    def register(self, phone: str, password: str, role: str = "USER"):
        """统一注册接口，根据角色创建不同用户"""
        if not phone:
            raise ValueError("手机号不能为空")

        if not password:
            raise ValueError("密码不能为空")

        if self.db.get_user_by_phone(phone):
            raise ValueError("手机号已存在")

        # 普通用户
        if role.upper() == "USER":
            uid = gen_id("u_")
            user = BaseUser(
                user_id=uid,
                phone=phone,
                name=phone,
                password_hash=self._hash(password)
            )
            self.db.add_user(user)
            return user

        # 商家
        elif role.upper() == "MERCHANT":
            mid = gen_id("m_")
            merchant = Merchant(
                user_id=mid,
                phone=phone,
                name=phone,
                password_hash=self._hash(password),
                shop_name=f"{phone}的店铺"
            )
            self.db.add_user(merchant)
            return merchant

        # 管理员
        elif role.upper() == "ADMIN":
            aid = gen_id("a_")
            admin = Admin(
                user_id=aid,
                phone=phone,
                name=phone,
                password_hash=self._hash(password)
            )
            self.db.add_user(admin)
            return admin

        else:
            raise ValueError(f"未知角色: {role}")

    # =============================
    #        用户认证
    # =============================
    def authenticate(self, phone: str, password: str):
        user = self.db.get_user_by_phone(phone)
        if user and self._hash(password) == user.password_hash:
            return user
        return None

    # =============================
    #        密码加密（你原来的方式）
    # =============================
    @staticmethod
    def _hash(password: str) -> str:
        return "H:" + password[::-1]
