"""Module adjusted to satisfy style checks."""

from typing import List, Optional, Set

from ..db import MemoryDB
from ..models import Product, gen_id


class ProductService:
    def __init__(self, db: MemoryDB) -> None:
        self.db = db

    def create_product(self, merchant_id: str, title: str, description: str, price_cents: int,
                       stock: int = 0, allow_bargain: bool = True, tags: Optional[Set[str]] = None) -> Product:
        pid = gen_id("p_")
        p = Product(product_id=pid, merchant_id=merchant_id, title=title,
                    description=description, price_cents=price_cents, stock=stock, allow_bargain=allow_bargain)
        if tags:
            p.tags = set(tags)
        self.db.add_product(p)
        return p

    def list_for_merchant(self, merchant_id: str) -> List[Product]:
        return [p for p in self.db.products.values() if p.merchant_id == merchant_id]

    def update_stock(self, product_id: str, delta: int) -> Product:
        p = self.db.get_product(product_id)
        if not p:
            raise ValueError("product not found")
        p.stock += delta
        return p

    def search(self, keyword: str = "") -> List[Product]:
        return self.db.search_products(keyword)
