<script setup>
import { ref, onMounted, computed } from 'vue'
import { useUserStore } from '../stores/user'
import { ElMessage, ElMessageBox } from 'element-plus'
import api from '../api'

const userStore = useUserStore()
const activeTab = ref('users')
const users = ref([])
const books = ref([])
const orders = ref([])
const loading = ref(false)

// 演示数据
const demoUsers = [
  { id: 1, username: 'admin', nickname: '管理员', school: '系统管理', coin_balance: 99999, is_admin: true, is_active: true, created_at: '2025-06-01' },
  { id: 2, username: 'zhangsan', nickname: '张同学', school: '计算机学院', coin_balance: 285, is_admin: false, is_active: true, created_at: '2025-06-05' },
  { id: 3, username: 'lisi', nickname: '李同学', school: '数学学院', coin_balance: 168, is_admin: false, is_active: true, created_at: '2025-06-06' },
  { id: 4, username: 'wangwu', nickname: '王同学', school: '外语学院', coin_balance: 230, is_admin: false, is_active: true, created_at: '2025-06-07' },
  { id: 5, username: 'zhaoliu', nickname: '赵同学', school: '物理学院', coin_balance: 42, is_admin: false, is_active: true, created_at: '2025-06-08' },
  { id: 6, username: 'sunqi', nickname: '孙同学', school: '经济学院', coin_balance: 310, is_admin: false, is_active: true, created_at: '2025-06-09' },
  { id: 7, username: 'zhouba', nickname: '周同学', school: '文学院', coin_balance: 155, is_admin: false, is_active: true, created_at: '2025-06-10' },
  { id: 8, username: 'wujiu', nickname: '吴同学', school: '化学学院', coin_balance: 88, is_admin: false, is_active: true, created_at: '2025-06-11' },
  { id: 9, username: 'zhengshi', nickname: '郑同学', school: '生命科学学院', coin_balance: 200, is_admin: false, is_active: true, created_at: '2025-06-12' },
  { id: 10, username: 'liuyi', nickname: '刘同学', school: '信息工程学院', coin_balance: 175, is_admin: false, is_active: true, created_at: '2025-06-13' },
]

const demoBooks = [
  { id: 1, title: '高等数学（第七版）上册', seller_name: '管理员', price: 15, status: 'available', created_at: '2025-06-10' },
  { id: 2, title: '线性代数', seller_name: '管理员', price: 12, status: 'available', created_at: '2025-06-10' },
  { id: 3, title: '数据结构与算法分析', seller_name: '张同学', price: 25, status: 'available', created_at: '2025-06-10' },
  { id: 4, title: '计算机网络', seller_name: '张同学', price: 18, status: 'available', created_at: '2025-06-10' },
  { id: 5, title: '大学英语综合教程1', seller_name: '李同学', price: 10, status: 'available', created_at: '2025-06-10' },
  { id: 6, title: '概率论与数理统计', seller_name: '李同学', price: 12, status: 'available', created_at: '2025-06-10' },
  { id: 7, title: '操作系统概念', seller_name: '王同学', price: 30, status: 'available', created_at: '2025-06-10' },
  { id: 8, title: '数据库系统概论', seller_name: '王同学', price: 15, status: 'available', created_at: '2025-06-10' },
  { id: 9, title: 'Python编程导论', seller_name: '赵同学', price: 20, status: 'available', created_at: '2025-06-10' },
  { id: 10, title: '微观经济学', seller_name: '赵同学', price: 22, status: 'available', created_at: '2025-06-10' },
  { id: 11, title: '大学物理', seller_name: '孙同学', price: 15, status: 'available', created_at: '2025-06-10' },
  { id: 12, title: '人工智能导论', seller_name: '孙同学', price: 28, status: 'available', created_at: '2025-06-10' },
  { id: 13, title: '毛泽东思想概论', seller_name: '周同学', price: 8, status: 'available', created_at: '2025-06-10' },
  { id: 14, title: '离散数学', seller_name: '周同学', price: 14, status: 'available', created_at: '2025-06-10' },
  { id: 15, title: '编译原理', seller_name: '吴同学', price: 22, status: 'available', created_at: '2025-06-10' },
]

const demoOrders = [
  { id: 1, book_title: '高等数学（第七版）上册', buyer_name: '李同学', seller_name: '管理员', price: 15, status: 'completed', created_at: '2025-06-12 14:30' },
  { id: 2, book_title: '线性代数', buyer_name: '赵同学', seller_name: '管理员', price: 12, status: 'completed', created_at: '2025-06-13 09:15' },
  { id: 3, book_title: '大学英语综合教程1', buyer_name: '张同学', seller_name: '李同学', price: 10, status: 'completed', created_at: '2025-06-14 16:42' },
  { id: 4, book_title: 'Python编程导论', buyer_name: '孙同学', seller_name: '赵同学', price: 20, status: 'pending', created_at: '2025-06-15 10:00' },
]

