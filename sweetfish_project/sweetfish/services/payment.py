"""Module adjusted to satisfy style checks."""

import random

from ..db import MemoryDB
from ..models import Payment
from ..services.notification import NotificationService


class PaymentGateway:

    def __init__(self, db: MemoryDB, notification: NotificationService) -> None:
        self.db = db
        self.notification = notification

    def create_payment(self, order) -> Payment:
        pay_id = "pay_" + __import__("uuid").uuid4().hex[:12]
        pay = Payment(payment_id=pay_id, order_id=order.order_id, amount_cents=order.total_cents)
        self.db.add_payment(pay)
        return pay

    def process_payment(self, payment: Payment, succeed_rate: float = 0.95) -> Payment:
        if random.random() < succeed_rate:
            payment.status = "success"
            self.notification.push_payment_success(payment.order_id, payment.payment_id)
        else:
            payment.status = "failed"
            self.notification.push_payment_failure(payment.order_id, payment.payment_id)
        return payment
