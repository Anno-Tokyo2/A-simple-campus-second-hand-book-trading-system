<div align="center">

# 旧书集 / Campus Book Exchange

**校园二手书交易平台**

*A campus second-hand book trading platform powered by virtual "Book Coin" economy*

![Vue 3](https://img.shields.io/badge/Vue-3-4FC08D?logo=vue.js&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?logo=fastapi&logoColor=white)
![Vite](https://img.shields.io/badge/Vite-6-646CFF?logo=vite&logoColor=white)
![Tailwind CSS](https://img.shields.io/badge/Tailwind-4-06B6D4?logo=tailwindcss&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-3-003B57?logo=sqlite&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)

</div>

---

## 中文简介

旧书集是一个面向高校学生的校园二手书交易平台。平台采用虚拟"书币"经济系统，注册即送 100 书币，用户可以自由买卖闲置书籍。支持 ISBN 一键上架、求购发布、站内私信、后台管理等完整功能，并内置滑块拼图验证码和程序化书籍封面生成等特色功能。

### 核心功能

| 功能 | 说明 |
|------|------|
| 用户注册/登录 | 滑块拼图验证码，JWT 鉴权，bcrypt 密码加密 |
| 书籍发布与搜索 | 分类筛选、关键词搜索、多种排序，支持封面图片上传 |
| ISBN 一键上架 | 输入 ISBN 自动填充书名、作者、出版社 |
| 书币经济系统 | 虚拟货币交易，注册赠送 100 书币，完整交易流水记录 |
| 担保交易流程 | 买家下单 → 书币冻结 → 确认收货 → 书币转入卖家 |
| 求购系统 | 发布求购需求，其他用户可回应并自动发送站内消息 |
| 站内私信 | 用户间实时聊天，未读消息提醒，消息关联书籍 |
| 后台管理 | 用户管理、书籍管理、订单管理、书币调节 |
| 程序化封面 | 无封面图片时，按学科自动生成风格化 SVG 封面 |
| 响应式设计 | 适配桌面端与移动端，含汉堡菜单导航 |

---

## English Introduction

Campus Book Exchange is a full-stack web application designed for university students to buy and sell second-hand books. Instead of real money, it uses a virtual **"Book Coin"** economy — every new user receives 100 coins upon registration, which they can use to purchase books from other students. The platform features ISBN auto-fill, a want-to-buy system, in-app messaging, and a full admin dashboard.

### Key Features

| Feature | Description |
|---------|-------------|
| **Auth & Security** | Slide puzzle CAPTCHA, JWT authentication, bcrypt password hashing |
| **Book Marketplace** | Category filters, keyword search, multi-sort, cover image upload |
| **ISBN Quick-Fill** | Enter ISBN to auto-populate title, author, and publisher |
| **Book Coin Economy** | Virtual currency with full transaction history tracking |
| **Escrow Trading** | Purchase → coins held → confirm receipt → coins released to seller |
| **Want-to-Buy** | Post requests for books you need; others can respond via site message |
| **In-App Messaging** | Real-time-style chat between users with unread badges |
| **Admin Panel** | User/book/order management, coin balance adjustment |
| **Procedural Covers** | Auto-generated SVG covers by subject when no image is uploaded |
| **Responsive Design** | Desktop & mobile friendly with hamburger nav on small screens |

---

## Tech Stack / 技术栈

```
Frontend                          Backend
─────────────                     ─────────────
Vue 3 (Composition API)           Python FastAPI
Vite 6                            SQLAlchemy 2.0
Tailwind CSS 4                    SQLite
Element Plus                      python-jose (JWT)
Pinia 3 (State Management)        passlib + bcrypt
Vue Router 4                      httpx
Axios
```

---

## Quick Start / 快速启动

### Prerequisites / 环境要求

- **Python** 3.10+
- **Node.js** 18+
- **npm** 9+

### Option 1: One-Click Start (Windows) / 一键启动

```bash
双击 start.bat
```

This will start both the backend (port 8000) and frontend (port 5173), then open the browser.

### Option 2: Manual Start / 手动启动

**Backend / 后端:**

```bash
cd backend
pip install -r requirements.txt
python main.py
```

**Frontend / 前端:**

```bash
cd frontend
npm install
npm run dev
```

Then open http://localhost:5173 in your browser.

### Seed Data / 初始化数据

To populate the database with demo data (10 users, 15 books, sample orders & messages):

```bash
cd backend
python seed.py
```

---

## Project Structure / 项目结构

```
PBL/
├── backend/                    # FastAPI Backend
│   ├── app/
│   │   ├── routers/            # API route handlers
│   │   │   ├── users.py        #   注册/登录/个人信息
│   │   │   ├── books.py        #   书籍 CRUD
│   │   │   ├── orders.py       #   订单与交易
│   │   │   ├── messages.py     #   站内私信
│   │   │   ├── wantbuys.py     #   求购系统
│   │   │   └── admin.py        #   后台管理
│   │   ├── models/             # SQLAlchemy 数据模型
│   │   ├── schemas/            # Pydantic 请求/响应模型
│   │   ├── services/           # 业务逻辑层
│   │   └── utils/              # 工具函数 (JWT, 密码等)
│   ├── main.py                 # 应用入口
│   ├── seed.py                 # 演示数据初始化
│   └── requirements.txt
├── frontend/                   # Vue 3 Frontend
│   ├── src/
│   │   ├── views/              # 页面组件 (10 个路由)
│   │   ├── components/         # 公共组件
│   │   │   ├── Navbar.vue      #   导航栏
│   │   │   ├── BookCard.vue    #   书籍卡片
│   │   │   ├── BookCover.vue   #   程序化封面生成
│   │   │   └── SlideVerify.vue #   滑块验证码
│   │   ├── stores/             # Pinia 状态管理
│   │   ├── api/                # Axios 接口封装
│   │   └── router/             # Vue Router 配置
│   ├── package.json
│   └── vite.config.js
├── data/                       # SQLite 数据库文件
├── uploads/                    # 上传的书籍封面图片
├── photo/                      # 示例书籍封面
├── start.bat                   # Windows 一键启动脚本
└── README.md
```

---

## Test Accounts / 测试帐号

| Role / 角色 | Username / 帐号 | Password / 密码 | Book Coins / 书币 |
|:-----------:|:----------------:|:---------------:|:-----------------:|
| Admin / 管理员 | `admin` | `admin123` | 99999 |
| Student / 学生 | `zhangsan` | `123456` | 285 |
| Student / 学生 | `lisi` | `123456` | 168 |
| Student / 学生 | `wangwu` | `123456` | 230 |
| Student / 学生 | `sunqi` | `123456` | 310 |
| Student / 学生 | `zhouba` | `123456` | 155 |

> More test accounts are available in `测试帐号.txt`.

---

## API Overview / 接口概览

| Module | Endpoint | Description |
|--------|----------|-------------|
| Users | `POST /api/users/register` | Register (100 coins bonus) |
| Users | `POST /api/users/login` | Login (returns JWT) |
| Books | `GET /api/books` | List books with filters |
| Books | `POST /api/books` | Publish a book |
| Books | `GET /api/books/{id}` | Book detail |
| Orders | `POST /api/orders` | Purchase a book |
| Orders | `POST /api/orders/{id}/confirm` | Confirm receipt |
| Messages | `POST /api/messages` | Send a message |
| Messages | `GET /api/messages/conversations` | List conversations |
| WantBuy | `POST /api/wantbuys` | Post a want-to-buy |
| WantBuy | `POST /api/wantbuys/{id}/respond` | Respond to a want-to-buy |
| Admin | `GET /api/admin/users` | List all users (admin) |
| Admin | `POST /api/admin/users/{id}/adjust-coins` | Adjust coins (admin) |

> Full API documentation is available at http://localhost:8000/docs (Swagger UI) when the backend is running.

---

## Screenshots / 界面截图

> *Coming soon — contributions welcome!*
>
> *即将添加 — 欢迎贡献截图！*

---

## Contributing / 参与贡献

Contributions are welcome! Feel free to open issues and pull requests.

欢迎提交 Issue 和 Pull Request！

1. Fork this repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## License / 开源许可

This project is licensed under the MIT License.

本项目基于 MIT 许可证开源。

---

<div align="center">

**Built with love for campus book lovers**

**为爱书的校园人而造**

</div>
