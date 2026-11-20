"""书币交易记录模型"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from app.database import Base

class CoinTransaction(Base):
    __tablename__ = "coin_transactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    amount = Column(Integer, nullable=False)  # 正数为收入，负数为支出
    balance_after = Column(Integer, nullable=False)  # 交易后余额
    tx_type = Column(String(30), nullable=False)  # buy/sell/admin_reward/admin_deduct
    reference_id = Column(Integer, nullable=True)  # 关联的订单ID等
    description = Column(String(200), default="")
    created_at = Column(DateTime, default=datetime.utcnow)
