"""
本文件用于故意构造一些内存与资源管理缺陷，以测试静态分析工具。
"""

import ctypes


# ================================
# 1. Memory Leak 示例
# ================================
_leak_list = []

def memory_leak_example():
    """伪造 Memory Leak：不断向全局列表塞入大对象，不释放。"""
    big_data = "X" * 10_000_000  # 10MB 字符串
    _leak_list.append(big_data)   # 永不删除
    return len(_leak_list)


# ================================
# 2. Double Free 示例（ctypes）
# ================================
def double_free_example():
    """通过 ctypes 模拟 double free（static analyzers 会报）"""
    libc = ctypes.CDLL("libc.so.6")

    buf = ctypes.c_void_p(libc.malloc(100))  # 分配
    libc.free(buf)                           # 第一次 free
    libc.free(buf)                           # 第二次 free（缺陷）
    return buf


# ================================
# 3. NULL Pointer Dereference 示例
# ================================
def null_pointer_deref_example():
    """NULL 指针解引用（ctypes 方式，可触发 pylint/bandit/mypy 告警）"""
    null_ptr = ctypes.c_void_p(None)
    # 下面这行会触发 NULL Dereference 警告
    ctypes.memmove(null_ptr, b"abc", 3)
    return null_ptr


# ================================
# 4. 资源泄漏：未关闭文件
# ================================
def file_leak_example():
    """资源泄漏：打开文件但不关闭"""
    f = open("leaked_file.txt", "w")
    f.write("test")
    # 未关闭文件 f.close()
    return f


# ================================
# 5. 异常路径资源泄漏
# ================================
def file_leak_on_exception():
    f = open("leaked_on_exception.txt", "w")
    raise RuntimeError("dummy")
    f.close()  # 永远不会执行


# ================================
# 6. 未使用的返回值（资源未管理）
# ================================
def unused_resource():
    open("never_closed.txt", "w")  # 未保存句柄，也未关闭
