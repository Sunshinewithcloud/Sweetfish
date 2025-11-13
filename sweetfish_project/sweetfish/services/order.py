"""Module adjusted to satisfy style checks."""

from typing import List, Tuple

from ..db import MemoryDB
from ..models import Order, OrderItem, OrderStatus, gen_id
from ..services import credit
from ..services.recommend import RecommendationEngine
from .notification import NotificationService
from .payment import PaymentGateway


class OrderService:
    def __init__(self, db: MemoryDB, payment_gateway: PaymentGateway, notification: NotificationService,
            credit_system: credit.CreditSystem, rec_engine: RecommendationEngine) -> None:
        self.db = db
        self.payment_gateway = payment_gateway
        self.notification = notification
        self.credit_system = credit_system
        self.rec_engine = rec_engine

    def create_order(self, buyer_id: str, items: List[Tuple[str, int]]) -> Order:
        total = 0
        merchant_id = None
        parsed_items = []
        for pid, qty in items:
            p = self.db.get_product(pid)
            if not p:
                raise ValueError("product not found")
            if p.stock < qty:
                raise ValueError("insufficient stock")
            if merchant_id is None:
                merchant_id = p.merchant_id
            elif merchant_id != p.merchant_id:
                raise ValueError("all items must be from same merchant in demo")
            total += p.price_cents * qty
            parsed_items.append(OrderItem(product_id=pid, quantity=qty))
        order = Order(order_id=gen_id("o_"), buyer_id=buyer_id, merchant_id=merchant_id or "unknown",
                      items=parsed_items, total_cents=total)
        self.db.add_order(order)
        for pid, _ in items:
            self.rec_engine.record_view(buyer_id, pid)
        return order

    def pay_order(self, order_id: str, succeed_rate: float = 0.95):
        order = self.db.get_order(order_id)
        if not order:
            raise ValueError("order not found")
        if order.status != OrderStatus.CREATED:
            raise ValueError("order not payable")
        pay = self.payment_gateway.create_payment(order)
        processed = self.payment_gateway.process_payment(pay, succeed_rate=succeed_rate)
        if processed.status == "success":
            order.mark_paid(processed.payment_id)
            for it in order.items:
                p = self.db.get_product(it.product_id)
                if p:
                    p.stock = max(0, p.stock - it.quantity)
                    p.sold += it.quantity
                    self.rec_engine.record_purchase(order.buyer_id, it.product_id)
            self.credit_system.adjust_for_payment(order.buyer_id, True)
        else:
            self.credit_system.adjust_for_payment(order.buyer_id, False)
        return processed
