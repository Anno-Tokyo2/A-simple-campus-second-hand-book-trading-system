# 旧书集 - 前端 / Campus Book Exchange - Frontend

基于 Vue 3 + Vite 构建的校园二手书交易平台前端。

A Vue 3 + Vite frontend for the Campus Book Exchange platform.

## 技术栈 / Tech Stack

- **Vue 3** — Composition API + `<script setup>`
- **Vite 6** — 开发服务器与构建工具
- **Tailwind CSS 4** — 原子化 CSS 框架
- **Element Plus** — UI 组件库（中文 locale）
- **Pinia** — 状态管理
- **Vue Router 4** — 路由管理
- **Axios** — HTTP 请求

## 项目结构 / Structure

```
src/
├── views/              # 页面组件
│   ├── Home.vue        #   首页
│   ├── Login.vue       #   登录（含滑块验证码）
│   ├── Register.vue    #   注册（含滑块验证码）
│   ├── BookList.vue    #   书市（分类/搜索/排序）
│   ├── BookDetail.vue  #   书籍详情（购买/联系卖家）
│   ├── PublishBook.vue #   发布书籍（ISBN 一键上架）
│   ├── UserCenter.vue  #   个人中心（发布/订单/书币明细）
│   ├── Messages.vue    #   站内私信（会话列表+聊天）
│   ├── WantBuy.vue     #   求购广场（发布/回应求购）
│   └── Admin.vue       #   后台管理（用户/书籍/订单）
├── components/         # 公共组件
│   ├── Navbar.vue      #   顶部导航栏
│   ├── BookCard.vue    #   书籍卡片（三种变体）
│   ├── BookCover.vue   #   程序化 SVG 封面生成
│   └── SlideVerify.vue #   滑块拼图验证码
├── stores/
│   └── user.js         #   Pinia 用户状态（token/登录/登出）
├── api/
│   └── index.js        #   Axios 实例（JWT 拦截器）
├── router/
│   └── index.js        #   路由配置（含 auth/admin 守卫）
├── style.css           #   全局样式（暖杏色主题）
├── App.vue             #   根组件（页面过渡动画）
└── main.js             #   入口文件
```

## 开发 / Development

```bash
# 安装依赖
npm install

# 启动开发服务器 (http://localhost:5173)
npm run dev

# 构建生产版本
npm run build

# 预览构建结果
npm run preview
```

> 后端服务需同时运行在 http://localhost:8000，Vite 会自动代理 `/api` 和 `/static` 请求。
