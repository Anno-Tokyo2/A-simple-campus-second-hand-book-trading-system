"""书籍数据模型"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, Text
from app.database import Base

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    seller_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(200), nullable=False)
    author = Column(String(100), default="")
    publisher = Column(String(100), default="")
    isbn = Column(String(20), default="", index=True)
    price = Column(Float, nullable=False)  # 书币价格
    original_price = Column(Float, default=0)  # 原价
    condition = Column(String(20), default="九成新")  # 成色
    category = Column(String(50), default="")  # 分类/风格
    description = Column(Text, default="")
    cover_image = Column(String(255), default="")  # 封面图路径
    images = Column(Text, default="[]")  # JSON 格式图片列表
    status = Column(String(20), default="available")  # available/sold/removed
    view_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
