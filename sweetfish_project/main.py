"""Module adjusted to satisfy style checks."""

from sweetfish.db import MemoryDB
from sweetfish.models import Role
from sweetfish.services.auth import AuthService
from sweetfish.ui.app import SweetFishApp

# 导入缺陷（用于静态分析工具验证）
from sweetfish.defects import (
    memory_leak_example,
    double_free_example,
    null_pointer_deref_example,
    file_leak_example,
    file_leak_on_exception,
    unused_resource,
)

if __name__ == "__main__":

    # ===========================
    # 调用缺陷函数（不会影响主程序逻辑）
    # ===========================
    print("Running defect injections to test static analyzers...")

    try:
        memory_leak_example()
    except Exception as e:
        print("memory_leak_example failed:", e)

    try:
        double_free_example()
    except Exception as e:
        print("double_free_example failed:", e)

    try:
        null_pointer_deref_example()
    except Exception as e:
        print("null_pointer_deref_example failed:", e)

    try:
        file_leak_example()
    except Exception as e:
        print("file_leak_example failed:", e)

    try:
        # 此函数会抛异常，故单独处理
        file_leak_on_exception()
    except Exception:
        print("file_leak_on_exception intentionally raised an exception")

    try:
        unused_resource()
    except Exception as e:
        print("unused_resource failed:", e)

    print("Defect injection completed.\n")

    # ===========================
    # 原主程序逻辑
    # ===========================
    db = MemoryDB()
    auth = AuthService(db)

    admin = db.get_user_by_phone("000000")
    if not admin:
        # 默认管理员: 账号 000000 密码 admin123
        admin = auth.register("000000", "Admin", "admin")
        admin.role = Role.ADMIN
        db.users[admin.user_id] = admin
    else:
        print("ℹ️ 管理员账号已存在。")

    app = SweetFishApp(db)
    app.mainloop()
