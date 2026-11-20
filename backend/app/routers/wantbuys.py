"""求购路由 - 发布/回应"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional

from app.database import get_db
from app.models.wantbuy import WantBuy
from app.models.user import User
from app.models.message import Message
from app.utils.auth import get_current_user

router = APIRouter()


class CreateWantBuy(BaseModel):
    title: str
    author: Optional[str] = ""
    isbn: Optional[str] = ""
    expected_price: Optional[float] = None
    description: Optional[str] = ""


class RespondWantBuy(BaseModel):
    message: str
    price: Optional[float] = None


@router.post("")
def create_wantbuy(data: CreateWantBuy, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    """发布求购"""
    wb = WantBuy(
        user_id=user.id,
        title=data.title,
        author=data.author or "",
        isbn=data.isbn or "",
        expected_price=data.expected_price,
        description=data.description or "",
        status="open"
    )
    db.add(wb)
    db.commit()
    return {"message": "发布成功", "id": wb.id}


@router.post("/{wantbuy_id}/respond")
def respond_wantbuy(wantbuy_id: int, data: RespondWantBuy, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    """回应求购 - 通过站内信联系求购者"""
    wb = db.query(WantBuy).filter(WantBuy.id == wantbuy_id).first()
    if not wb:
        raise HTTPException(status_code=404, detail="求购信息不存在")
    if wb.user_id == user.id:
        raise HTTPException(status_code=400, detail="不能回应自己的求购")
    if wb.status != "open":
        raise HTTPException(status_code=400, detail="该求购已关闭")

    price_info = f"，售价 {data.price} 书币" if data.price else ""
    content = f"你好，我有《{wb.title}》这本书{price_info}。{data.message}"

    msg = Message(
        sender_id=user.id,
        receiver_id=wb.user_id,
        content=content
    )
    db.add(msg)
    db.commit()

    return {"message": "回应已发送给求购者"}


@router.get("")
def list_wantbuys(db: Session = Depends(get_db)):
    """获取求购列表"""
    wbs = db.query(WantBuy).order_by(WantBuy.created_at.desc()).all()
    items = []
    for wb in wbs:
        user = db.query(User).filter(User.id == wb.user_id).first()
        items.append({
            "id": wb.id,
            "title": wb.title,
            "author": wb.author,
            "isbn": wb.isbn,
            "expected_price": wb.expected_price,
            "description": wb.description,
            "status": wb.status,
            "user": {"id": wb.user_id, "nickname": user.nickname if user else "未知", "school": user.school if user else ""},
            "created_at": wb.created_at.strftime("%Y-%m-%d") if wb.created_at else ""
        })
    return {"items": items}
