# -*- coding: utf-8 -*-
"""种子数据脚本 - 创建演示用户、书籍、求购、消息等数据"""
import os
import sys

# 强制 Python 使用 UTF-8 编码
os.environ.setdefault("PYTHONUTF8", "1")
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT_DIR))

from app.database import engine, Base, SessionLocal
from app.models.user import User
from app.models.book import Book
from app.models.order import Order
from app.models.coin import CoinTransaction
from app.models.message import Message
from app.models.wantbuy import WantBuy
from app.utils.auth import hash_password

def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    # 检查是否已有完整种子数据（用 zhangsan 作为标记）
    if db.query(User).filter(User.username == "zhangsan").first():
        print("数据库已有种子数据，跳过")
        db.close()
        return

    # ==================== 用户 ====================
    users_data = [
        {"username": "admin", "nickname": "管理员", "school": "系统管理", "coins": 99999, "is_admin": True},
        {"username": "zhangsan", "nickname": "张同学", "school": "计算机学院", "coins": 285},
        {"username": "lisi", "nickname": "李同学", "school": "数学学院", "coins": 168},
        {"username": "wangwu", "nickname": "王同学", "school": "外语学院", "coins": 230},
        {"username": "zhaoliu", "nickname": "赵同学", "school": "物理学院", "coins": 42},
        {"username": "sunqi", "nickname": "孙同学", "school": "经济学院", "coins": 310},
        {"username": "zhouba", "nickname": "周同学", "school": "文学院", "coins": 155},
        {"username": "wujiu", "nickname": "吴同学", "school": "化学学院", "coins": 88},
        {"username": "zhengshi", "nickname": "郑同学", "school": "生命科学学院", "coins": 200},
        {"username": "liuyi", "nickname": "刘同学", "school": "信息工程学院", "coins": 175},
    ]

    users = []
    for u in users_data:
        existing = db.query(User).filter(User.username == u["username"]).first()
        if existing:
            users.append(existing)
            continue
        pwd = "admin123" if u.get("is_admin") else "123456"
        user = User(
            username=u["username"],
            password_hash=hash_password(pwd),
            nickname=u["nickname"],
            school=u["school"],
            coin_balance=u["coins"],
            is_admin=u.get("is_admin", False),
            is_active=True
        )
        db.add(user)
        users.append(user)
    db.commit()
    for u in users:
        db.refresh(u)
    print(f"[种子] 创建 {len(users)} 个用户")

    # ==================== 书籍 ====================
    books_data = [
        {"seller": 1, "title": "高等数学（第七版）上册", "author": "同济大学数学系", "publisher": "高等教育出版社", "isbn": "9787040396638", "price": 15, "orig": 46.5, "condition": "九成新", "category": "数学", "desc": "经典高数教材，少量笔记标注，重点章节有荧光笔标记。", "cover": "高等数学（第七版）上册.jpg"},
        {"seller": 1, "title": "线性代数", "author": "同济大学数学系", "publisher": "高等教育出版社", "isbn": "9787040396645", "price": 12, "orig": 39, "condition": "八成新", "category": "数学", "desc": "配套习题已做，答案页完整。", "cover": "线性代数.jpg"},
        {"seller": 2, "title": "数据结构与算法分析", "author": "Mark Allen Weiss", "publisher": "机械工业出版社", "isbn": "9787111127482", "price": 25, "orig": 69, "condition": "九成新", "category": "计算机", "desc": "C语言描述版本，代码示例清晰。", "cover": "数据结构与算法分析.jpg"},
        {"seller": 2, "title": "计算机网络", "author": "谢希仁", "publisher": "电子工业出版社", "isbn": "9787121159268", "price": 18, "orig": 52, "condition": "八成新", "category": "计算机", "desc": "第七版，课后习题已做。", "cover": "计算机网络.jpg"},
        {"seller": 3, "title": "大学英语综合教程1", "author": "李荫华", "publisher": "上海外语教育出版社", "isbn": "9787544638289", "price": 10, "orig": 58, "condition": "七成新", "category": "英语", "desc": "有少量铅笔笔记，可擦除。", "cover": "大学英语综合教程.jpg"},
        {"seller": 3, "title": "概率论与数理统计", "author": "浙江大学", "publisher": "高等教育出版社", "isbn": "9787040238969", "price": 12, "orig": 38, "condition": "八成新", "category": "数学", "desc": "第四版，考研必备。", "cover": "概率论与数理统计.jpg"},
        {"seller": 4, "title": "操作系统概念", "author": "Abraham Silberschatz", "publisher": "机械工业出版社", "isbn": "9787111234517", "price": 30, "orig": 89, "condition": "九五新", "category": "计算机", "desc": "英文原版，几乎全新。", "cover": "操作系统概念.jpg"},
        {"seller": 4, "title": "数据库系统概论", "author": "王珊", "publisher": "高等教育出版社", "isbn": "9787040406641", "price": 15, "orig": 45, "condition": "八成新", "category": "计算机", "desc": "第五版，有部分课后答案。", "cover": "数据库系统概论.jpg"},
        {"seller": 5, "title": "Python编程导论", "author": "John Guttag", "publisher": "人民邮电出版社", "isbn": "9787115434678", "price": 20, "orig": 65, "condition": "九成新", "category": "计算机", "desc": "适合编程入门，代码示例丰富。", "cover": "Python编程导论.jpg"},
        {"seller": 5, "title": "微观经济学", "author": "曼昆", "publisher": "北京大学出版社", "isbn": "9787301150894", "price": 22, "orig": 72, "condition": "九成新", "category": "经济", "desc": "第九版，核心教材。", "cover": "微观经济学.jpg"},
        {"seller": 6, "title": "大学物理", "author": "马文蔚", "publisher": "高等教育出版社", "isbn": "9787040378740", "price": 15, "orig": 49, "condition": "八成新", "category": "物理", "desc": "上下册合售。", "cover": "大学物理.jpg"},
        {"seller": 6, "title": "人工智能导论", "author": "Stuart Russell", "publisher": "清华大学出版社", "isbn": "9787302297895", "price": 28, "orig": 85, "condition": "九五新", "category": "计算机", "desc": "经典AI教材，适合进阶学习。", "cover": "人工智能导论.jpg"},
        {"seller": 7, "title": "毛泽东思想概论", "author": "教材编写组", "publisher": "高等教育出版社", "isbn": "9787040361780", "price": 8, "orig": 25, "condition": "七成新", "category": "政治", "desc": "公共课教材，有笔记。", "cover": "毛泽东思想概论.jpg"},
        {"seller": 7, "title": "离散数学", "author": "屈婉玲", "publisher": "高等教育出版社", "isbn": "9787040292107", "price": 14, "orig": 42, "condition": "八成新", "category": "数学", "desc": "计算机专业必修。", "cover": "离散数学.jpg"},
        {"seller": 8, "title": "编译原理", "author": "Alfred V. Aho", "publisher": "机械工业出版社", "isbn": "9787111251217", "price": 22, "orig": 68, "condition": "九成新", "category": "计算机", "desc": "龙书，经典中的经典。", "cover": "编译原理.png"},
    ]

    books = []
    for b in books_data:
        book = Book(
            seller_id=users[b["seller"]].id,
            title=b["title"], author=b["author"], publisher=b["publisher"],
            isbn=b["isbn"], price=b["price"], original_price=b["orig"],
            condition=b["condition"], category=b["category"], description=b["desc"],
            cover_image=b.get("cover", ""),
            status="available", view_count=50 + hash(b["title"]) % 200
        )
        db.add(book)
        books.append(book)
    db.commit()
    for b in books:
        db.refresh(b)
    print(f"[种子] 创建 {len(books)} 本书籍")

    # ==================== 求购 ====================
    wantbuys_data = [
        {"user": 1, "title": "机器学习", "author": "周志华", "isbn": "9787302423287", "price": 25, "desc": "希望是西瓜书，版次不限"},
        {"user": 3, "title": "深入理解计算机系统", "author": "Randal E. Bryant", "isbn": "", "price": 35, "desc": "英文原版或中文翻译版均可"},
        {"user": 5, "title": "算法导论", "author": "Thomas H. Cormen", "isbn": "9787111407010", "price": 30, "desc": "第三版优先"},
        {"user": 6, "title": "经济学原理", "author": "曼昆", "isbn": "", "price": 20, "desc": "微观经济学分册"},
        {"user": 8, "title": "信号与系统", "author": "奥本海姆", "isbn": "", "price": 28, "desc": "第二版，中文版"},
    ]

    for w in wantbuys_data:
        wb = WantBuy(
            user_id=users[w["user"]].id,
            title=w["title"], author=w["author"], isbn=w["isbn"],
            expected_price=w["price"], description=w["desc"],
            status="open"
        )
        db.add(wb)
    db.commit()
    print(f"[种子] 创建 {len(wantbuys_data)} 条求购")

    # ==================== 订单 ====================
    orders_data = [
        {"book": 0, "buyer": 3, "seller": 1, "price": 15, "status": "completed"},
        {"book": 1, "buyer": 5, "seller": 1, "price": 12, "status": "completed"},
        {"book": 4, "buyer": 2, "seller": 3, "price": 10, "status": "completed"},
        {"book": 8, "buyer": 6, "seller": 5, "price": 20, "status": "pending"},
    ]

    for o in orders_data:
        order = Order(
            book_id=books[o["book"]].id,
            buyer_id=users[o["buyer"]].id,
            seller_id=users[o["seller"]].id,
            price=o["price"],
            status=o["status"]
        )
        db.add(order)
    db.commit()
    print(f"[种子] 创建 {len(orders_data)} 个订单")

    # ==================== 消息 ====================
    msgs = [
        (2, 3, "你好，高数那本还在吗？"), (3, 2, "在的，你要买吗？"),
        (2, 3, "嗯嗯，15书币对吧？"), (3, 2, "对的，成色还不错"),
        (4, 1, "请问数据结构有配套代码吗？"), (1, 4, "有的，在最后一章"),
        (6, 5, "Python那本书有电子版吗？"), (5, 6, "没有哦，只有纸质版"),
        (8, 2, "编译原理适合自学吗？"), (2, 8, "建议配合视频课程看"),
    ]
    for sender, receiver, content in msgs:
        msg = Message(
            sender_id=users[sender].id,
            receiver_id=users[receiver].id,
            content=content
        )
        db.add(msg)
    db.commit()
    print(f"[种子] 创建 {len(msgs)} 条消息")

    # ==================== 书币交易记录 ====================
    txs = [
        (2, 100, "buy", "新用户注册奖励"),
        (2, 15, "sell", "出售《高等数学》"),
        (2, -20, "buy", "购买《Python编程导论》"),
        (3, 100, "buy", "新用户注册奖励"),
        (3, 12, "sell", "出售《线性代数》"),
        (5, 100, "buy", "新用户注册奖励"),
        (5, -25, "buy", "购买《数据结构》"),
    ]
    for uid, amount, tx_type, desc in txs:
        user = users[uid]
        tx = CoinTransaction(
            user_id=user.id,
            amount=amount,
            balance_after=user.coin_balance,
            tx_type=tx_type,
            description=desc
        )
        db.add(tx)
    db.commit()
    print(f"[种子] 创建 {len(txs)} 条交易记录")

    db.close()
    print("\n种子数据创建完成！")
    print("所有用户密码: 123456")
    print("管理员账号: admin / 123456")

if __name__ == "__main__":
    seed()
