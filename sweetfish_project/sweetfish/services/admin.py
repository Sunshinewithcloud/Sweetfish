"""Module adjusted to satisfy style checks."""

from ..db import MemoryDB


class AdminService:


    def __init__(self, db: MemoryDB) -> None:

        self.db = db

    def generate_sales_report(self):

        total_sales = 0
        for product in self.db.products.values():
            total_sales += product.sold * product.price_cents

        all_products = list(self.db.products.values())
        all_products.sort(key=lambda p: p.sold, reverse=True)
        top_5_products = all_products[:5]

        top_list = []
        for p in top_5_products:
            top_list.append((p.product_id, p.title, p.sold))

        return {"total_sales_cents": total_sales, "top": top_list}
