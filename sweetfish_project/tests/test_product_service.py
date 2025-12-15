import pytest
from sweetfish.db import MemoryDB
from sweetfish.services.product import ProductService

MERCHANT_ID = "m_test"

@pytest.fixture
def db():
    return MemoryDB()


@pytest.fixture
def service(db):
    return ProductService(db)


def test_create_product(service):
    p = service.create_product(MERCHANT_ID,"apple", "apple", 10)
    assert p.title == "apple"


def test_create_product_negative_price(service):
    with pytest.raises(ValueError):
        service.create_product(MERCHANT_ID,"bad","bad", -1)


def test_create_product_empty_name(service):
    with pytest.raises(ValueError):
        service.create_product(MERCHANT_ID,"","", 10)


def test_get_product(service):
    p = service.create_product(MERCHANT_ID,"apple","apple", 10)
    found = service.get_product(p.product_id)
    assert found == p


def test_get_nonexistent_product(service):
    assert service.get_product("not_exist") is None


def test_delete_product(service):
    p = service.create_product(MERCHANT_ID,"apple","apple", 10)
    service.delete_product(p.product_id)
    assert service.get_product(p.product_id) is None


def test_delete_nonexistent_product(service):
    with pytest.raises(ValueError):
        service.delete_product("xxx")


def test_multiple_products(service):
    service.create_product(MERCHANT_ID,"a", "a",1)
    service.create_product(MERCHANT_ID,"b", "b",2)
    assert len(service.db.products) == 2


def test_duplicate_product_name_allowed(service):
    service.create_product(MERCHANT_ID,"a","a", 1)
    service.create_product(MERCHANT_ID,"a","a", 2)
    assert len(service.db.products) == 2


def test_product_price_type(service):
    p = service.create_product(MERCHANT_ID,"apple","apple", 10)
    assert isinstance(p.price_cents, int)
