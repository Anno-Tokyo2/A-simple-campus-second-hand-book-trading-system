"""订单路由 - 购买/确认收货/书币交易"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.database import get_db
from app.models.book import Book
from app.models.order import Order
from app.models.user import User
from app.models.coin import CoinTransaction
from app.utils.auth import get_current_user

router = APIRouter()


class CreateOrder(BaseModel):
    book_id: int


@router.post("")
def create_order(data: CreateOrder, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    """购买书籍 - 创建订单并扣款"""
    book = db.query(Book).filter(Book.id == data.book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="书籍不存在")
    if book.status != "available":
        raise HTTPException(status_code=400, detail="该书已售出或下架")
    if book.seller_id == user.id:
        raise HTTPException(status_code=400, detail="不能购买自己发布的书籍")

    # 检查余额
    if user.coin_balance < book.price:
        raise HTTPException(status_code=400, detail="书币余额不足")

    # 事务：扣买家币、冻结订单
    user.coin_balance = int(user.coin_balance - book.price)
    book.status = "sold"

    order = Order(
        book_id=book.id,
        buyer_id=user.id,
        seller_id=book.seller_id,
        price=book.price,
        status="pending"
    )
    db.add(order)

    # 记录买家扣款
    tx_buyer = CoinTransaction(
        user_id=user.id,
        amount=int(-book.price),
        balance_after=user.coin_balance,
        tx_type="buy",
        description=f"购买《{book.title}》"
    )
    db.add(tx_buyer)
    db.commit()
    db.refresh(order)

    return {
        "message": "购买成功，等待确认收货",
        "order_id": order.id,
        "price": order.price,
        "new_balance": user.coin_balance
    }


@router.post("/{order_id}/confirm")
def confirm_order(order_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    """确认收货 - 书币转入卖家"""
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="订单不存在")
    if order.buyer_id != user.id:
        raise HTTPException(status_code=403, detail="只有买家才能确认收货")
    if order.status != "pending":
        raise HTTPException(status_code=400, detail="订单状态不正确")

    # 打币给卖家
    seller = db.query(User).filter(User.id == order.seller_id).first()
    if not seller:
        raise HTTPException(status_code=500, detail="卖家不存在")

    seller.coin_balance = int(seller.coin_balance + order.price)
    order.status = "completed"

    tx_seller = CoinTransaction(
        user_id=seller.id,
        amount=int(order.price),
        balance_after=seller.coin_balance,
        tx_type="sell",
        description=f"出售书籍收入"
    )
    db.add(tx_seller)
    db.commit()

    return {
        "message": "确认收货成功，书币已转给卖家",
        "seller_received": order.price,
        "seller_balance": seller.coin_balance
    }


@router.get("")
def list_orders(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    """获取当前用户的订单"""
    orders = db.query(Order).filter(
        (Order.buyer_id == user.id) | (Order.seller_id == user.id)
    ).order_by(Order.created_at.desc()).all()

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
            "buyer_id": o.buyer_id,
            "seller_id": o.seller_id,
            "price": o.price,
            "status": o.status,
            "created_at": o.created_at.strftime("%Y-%m-%d %H:%M") if o.created_at else ""
        })
    return {"items": items}
