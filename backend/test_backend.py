"""后端基础验证脚本 - 验证数据库建表和 FastAPI 启动"""
import sys
import os
from pathlib import Path

# Windows 控制台 UTF-8 支持
os.system("chcp 65001 >nul 2>&1")
sys.stdout.reconfigure(encoding='utf-8')

# 确保路径正确
ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR / "backend"))

def test_database():
    """验证数据库表创建"""
    print("=" * 50)
    print("1. 测试数据库建表...")
    from app.database import engine, Base, SessionLocal
    from app.models import User, Book, Order, CoinTransaction, Message, WantBuy

    # 创建所有表
    Base.metadata.create_all(bind=engine)

    # 验证表是否存在
    from sqlalchemy import inspect
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    expected_tables = ["users", "books", "orders", "coin_transactions", "messages", "wantbuys"]

    for table in expected_tables:
        if table in tables:
            print(f"   [OK] 表 '{table}' 创建成功")
        else:
            print(f"   [FAIL] 表 '{table}' 未找到")
            return False

    # 测试会话
    db = SessionLocal()
    user_count = db.query(User).count()
    print(f"   [OK] 数据库会话正常，当前用户数: {user_count}")
    db.close()

    print("   [通过] 数据库测试全部通过！")
    return True

def test_app_startup():
    """验证 FastAPI 应用能正常创建"""
    print("\n" + "=" * 50)
    print("2. 测试 FastAPI 应用创建...")
    try:
        from main import app
        routes = [r.path for r in app.routes]
        print(f"   [OK] 应用创建成功，共 {len(routes)} 个路由")
        for route in routes:
            if route != "/openapi.json":
                print(f"     - {route}")
        print("   [通过] FastAPI 应用测试通过！")
        return True
    except Exception as e:
        print(f"   [FAIL] 应用创建失败: {e}")
        return False

if __name__ == "__main__":
    print("校园二手书交易平台 - 后端验证")
    print("=" * 50)

    results = []
    results.append(test_database())
    results.append(test_app_startup())

    print("\n" + "=" * 50)
    if all(results):
        print("[OK] 所有测试通过！后端基础就绪。")
    else:
        print("[FAIL] 部分测试失败，请检查错误信息。")
        sys.exit(1)
