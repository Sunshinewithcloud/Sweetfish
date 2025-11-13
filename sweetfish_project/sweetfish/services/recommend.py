"""Module adjusted to satisfy style checks."""

from typing import List

from ..db import MemoryDB
from ..models import Product


class RecommendationEngine:

    def __init__(self, db: MemoryDB) -> None:
        self.db = db
        self.user_history = {}

    def record_view(self, user_id: str, product_id: str) -> None:
        self.user_history.setdefault(user_id, []).append(product_id)
        p = self.db.get_product(product_id)
        if p:
            p.views += 1

    def record_purchase(self, user_id: str, product_id: str) -> None:
        self.user_history.setdefault(user_id, []).append(product_id)
        p = self.db.get_product(product_id)
        if p:
            p.sold += 1

    def recommend_for_user(self, user_id: str, top_k: int = 6) -> List[Product]:
        history = self.user_history.get(user_id, [])
        if not history:
            prods = list(self.db.products.values())
            prods.sort(key=lambda x: (-x.promotion_rank, -x.views, -x.sold))
            return prods[:top_k]
        tag_scores = {}
        for pid in history[-10:]:
            p = self.db.get_product(pid)
            if not p:
                continue
            for t in p.tags:
                tag_scores[t] = tag_scores.get(t, 0) + 1
        scored = []
        for p in self.db.products.values():
            tag_overlap = sum(tag_scores.get(t, 0) for t in p.tags)
            score = tag_overlap * 5 + p.promotion_rank * 2 + p.views * 0.01 + p.sold * 0.1
            scored.append((score, p))
        scored.sort(key=lambda z: -z[0])
        return [p for (_, p) in scored[:top_k]]
