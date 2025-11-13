"""
Project module adjusted for pylint-friendly style.
"""

import threading
from typing import Dict, List, Optional, Tuple

from . import models


class MemoryDB:


    def __init__(self) -> None:
        # user
        self.users: Dict[str, models.BaseUser] = {}
        self.user_phone_index: Dict[str, str] = {}

        # product
        self.products: Dict[str, models.Product] = {}

        # order
        self.orders: Dict[str, models.Order] = {}
        self.payments: Dict[str, models.Payment] = {}
        self.bargains: Dict[str, models.Bargain] = {}
        self.reviews: Dict[str, models.Review] = {}

        # 通知（admin）
        self.notifications: List[dict] = []

        # 线程锁，保证多线程访问安全
        self._lock = threading.RLock()

    # 用户
    def add_user(self, user: models.BaseUser) -> None:
        with self._lock:
            self.users[user.user_id] = user
            self.user_phone_index[user.phone] = user.user_id

    def get_user_by_id(self, user_id: str) -> Optional[models.BaseUser]:
        return self.users.get(user_id)

    def get_user_by_phone(self, phone: str) -> Optional[models.BaseUser]:
        uid = self.user_phone_index.get(phone)
        return self.users.get(uid) if uid else None

    # 商品
    def add_product(self, p: models.Product) -> None:
        with self._lock:
            self.products[p.product_id] = p

    def get_product(self, pid: str) -> Optional[models.Product]:
        return self.products.get(pid)

    def search_products(self, keyword: str = "") -> List[models.Product]:
        res = []
        low = keyword.lower()
        for p in self.products.values():
            if (
                not keyword
                or low in p.title.lower()
                or low in p.description.lower()
                or low in " ".join(p.tags).lower()
            ):
                res.append(p)
        res.sort(key=lambda q: (-q.promotion_rank, -q.views, -q.sold))
        return res

    # 订单交易
    def add_order(self, order: models.Order) -> None:
        with self._lock:
            self.orders[order.order_id] = order

    def get_order(self, oid: str) -> Optional[models.Order]:
        return self.orders.get(oid)

    def add_payment(self, pay: models.Payment) -> None:
        with self._lock:
            self.payments[pay.payment_id] = pay

    def get_payment(self, pid: str) -> Optional[models.Payment]:
        return self.payments.get(pid)

    def add_bargain(self, b: models.Bargain) -> None:
        with self._lock:
            self.bargains[b.bargain_id] = b

    def get_bargain(self, bid: str) -> Optional[models.Bargain]:
        return self.bargains.get(bid)

    # 评论
    def add_review(self, r: models.Review) -> None:
        with self._lock:
            self.reviews[r.review_id] = r

    def list_reviews_for_product(self, pid: str) -> List[models.Review]:
        product_reviews = []
        for review in self.reviews.values():
            if review.product_id == pid:
                product_reviews.append(review)

        return product_reviews

    # 通知
    def add_notification(self, notif: dict) -> None:
        with self._lock:
            self.notifications.append(notif)

    def get_notifications(self) -> List[dict]:
        with self._lock:
            return self.notifications.copy()