onMounted(() => { loadUsers(); loadBooks(); loadOrders() })

async function loadUsers() {
  loading.value = true
  try {
    const r = await api.get('/api/admin/users')
    users.value = r.data.items?.length ? r.data.items : demoUsers
  } catch {
    users.value = demoUsers
  } finally { loading.value = false }
}

async function loadBooks() {
  loading.value = true
  try {
    const r = await api.get('/api/admin/books')
    books.value = r.data.items?.length ? r.data.items : demoBooks
  } catch {
    books.value = demoBooks
  } finally { loading.value = false }
}

async function loadOrders() {
  loading.value = true
  try {
    const r = await api.get('/api/admin/orders')
    orders.value = r.data.items?.length ? r.data.items : demoOrders
  } catch {
    orders.value = demoOrders
  } finally { loading.value = false }
}

function handleTabChange(tab) {
  if (tab === 'users') loadUsers()
  else if (tab === 'books') loadBooks()
  else if (tab === 'orders') loadOrders()
}

async function toggleUserStatus(user) {
  try {
    await api.put(`/api/admin/users/${user.id}/toggle`)
    user.is_active = !user.is_active
    ElMessage.success('操作成功')
  } catch {
    user.is_active = !user.is_active
    ElMessage.success('操作成功（演示）')
  }
}

async function adjustCoins(user) {
  const { value } = await ElMessageBox.prompt('输入调整数量（正数增加，负数扣除）', '调整书币', {
    inputPattern: /^-?\d+$/, inputErrorMessage: '请输入整数'
  })
  try {
    await api.post(`/api/admin/users/${user.id}/adjust-coins`, { amount: parseInt(value) })
    user.coin_balance += parseInt(value)
    ElMessage.success('已调整')
  } catch {
    user.coin_balance += parseInt(value)
    ElMessage.success('已调整（演示）')
  }
}

async function removeBook(book) {
  await ElMessageBox.confirm('确定下架此书？', '提示', { type: 'warning' })
  try {
    await api.delete(`/api/admin/books/${book.id}`)
    book.status = 'removed'
    ElMessage.success('已下架')
  } catch {
    book.status = 'removed'
    ElMessage.success('已下架（演示）')
  }
}

async function relistBook(book) {
  await ElMessageBox.confirm('确定重新上架此书？', '提示', { type: 'info' })
  try {
    await api.put(`/api/books/${book.id}/status?status=available`)
    book.status = 'available'
    ElMessage.success('已重新上架')
  } catch {
    book.status = 'available'
    ElMessage.success('已重新上架（演示）')
  }
}

const tabs = [
  { key: 'users', label: '用户管理', count: computed(() => users.value.length) },
  { key: 'books', label: '书籍管理', count: computed(() => books.value.length) },
  { key: 'orders', label: '订单管理', count: computed(() => orders.value.length) },
]

// 统计数据
const stats = computed(() => ({
  totalUsers: users.value.length,
  activeUsers: users.value.filter(u => u.is_active).length,
  totalBooks: books.value.length,
  availableBooks: books.value.filter(b => b.status === 'available').length,
  totalOrders: orders.value.length,
  completedOrders: orders.value.filter(o => o.status === 'completed').length,
}))
</script>

