"""
集成测试：main → ProductService → MemoryDB
"""

from sweetfish.db import MemoryDB
from sweetfish.services.product import ProductService

MERCHANT_ID = "m_test"

def test_product_crud_integration():
    db = MemoryDB()
    product_service = ProductService(db)

    # 创建商品
    product = product_service.create_product(MERCHANT_ID,"apple","apple", 5)
    assert product.title == "apple"

    # 查询商品
    found = product_service.get_product(product.product_id)
    assert found is product

    # 删除商品
    product_service.delete_product(product.product_id)
    assert product_service.get_product(product.product_id) is None


def test_multiple_product_integration():
    db = MemoryDB()
    product_service = ProductService(db)

    p1 = product_service.create_product(MERCHANT_ID,"a", "a",1)
    p2 = product_service.create_product(MERCHANT_ID,"b", "b",2)

    assert len(db.products) == 2
    assert p1.product_id in db.products
    assert p2.product_id in db.products


def test_delete_nonexistent_product_integration():
    db = MemoryDB()
    product_service = ProductService(db)

    try:
        product_service.delete_product("not_exist")
        assert False, "should raise exception"
    except ValueError:
        assert True
