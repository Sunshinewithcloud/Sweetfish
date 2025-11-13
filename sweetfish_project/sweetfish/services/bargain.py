"""Module adjusted to satisfy style checks."""

import random
from datetime import datetime, timedelta

from ..db import MemoryDB
from ..models import Bargain, gen_id


class BargainService:

    def __init__(self, db: MemoryDB, notification) -> None:
        self.db = db
        self.notification = notification

    def start_bargain(
        self, requester_id: str, product_id: str, expires_minutes: int = 60
    ) -> Bargain:
        p = self.db.get_product(product_id)
        if not p:
            raise ValueError("product not found")
        if not p.allow_bargain:
            raise ValueError("no bargain")
        b = Bargain(
            bargain_id=gen_id("b_"),
            product_id=product_id,
            requester_id=requester_id,
            original_price_cents=p.price_cents,
            current_price_cents=p.price_cents,
        )
        b.expires_at = datetime.utcnow() + timedelta(minutes=expires_minutes)
        self.db.add_bargain(b)
        self.notification.push(requester_id, f"started bargain for {p.title}")
        return b

    def join_bargain(self, bid: str, user_id: str):
        b = self.db.get_bargain(bid)
        if not b:
            raise ValueError("bargain not found")
        if b.closed:
            raise ValueError("closed")
        cut = self._calculate_cut(b)
        b.participants.add(user_id)
        b.current_price_cents = max(0, b.current_price_cents - cut)
        self.notification.push(user_id, f"you cut {cut} cents")
        return b

    def _calculate_cut(self, b: Bargain) -> int:
        base = max(1, b.original_price_cents)
        pct = random.uniform(0.005, 0.05)
        part = max(0, len(b.participants))
        pct = min(0.15, pct + 0.002 * part)
        cut = int(base * pct)
        if cut <= 0:
            cut = 1
        return cut
