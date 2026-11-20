"""用户路由 - 注册/登录/个人信息"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.models.coin import CoinTransaction
from app.schemas.user import UserRegister, UserLogin, UserResponse, TokenResponse
from app.utils.auth import hash_password, verify_password, create_token, get_current_user

router = APIRouter()


@router.post("/register", response_model=dict)
def register(data: UserRegister, db: Session = Depends(get_db)):
    """用户注册"""
    # 检查用户名是否已存在
    existing = db.query(User).filter(User.username == data.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="用户名已存在")

    # 检查密码长度
    if len(data.password) < 6:
        raise HTTPException(status_code=400, detail="密码至少6位")

    # 创建用户
    user = User(
        username=data.username,
        password_hash=hash_password(data.password),
        nickname=data.nickname or data.username,
        school=data.school or "",
        coin_balance=100,  # 新用户初始100书币
        is_admin=False,
        is_active=True
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    return {"message": "注册成功", "user_id": user.id}


@router.post("/login", response_model=TokenResponse)
def login(data: UserLogin, db: Session = Depends(get_db)):
    """用户登录"""
    user = db.query(User).filter(User.username == data.username).first()
    if not user:
        raise HTTPException(status_code=401, detail="用户名或密码错误")
    if not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="用户名或密码错误")
    if not user.is_active:
        raise HTTPException(status_code=403, detail="账号已被禁用")

    token = create_token(user.id, user.username)
    return TokenResponse(
        token=token,
        user=UserResponse.model_validate(user)
    )


@router.get("/me", response_model=UserResponse)
def get_me(user: User = Depends(get_current_user)):
    """获取当前用户信息"""
    return UserResponse.model_validate(user)


@router.get("/coin-history")
def get_coin_history(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """获取书币交易记录"""
    txs = db.query(CoinTransaction).filter(CoinTransaction.user_id == user.id).order_by(CoinTransaction.created_at.desc()).all()
    items = [{
        "id": tx.id,
        "description": tx.description,
        "amount": tx.amount,
        "balance_after": tx.balance_after,
        "created_at": tx.created_at.strftime("%Y-%m-%d %H:%M") if tx.created_at else ""
    } for tx in txs]
    return {"items": items}
