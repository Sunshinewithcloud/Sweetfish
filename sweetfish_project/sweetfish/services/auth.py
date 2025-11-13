"""Module adjusted to satisfy style checks."""

from ..db import MemoryDB
from ..models import Admin, BaseUser, Merchant, gen_id


class AuthService:

    def __init__(self, db: MemoryDB) -> None:
        self.db = db

    def register_user(self, phone: str, name: str, password: str) -> BaseUser:
        if self.db.get_user_by_phone(phone):
            raise ValueError("phone already registered")
        user_id = gen_id("u_")
        user = BaseUser(user_id=user_id, phone=phone, name=name, password_hash=self._hash(password))
        self.db.add_user(user)
        return user

    def register_merchant(self, phone: str, name: str, password: str, shop_name: str) -> Merchant:
        if self.db.get_user_by_phone(phone):
            raise ValueError("phone already registered")
        mid = gen_id("m_")
        merchant = Merchant(
            user_id=mid,
            phone=phone,
            name=name,
            password_hash=self._hash(password),
            shop_name=shop_name,
        )
        self.db.add_user(merchant)
        return merchant

    def register_admin(self, phone: str, name: str, password: str) -> Admin:
        if self.db.get_user_by_phone(phone):
            raise ValueError("phone already registered")
        aid = gen_id("a_")
        admin = Admin(user_id=aid, phone=phone, name=name, password_hash=self._hash(password))
        self.db.add_user(admin)
        return admin

    def authenticate(self, phone: str, password: str):
        user = self.db.get_user_by_phone(phone)
        if user and self._hash(password) == user.password_hash:
            return user
        return None

    # 大模型让加的什么保密
    @staticmethod
    def _hash(password: str) -> str:
        return "H:" + password[::-1]
