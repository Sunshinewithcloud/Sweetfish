"""Module adjusted to satisfy style checks."""

from sweetfish.db import MemoryDB
from sweetfish.models import Role
from sweetfish.services.auth import AuthService
from sweetfish.ui.app import SweetFishApp

if __name__ == "__main__":
    db = MemoryDB()
    auth = AuthService(db)

    admin = db.get_user_by_phone("000000")
    if not admin:
        # 默认管理员: 账号 000000 密码 admin123
        admin = auth.register_user("000000", "Admin", "admin123")
        admin.role = Role.ADMIN
        db.users[admin.user_id] = admin
    else:
        print("ℹ️ 管理员账号已存在。")

    app = SweetFishApp(db)
    app.mainloop()
