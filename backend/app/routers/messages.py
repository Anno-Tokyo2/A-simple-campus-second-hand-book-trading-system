"""私信路由 - 站内消息"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional

from app.database import get_db
from app.models.message import Message
from app.models.user import User
from app.utils.auth import get_current_user

router = APIRouter()


class SendMessage(BaseModel):
    receiver_id: int
    content: str
    book_id: Optional[int] = None


@router.post("")
def send_message(data: SendMessage, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    """发送消息"""
    if data.receiver_id == user.id:
        raise HTTPException(status_code=400, detail="不能给自己发消息")

    receiver = db.query(User).filter(User.id == data.receiver_id).first()
    if not receiver:
        raise HTTPException(status_code=404, detail="接收者不存在")

    msg = Message(
        sender_id=user.id,
        receiver_id=data.receiver_id,
        content=data.content,
        book_id=data.book_id
    )
    db.add(msg)
    db.commit()
    return {"message": "发送成功", "id": msg.id}


@router.get("/conversations")
def list_conversations(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    """获取会话列表"""
    # 获取与当前用户相关的所有会话
    sent = db.query(Message.receiver_id).filter(Message.sender_id == user.id).distinct().all()
    received = db.query(Message.sender_id).filter(Message.receiver_id == user.id).distinct().all()

    user_ids = set()
    for r in sent:
        user_ids.add(r[0])
    for r in received:
        user_ids.add(r[0])

    items = []
    for uid in user_ids:
        other = db.query(User).filter(User.id == uid).first()
        if not other:
            continue
        # 最后一条消息
        last_msg = db.query(Message).filter(
            ((Message.sender_id == user.id) & (Message.receiver_id == uid)) |
            ((Message.sender_id == uid) & (Message.receiver_id == user.id))
        ).order_by(Message.created_at.desc()).first()

        # 未读数
        unread = db.query(Message).filter(
            Message.sender_id == uid, Message.receiver_id == user.id, Message.is_read == False
        ).count()

        items.append({
            "user_id": uid,
            "nickname": other.nickname,
            "last_message": last_msg.content if last_msg else "",
            "last_time": last_msg.created_at.strftime("%Y-%m-%d %H:%M") if last_msg else "",
            "unread": unread
        })

    items.sort(key=lambda x: x["last_time"], reverse=True)
    return {"items": items}


@router.get("/conversations/{other_id}")
def get_conversation(other_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    """获取与某人的聊天记录"""
    msgs = db.query(Message).filter(
        ((Message.sender_id == user.id) & (Message.receiver_id == other_id)) |
        ((Message.sender_id == other_id) & (Message.receiver_id == user.id))
    ).order_by(Message.created_at.asc()).all()

    # 标记已读
    db.query(Message).filter(
        Message.sender_id == other_id, Message.receiver_id == user.id, Message.is_read == False
    ).update({"is_read": True})
    db.commit()

    items = [{
        "id": m.id,
        "sender_id": m.sender_id,
        "content": m.content,
        "is_read": m.is_read,
        "created_at": m.created_at.strftime("%Y-%m-%d %H:%M")
    } for m in msgs]

    return {"items": items}
