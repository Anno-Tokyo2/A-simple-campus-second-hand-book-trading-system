"""书籍路由 - 发布/搜索/详情"""
import os
import uuid
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional

from app.database import get_db
from app.models.book import Book
from app.models.user import User
from app.utils.auth import get_current_user, get_optional_user

UPLOAD_DIR = Path(__file__).parent.parent.parent.parent / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)

router = APIRouter()


class CreateBook(BaseModel):
    title: str
    author: Optional[str] = ""
    publisher: Optional[str] = ""
    isbn: Optional[str] = ""
    price: float
    original_price: Optional[float] = 0
    condition: Optional[str] = "九成新"
    category: Optional[str] = ""
    description: Optional[str] = ""


@router.get("")
def list_books(
    category: Optional[str] = None,
    search: Optional[str] = None,
    sort: Optional[str] = "newest",
    seller_id: Optional[str] = None,
    limit: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_user)
):
    """获取书籍列表（默认仅在售）"""
    query = db.query(Book)

    if seller_id == "me":
        if not current_user:
            raise HTTPException(status_code=401, detail="请先登录")
        query = query.filter(Book.seller_id == current_user.id)
    elif seller_id:
        query = query.filter(Book.seller_id == int(seller_id))
    else:
        # 书市只显示在售
        query = query.filter(Book.status == "available")

    if category:
        query = query.filter(Book.category == category)
    if search:
        query = query.filter(
            (Book.title.contains(search)) | (Book.author.contains(search))
        )

    if sort == "price-asc":
        query = query.order_by(Book.price.asc())
    elif sort == "price-desc":
        query = query.order_by(Book.price.desc())
    else:
        query = query.order_by(Book.created_at.desc())

    if limit:
        query = query.limit(limit)

    books = query.all()
    items = []
    for b in books:
        items.append({
            "id": b.id,
            "title": b.title,
            "author": b.author,
            "publisher": b.publisher,
            "isbn": b.isbn,
            "price": b.price,
            "original_price": b.original_price,
            "condition": b.condition,
            "category": b.category,
            "description": b.description,
            "cover_image": b.cover_image or "",
            "status": b.status,
            "view_count": b.view_count,
            "created_at": b.created_at.strftime("%Y-%m-%d") if b.created_at else ""
        })
    return {"items": items}


@router.get("/{book_id}")
def get_book(book_id: int, db: Session = Depends(get_db)):
    """获取书籍详情"""
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="书籍不存在")

    seller = db.query(User).filter(User.id == book.seller_id).first()
    return {
        "id": book.id,
        "title": book.title,
        "author": book.author,
        "publisher": book.publisher,
        "isbn": book.isbn,
        "price": book.price,
        "original_price": book.original_price,
        "condition": book.condition,
        "category": book.category,
        "description": book.description,
        "cover_image": book.cover_image or "",
        "status": book.status,
        "view_count": book.view_count,
        "created_at": book.created_at.strftime("%Y-%m-%d") if book.created_at else "",
        "seller": {
            "id": seller.id,
            "nickname": seller.nickname,
            "school": seller.school
        } if seller else None
    }


@router.post("")
async def create_book(
    title: str = Form(...),
    price: float = Form(...),
    author: str = Form(""),
    publisher: str = Form(""),
    isbn: str = Form(""),
    original_price: float = Form(0),
    condition: str = Form("九成新"),
    category: str = Form(""),
    description: str = Form(""),
    cover: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    """发布书籍（支持封面图片上传）"""
    cover_filename = ""
    if cover and cover.filename:
        ext = os.path.splitext(cover.filename)[1].lower()
        if ext in (".jpg", ".jpeg", ".png", ".webp", ".gif"):
            cover_filename = f"{uuid.uuid4().hex}{ext}"
            file_path = UPLOAD_DIR / cover_filename
            content = await cover.read()
            with open(file_path, "wb") as f:
                f.write(content)

    book = Book(
        seller_id=user.id,
        title=title,
        author=author or "",
        publisher=publisher or "",
        isbn=isbn or "",
        price=price,
        original_price=original_price or 0,
        condition=condition or "九成新",
        category=category or "",
        description=description or "",
        cover_image=cover_filename,
        status="available"
    )
    db.add(book)
    db.commit()
    db.refresh(book)
    return {"message": "发布成功", "id": book.id}


@router.put("/{book_id}")
async def update_book(
    book_id: int,
    title: str = Form(...),
    price: float = Form(...),
    author: str = Form(""),
    publisher: str = Form(""),
    isbn: str = Form(""),
    original_price: float = Form(0),
    condition: str = Form("九成新"),
    category: str = Form(""),
    description: str = Form(""),
    cover: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    """编辑书籍（支持封面图片上传）"""
    book = db.query(Book).filter(Book.id == book_id, Book.seller_id == user.id).first()
    if not book:
        raise HTTPException(status_code=404, detail="书籍不存在或无权编辑")

    if cover and cover.filename:
        ext = os.path.splitext(cover.filename)[1].lower()
        if ext in (".jpg", ".jpeg", ".png", ".webp", ".gif"):
            cover_filename = f"{uuid.uuid4().hex}{ext}"
            file_path = UPLOAD_DIR / cover_filename
            content = await cover.read()
            with open(file_path, "wb") as f:
                f.write(content)
            book.cover_image = cover_filename

    book.title = title
    book.author = author or ""
    book.publisher = publisher or ""
    book.isbn = isbn or ""
    book.price = price
    book.original_price = original_price or 0
    book.condition = condition or "九成新"
    book.category = category or ""
    book.description = description or ""
    db.commit()
    return {"message": "编辑成功"}


@router.put("/{book_id}/status")
def update_book_status(book_id: int, status: str, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    """修改书籍状态（下架/重新上架）"""
    book = db.query(Book).filter(Book.id == book_id, Book.seller_id == user.id).first()
    if not book:
        raise HTTPException(status_code=404, detail="书籍不存在或无权操作")
    if status not in ("available", "removed"):
        raise HTTPException(status_code=400, detail="状态值无效")
    book.status = status
    db.commit()
    return {"message": "已下架" if status == "removed" else "已重新上架"}
