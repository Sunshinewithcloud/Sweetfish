"""Module adjusted to satisfy style checks."""

from typing import List, Optional, Set

from ..db import MemoryDB
from ..models import Product, gen_id


class ProductService:
    def __init__(self, db: MemoryDB) -> None:
        self.db = db

    def create_product(
            self,
            merchant_id: str,
            title: str,
            description: str,
            price_cents: int,
            stock: int = 0,
            allow_bargain: bool = True,
            tags: Optional[Set[str]] = None
    ) -> Product:
        # ----------- 参数校验（业务规则）-----------
        if not merchant_id:
            raise ValueError("merchant_id cannot be empty")

        if not title:
            raise ValueError("product title cannot be empty")

        if price_cents < 0:
            raise ValueError("price_cents must be non-negative")

        if stock < 0:
            raise ValueError("stock must be non-negative")

        # ----------- 创建商品 -----------
        pid = gen_id("p_")
        p = Product(
            product_id=pid,
            merchant_id=merchant_id,
            title=title,
            description=description,
            price_cents=price_cents,
            stock=stock,
            allow_bargain=allow_bargain
        )

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

    def get_product(self, product_id):
        return self.db.products.get(product_id)

    def delete_product(self, product_id):
        if product_id not in self.db.products:
            raise ValueError("商品不存在")
        del self.db.products[product_id]