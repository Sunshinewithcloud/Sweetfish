"""Module adjusted to satisfy style checks."""

from ..db import MemoryDB
from ..models import Review, gen_id


class ReviewService:

    def __init__(self, db: MemoryDB) -> None:
        self.db = db

    def add_review(self, product_id: str, user_id: str, rating: int, comment: str):
        if rating < 1 or rating > 5:
            raise ValueError("rating must be 1..5")
        r = Review(
            review_id=gen_id("r_"),
            product_id=product_id,
            user_id=user_id,
            rating=rating,
            comment=comment,
        )
        self.db.add_review(r)
        return r