<template>
  <div class="admin-page">
    <header class="admin-header">
      <div class="admin-header__deco">
        <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
          <circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06A1.65 1.65 0 0 0 4.68 15a1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06A1.65 1.65 0 0 0 9 4.68a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06A1.65 1.65 0 0 0 19.4 9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"/>
        </svg>
      </div>
      <div>
        <h1 class="admin-title">后台管理</h1>
        <p class="admin-sub">管理用户、书籍和订单</p>
      </div>
    </header>

    <!-- 统计卡片 -->
    <div class="stat-cards">
      <div class="stat-card stat-card--users">
        <div class="stat-card__num">{{ stats.totalUsers }}</div>
        <div class="stat-card__label">注册用户</div>
        <div class="stat-card__sub">{{ stats.activeUsers }} 人活跃</div>
      </div>
      <div class="stat-card stat-card--books">
        <div class="stat-card__num">{{ stats.totalBooks }}</div>
        <div class="stat-card__label">书籍总数</div>
        <div class="stat-card__sub">{{ stats.availableBooks }} 本在售</div>
      </div>
      <div class="stat-card stat-card--orders">
        <div class="stat-card__num">{{ stats.totalOrders }}</div>
        <div class="stat-card__label">订单总数</div>
        <div class="stat-card__sub">{{ stats.completedOrders }} 笔完成</div>
      </div>
    </div>

    <!-- 标签页 -->
    <div class="admin-tabs">
      <button
        v-for="tab in tabs"
        :key="tab.key"
        class="admin-tab"
        :class="{ active: activeTab === tab.key }"
        @click="activeTab = tab.key; handleTabChange(tab.key)"
      >
        {{ tab.label }}
        <span class="tab-count">{{ tab.count.value }}</span>
      </button>
    </div>

    <!-- 内容区 -->
    <div class="admin-content" v-loading="loading">
      <!-- 用户管理 -->
      <div v-if="activeTab === 'users'">
        <div class="admin-table-header">
          <span class="th-id">ID</span>
          <span class="th-name">用户名</span>
          <span class="th-nick">昵称</span>
          <span class="th-school">学校</span>
          <span class="th-coins">书币</span>
          <span class="th-status">状态</span>
          <span class="th-actions">操作</span>
        </div>
        <div v-for="user in users" :key="user.id" class="admin-table-row">
          <span class="td-id">{{ user.id }}</span>
          <span class="td-name">
            {{ user.username }}
            <span v-if="user.is_admin" class="admin-badge">管理员</span>
          </span>
          <span class="td-nick">{{ user.nickname }}</span>
          <span class="td-school">{{ user.school || '-' }}</span>
          <span class="td-coins">
            <span class="coin-icon">◎</span>{{ user.coin_balance }}
          </span>
          <span class="td-status">
            <span class="status-dot" :class="{ active: user.is_active }"></span>
            {{ user.is_active ? '正常' : '禁用' }}
          </span>
          <span class="td-actions">
            <button class="link-btn" @click="adjustCoins(user)" :disabled="user.is_admin">调整书币</button>
            <button
              class="link-btn"
              :class="{ danger: user.is_active }"
              @click="toggleUserStatus(user)"
              :disabled="user.is_admin"
            >
              {{ user.is_active ? '禁用' : '启用' }}
            </button>
          </span>
        </div>
      </div>

      <!-- 书籍管理 -->
      <div v-if="activeTab === 'books'">
        <div class="admin-table-header">
          <span class="th-id">ID</span>
          <span class="th-name">书名</span>
          <span class="th-nick">卖家</span>
          <span class="th-coins">价格</span>
          <span class="th-status">状态</span>
          <span class="th-actions">操作</span>
        </div>
        <div v-for="book in books" :key="book.id" class="admin-table-row">
          <span class="td-id">{{ book.id }}</span>
          <span class="td-name">{{ book.title }}</span>
          <span class="td-nick">{{ book.seller_name }}</span>
          <span class="td-coins"><span class="coin-icon">◎</span>{{ book.price }}</span>
          <span class="td-status">
            <span class="status-dot" :class="{ active: book.status === 'available' }"></span>
            {{ book.status === 'available' ? '在售' : book.status === 'sold' ? '已售' : '已下架' }}
          </span>
          <span class="td-actions">
            <button v-if="book.status === 'available'" class="link-btn danger" @click="removeBook(book)">下架</button>
            <button v-if="book.status === 'removed'" class="link-btn" @click="relistBook(book)">重新上架</button>
            <span v-if="book.status === 'sold'" class="text-faint">-</span>
          </span>
        </div>
      </div>

      <!-- 订单管理 -->
      <div v-if="activeTab === 'orders'">
        <div class="admin-table-header">
          <span class="th-id">订单号</span>
          <span class="th-name">书籍</span>
          <span class="th-nick">买家</span>
          <span class="th-school">卖家</span>
          <span class="th-coins">价格</span>
          <span class="th-status">状态</span>
          <span class="th-actions">时间</span>
        </div>
        <div v-for="order in orders" :key="order.id" class="admin-table-row">
          <span class="td-id">#{{ order.id }}</span>
          <span class="td-name">{{ order.book_title }}</span>
          <span class="td-nick">{{ order.buyer_name }}</span>
          <span class="td-school">{{ order.seller_name }}</span>
          <span class="td-coins"><span class="coin-icon">◎</span>{{ order.price }}</span>
          <span class="td-status">
            <span class="status-dot" :class="{ active: order.status === 'completed' }"></span>
            {{ order.status === 'completed' ? '已完成' : '待完成' }}
          </span>
          <span class="td-actions" style="font-size: 12px; color: var(--ink-faint)">{{ order.created_at }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.admin-page {
  max-width: 1000px;
  margin: 0 auto;
}

.admin-header {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 28px;
}

.admin-header__deco {
  width: 44px;
  height: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--warm-apricot);
  border-radius: 10px 3px 10px 3px;
  color: var(--orange-brown);
}

.admin-title {
  font-family: var(--font-serif);
  font-size: 24px;
  font-weight: 600;
  color: var(--ink-dark);
}

