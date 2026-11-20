"""后台管理路由 - 用户/书籍/订单管理"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional

from app.database import get_db
from app.models.user import User
from app.models.book import Book
from app.models.order import Order
from app.models.coin import CoinTransaction
from app.utils.auth import require_admin

router = APIRouter()


# ==================== 用户管理 ====================

@router.get("/users")
def list_users(db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    """获取所有用户列表"""
    users = db.query(User).order_by(User.id).all()
    items = []
    for u in users:
        items.append({
            "id": u.id,
            "username": u.username,
            "nickname": u.nickname,
            "school": u.school,
            "coin_balance": u.coin_balance,
            "is_admin": u.is_admin,
            "is_active": u.is_active,
            "created_at": u.created_at.strftime("%Y-%m-%d %H:%M") if u.created_at else ""
        })
    return {"items": items}


@router.put("/users/{user_id}/toggle")
def toggle_user(user_id: int, db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    """启用/禁用用户"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    if user.is_admin:
        raise HTTPException(status_code=400, detail="不能禁用管理员")
    user.is_active = not user.is_active
    db.commit()
    return {"message": "操作成功", "is_active": user.is_active}


class AdjustCoinsRequest(BaseModel):
    amount: int


@router.post("/users/{user_id}/adjust-coins")
def adjust_coins(user_id: int, data: AdjustCoinsRequest, db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    """调整用户书币"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")

    if user.coin_balance + data.amount < 0:
        raise HTTPException(status_code=400, detail="余额不能为负数")

    # 记录交易
    tx = CoinTransaction(
        user_id=user_id,
        amount=data.amount,
        balance_after=user.coin_balance + data.amount,
        tx_type="admin_reward" if data.amount > 0 else "admin_deduct",
        description=f"管理员调整: {'+' if data.amount > 0 else ''}{data.amount}"
    )
    db.add(tx)
    user.coin_balance += data.amount
    db.commit()
    return {"message": "调整成功", "new_balance": user.coin_balance}


# ==================== 书籍管理 ====================

@router.get("/books")
def list_books(db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    """获取所有书籍列表"""
    books = db.query(Book).order_by(Book.id.desc()).all()
    items = []
    for b in books:
        seller = db.query(User).filter(User.id == b.seller_id).first()
        items.append({
            "id": b.id,
            "title": b.title,
            "seller_name": seller.nickname if seller else "未知",
            "price": b.price,
            "status": b.status,
            "created_at": b.created_at.strftime("%Y-%m-%d %H:%M") if b.created_at else ""
        })
    return {"items": items}


@router.delete("/books/{book_id}")
def remove_book(book_id: int, db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    """下架书籍"""
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="书籍不存在")
    book.status = "removed"
    db.commit()
    return {"message": "已下架"}


# ==================== 订单管理 ====================

@router.get("/orders")
def list_orders(db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    """获取所有订单列表"""
    orders = db.query(Order).order_by(Order.id.desc()).all()
    items = []
    for o in orders:
        book = db.query(Book).filter(Book.id == o.book_id).first()
        buyer = db.query(User).filter(User.id == o.buyer_id).first()
        seller = db.query(User).filter(User.id == o.seller_id).first()
        items.append({
            "id": o.id,
            "book_title": book.title if book else "未知",
            "buyer_name": buyer.nickname if buyer else "未知",
            "seller_name": seller.nickname if seller else "未知",
            "price": o.price,
            "status": o.status,
            "created_at": o.created_at.strftime("%Y-%m-%d %H:%M") if o.created_at else ""
        })
    return {"items": items}
