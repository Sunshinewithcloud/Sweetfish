import pytest
from sweetfish.db import MemoryDB
from sweetfish.services.auth import AuthService
from sweetfish.models import BaseUser, Admin, Merchant


@pytest.fixture
def db():
    return MemoryDB()


@pytest.fixture
def auth(db):
    return AuthService(db)


def test_register_user(auth):
    user = auth.register("123", "pwd")
    assert isinstance(user, BaseUser)
    assert user.phone == "123"


def test_register_admin(auth):
    admin = auth.register("admin", "pwd", role="ADMIN")
    assert isinstance(admin, Admin)


def test_register_merchant(auth):
    merchant = auth.register("m1", "pwd", role="MERCHANT")
    assert isinstance(merchant, Merchant)


def test_register_duplicate_phone(auth):
    auth.register("123", "pwd")
    with pytest.raises(ValueError):
        auth.register("123", "pwd")


def test_register_invalid_role(auth):
    with pytest.raises(ValueError):
        auth.register("123", "pwd", role="INVALID")


def test_register_empty_phone(auth):
    with pytest.raises(ValueError):
        auth.register("", "pwd")


def test_register_empty_password(auth):
    with pytest.raises(ValueError):
        auth.register("123", "")


def test_register_phone_saved_in_db(auth, db):
    auth.register("123", "pwd")
    assert db.get_user_by_phone("123") is not None


def test_register_role_case_insensitive(auth):
    user = auth.register("u2", "pwd", role="user")
    assert isinstance(user, BaseUser)


def test_multiple_users(auth, db):
    auth.register("1", "a")
    auth.register("2", "b")
    assert len(db.users) == 2
