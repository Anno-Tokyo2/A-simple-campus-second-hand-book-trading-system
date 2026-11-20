"""求购信息数据模型"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, Text
from app.database import Base

class WantBuy(Base):
    __tablename__ = "wantbuys"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(200), nullable=False)
    author = Column(String(100), default="")
    isbn = Column(String(20), default="")
    expected_price = Column(Float, nullable=True)  # 预期价格(书币)
    description = Column(Text, default="")
    status = Column(String(20), default="open")  # open/matched/closed
    created_at = Column(DateTime, default=datetime.utcnow)
