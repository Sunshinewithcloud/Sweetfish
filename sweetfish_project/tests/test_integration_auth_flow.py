"""
集成测试：main → AuthService → MemoryDB
"""

from sweetfish.db import MemoryDB
from sweetfish.services.auth import AuthService
from sweetfish.models import Role

def test_user_register_integration():
    # 模拟 main.py 中创建对象的方式
    db = MemoryDB()
    auth_service = AuthService(db)

    # 模拟用户注册
    user = auth_service.register("13800000000", "123456")

    # 验证 service 返回结果
    assert user is not None
    assert user.phone == "13800000000"

    # 验证数据是否正确写入 DB
    stored = db.get_user_by_phone("13800000000")
    assert stored is user


def test_admin_register_integration():
    db = MemoryDB()
    auth_service = AuthService(db)

    admin = auth_service.register("admin", "adminpwd", role="ADMIN")

    assert admin.role == Role.ADMIN
    assert db.get_user_by_phone("admin") is not None


def test_duplicate_register_integration():
    db = MemoryDB()
    auth_service = AuthService(db)

    auth_service.register("u1", "pwd")

    try:
        auth_service.register("u1", "pwd")
        assert False, "duplicate register should fail"
    except ValueError:
        assert True