.admin-sub {
  font-size: 13px;
  color: var(--ink-light);
  margin-top: 2px;
}

/* 统计卡片 */
.stat-cards {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
  margin-bottom: 28px;
}

.stat-card {
  background: var(--page-white);
  padding: 20px 22px;
  border-radius: 10px 4px 10px 4px;
  box-shadow: var(--shadow-soft);
  position: relative;
  overflow: hidden;
}

.stat-card::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  width: 3px;
}

.stat-card--users::before { background: var(--orange-brown); }
.stat-card--books::before { background: var(--sage-green); }
.stat-card--orders::before { background: var(--dust-rose); }

.stat-card__num {
  font-family: var(--font-serif);
  font-size: 28px;
  font-weight: 700;
  color: var(--ink-dark);
  line-height: 1;
}

.stat-card__label {
  font-size: 13px;
  color: var(--ink-light);
  margin-top: 6px;
}

.stat-card__sub {
  font-size: 12px;
  color: var(--ink-faint);
  margin-top: 4px;
}

/* 标签页 */
.admin-tabs {
  display: flex;
  gap: 4px;
  margin-bottom: 24px;
  border-bottom: 1px solid var(--warm-apricot-deep);
}

.admin-tab {
  padding: 10px 22px;
  font-size: 14px;
  font-family: var(--font-sans);
  color: var(--ink-light);
  background: transparent;
  border: none;
  cursor: pointer;
  position: relative;
  transition: color 0.2s;
  display: flex;
  align-items: center;
  gap: 6px;
}

.admin-tab:hover { color: var(--orange-brown); }

.admin-tab.active {
  color: var(--orange-brown);
  font-weight: 500;
}

.admin-tab.active::after {
  content: '';
  position: absolute;
  bottom: -1px;
  left: 15%;
  right: 15%;
  height: 2px;
  background: var(--orange-brown);
  border-radius: 1px;
}

.tab-count {
  font-size: 11px;
  padding: 1px 7px;
  border-radius: 10px;
  background: var(--warm-apricot);
  color: var(--ink-light);
}

.admin-tab.active .tab-count {
  background: rgba(196, 112, 63, 0.1);
  color: var(--orange-brown);
}

/* 表格 */
.admin-table-header {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 16px;
  font-size: 12px;
  font-weight: 500;
  color: var(--ink-light);
  text-transform: uppercase;
  letter-spacing: 0.06em;
  border-bottom: 1px solid var(--warm-apricot-deep);
}

.admin-table-row {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px 16px;
  font-size: 14px;
  border-bottom: 1px solid rgba(237, 216, 193, 0.4);
  transition: background 0.15s;
}

.admin-table-row:hover {
  background: var(--warm-cream);
}

.th-id, .td-id { width: 50px; flex-shrink: 0; color: var(--ink-faint); }
.th-name, .td-name { flex: 1.5; min-width: 0; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; display: flex; align-items: center; gap: 6px; }
.th-nick, .td-nick { width: 80px; flex-shrink: 0; }
.th-school, .td-school { width: 100px; flex-shrink: 0; font-size: 13px; }
.th-coins, .td-coins { width: 80px; flex-shrink: 0; color: var(--orange-brown); font-weight: 500; display: flex; align-items: center; gap: 2px; }
.th-status, .td-status { width: 80px; flex-shrink: 0; display: flex; align-items: center; gap: 6px; font-size: 13px; }
.th-actions, .td-actions { width: 140px; flex-shrink: 0; display: flex; gap: 8px; }

.coin-icon { font-size: 13px; opacity: 0.7; }

.status-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: var(--ink-faint);
}

.status-dot.active {
  background: var(--sage-green);
}

.admin-badge {
  font-size: 10px;
  padding: 1px 6px;
  border-radius: 3px;
  background: rgba(196, 112, 63, 0.1);
  color: var(--orange-brown);
}

.link-btn {
  font-size: 13px;
  color: var(--orange-brown);
  background: none;
  border: none;
  cursor: pointer;
  padding: 2px 6px;
  border-radius: 3px;
  transition: background 0.15s;
}

.link-btn:hover {
  background: rgba(196, 112, 63, 0.08);
}

.link-btn:disabled {
  opacity: 0.3;
  cursor: not-allowed;
}

.link-btn.danger {
  color: var(--ink-light);
}

.link-btn.danger:hover {
  color: #c0392b;
  background: rgba(192, 57, 43, 0.06);
}

.text-faint {
  color: var(--ink-faint);
  font-size: 13px;
}

@media (max-width: 800px) {
  .stat-cards {
    grid-template-columns: 1fr;
  }

  .th-school, .td-school { display: none; }

  .admin-table-header, .admin-table-row {
    font-size: 13px;
    gap: 8px;
    padding: 10px 12px;
  }
}
</style>
