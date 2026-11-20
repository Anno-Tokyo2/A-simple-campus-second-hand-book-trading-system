"""校园二手书交易平台 - FastAPI 后端入口"""
import os
import sys

# 强制 Python 使用 UTF-8 编码，避免 Windows cp936 导致中文损坏
os.environ.setdefault("PYTHONUTF8", "1")
from pathlib import Path
from contextlib import asynccontextmanager

# 确保项目根目录在 Python 路径中
ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR))

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from sqlalchemy.orm import Session
from app.database import engine, Base, SessionLocal, get_db
from app.models.user import User
from app.utils.auth import hash_password
from app.routers import users, books, orders, messages, wantbuys, admin
from seed import seed as seed_data


def seed_admin():
    """创建管理员账号（如果不存在）"""
    db = SessionLocal()
    try:
        admin_user = db.query(User).filter(User.username == "admin").first()
        if not admin_user:
            admin_user = User(
                username="admin",
                password_hash=hash_password("admin123"),
                nickname="管理员",
                school="系统管理",
                coin_balance=99999,
                is_admin=True,
                is_active=True
            )
            db.add(admin_user)
            db.commit()
            print("[种子数据] 管理员账号已创建: admin / admin123")
        else:
            print("[种子数据] 管理员账号已存在，跳过")
    finally:
        db.close()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期：启动时初始化"""
    # 创建数据库表
    Base.metadata.create_all(bind=engine)
    # 运行种子数据（包含管理员账号）
    seed_data()
    print("[启动] 数据库初始化完成")
    yield
    print("[关闭] 应用退出")


app = FastAPI(
    title="校园二手书交易平台 API",
    description="提供用户注册登录、书籍交易、书币系统等功能",
    version="1.0.0",
    lifespan=lifespan
)

# CORS 配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 静态文件挂载
UPLOAD_DIR = ROOT_DIR / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)
app.mount("/static/uploads", StaticFiles(directory=str(UPLOAD_DIR)), name="uploads")

# 注册路由
app.include_router(users.router, prefix="/api/users", tags=["用户"])
app.include_router(books.router, prefix="/api/books", tags=["书籍"])
app.include_router(orders.router, prefix="/api/orders", tags=["订单"])
app.include_router(messages.router, prefix="/api/messages", tags=["私信"])
app.include_router(wantbuys.router, prefix="/api/wantbuys", tags=["求购"])
app.include_router(admin.router, prefix="/api/admin", tags=["后台管理"])


@app.get("/")
async def root():
    return {"message": "校园二手书交易平台 API 运行中"}


@app.get("/api/health")
async def health_check():
    return {"status": "ok", "version": "1.0.0"}


@app.get("/api/stats")
def get_stats(db: Session = Depends(get_db)):
    """首页统计数据"""
    from app.models.book import Book
    from app.models.user import User
    user_count = db.query(User).filter(User.is_active == True).count()
    book_count = db.query(Book).filter(Book.status == "available").count()
    return {"users": user_count, "books": book_count}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
