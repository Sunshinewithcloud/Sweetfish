"""Module adjusted to satisfy style checks."""

from typing import Dict

from ..db import MemoryDB


class CreditSystem:

    def __init__(self, db: MemoryDB) -> None:
        self.db = db
        self.scores: Dict[str, float] = {}

    def init_score(self, user_id: str) -> float:
        if user_id not in self.scores:
            self.scores[user_id] = 80.0
        return self.scores[user_id]

    def adjust_for_payment(self, user_id: str, success: bool) -> float:
        self.init_score(user_id)
        if success:
            self.scores[user_id] = min(100.0, self.scores[user_id] + 0.5)
        else:
            self.scores[user_id] = max(0.0, self.scores[user_id] - 2.0)
        return self.scores[user_id]

    def get_score(self, user_id: str) -> float:
        return self.scores.get(user_id, self.init_score(user_id))
