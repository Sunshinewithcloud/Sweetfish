"""Module adjusted to satisfy style checks."""

from datetime import datetime
from typing import List, Tuple

from ..db import MemoryDB


class NotificationService:

    def __init__(self, db: MemoryDB) -> None:
        self.db = db
        self.messages: List[Tuple[str, str, datetime]] = []

    def push(self, user_id: str, message: str) -> None:
        self.messages.append((user_id, message, datetime.utcnow()))

    def push_payment_success(self, order_id: str, payment_id: str) -> None:
        order = self.db.get_order(order_id)
        if order:
            self.push(order.buyer_id, f"支付成功: 订单 {order.order_id}，支付ID {payment_id}")

    def push_payment_failure(self, order_id: str, payment_id: str) -> None:
        order = self.db.get_order(order_id)
        if order:
            self.push(order.buyer_id, f"支付失败: 订单 {order.order_id}，支付ID {payment_id}")

    def get_notifications_for_user(self, user_id: str):
        return [(msg, ts) for (uid, msg, ts) in self.messages if uid == user_id]
