<script setup>
import { ref, onMounted } from 'vue'
import { useUserStore } from '../stores/user'
import { ElMessage, ElMessageBox } from 'element-plus'
import api from '../api'

const userStore = useUserStore()
const activeTab = ref('books')
const myBooks = ref([])
const myOrders = ref([])
const coinHistory = ref([])
const loading = ref(false)
const editDialog = ref(false)
const editForm = ref({ id: 0, title: '', author: '', publisher: '', isbn: '', price: 0, original_price: 0, condition: '九成新', category: '', description: '' })
const editFileList = ref([])
const conditions = ['九五新', '九成新', '八成新', '七成新', '六成新及以下']
const categories = ['数学', '计算机', '英语', '经济', '物理', '政治', '文学', '其他']

// 演示数据
const demoMyBooks = [
  { id: 1, title: '高等数学（第七版）上册', price: 15, status: 'available' },
  { id: 2, title: '线性代数', price: 12, status: 'sold' },
  { id: 3, title: '大学英语综合教程', price: 10, status: 'available' },
]

const demoMyOrders = [
  { id: 1, book_title: '数据结构与算法分析', price: 25, status: 'completed', created_at: '2025-06-12 14:30' },
  { id: 2, book_title: '计算机网络', price: 18, status: 'pending', created_at: '2025-06-14 09:15' },
]

const demoCoinHistory = [
  { id: 1, description: '新用户注册奖励', amount: 100, balance_after: 100, created_at: '2025-06-01 10:00' },
  { id: 2, description: '出售《线性代数》', amount: 12, balance_after: 112, created_at: '2025-06-12 14:30' },
  { id: 3, description: '购买《数据结构与算法分析》', amount: -25, balance_after: 87, created_at: '2025-06-12 15:00' },
  { id: 4, description: '出售《Python编程导论》', amount: 20, balance_after: 107, created_at: '2025-06-15 16:42' },
]

onMounted(() => { loadMyBooks() })

async function loadMyBooks() {
  loading.value = true
  try {
    const r = await api.get('/api/books?seller_id=me')
    myBooks.value = r.data.items?.length ? r.data.items : demoMyBooks
  } catch { myBooks.value = demoMyBooks }
  finally { loading.value = false }
}

async function loadMyOrders() {
  loading.value = true
  try {
    const r = await api.get('/api/orders')
    myOrders.value = r.data.items?.length ? r.data.items : demoMyOrders
  } catch { myOrders.value = demoMyOrders }
  finally { loading.value = false }
}

async function loadCoinHistory() {
  loading.value = true
  try {
    const r = await api.get('/api/users/coin-history')
    coinHistory.value = r.data.items?.length ? r.data.items : demoCoinHistory
  } catch { coinHistory.value = demoCoinHistory }
  finally { loading.value = false }
}

function handleTabChange(tab) {
  if (tab === 'books') loadMyBooks()
  else if (tab === 'orders') loadMyOrders()
  else if (tab === 'coins') loadCoinHistory()
}

async function confirmOrder(orderId) {
  try {
    await ElMessageBox.confirm('确认收货后书币将转给卖家，是否继续？', '确认收货', { type: 'warning' })
    const r = await api.post(`/api/orders/${orderId}/confirm`)
    ElMessage.success(r.data.message || '确认收货成功')
    userStore.userInfo.coin_balance = r.data.seller_balance || userStore.userInfo.coin_balance
    loadMyOrders()
  } catch {}
}

function editBook(book) {
  editForm.value = {
    id: book.id, title: book.title || '', author: book.author || '',
    publisher: book.publisher || '', isbn: book.isbn || '',
    price: book.price || 0, original_price: book.original_price || 0,
    condition: book.condition || '九成新', category: book.category || '',
    description: book.description || ''
  }
  editFileList.value = []
  editDialog.value = true
}

async function saveEdit() {
  if (!editForm.value.title) { ElMessage.warning('请填写书名'); return }
  if (!editForm.value.author) { ElMessage.warning('请填写作者'); return }
  if (!editForm.value.publisher) { ElMessage.warning('请填写出版社'); return }
  if (!editForm.value.price) { ElMessage.warning('请填写售价'); return }
  if (!editForm.value.category) { ElMessage.warning('请选择分类'); return }
  try {
    const fd = new FormData()
    fd.append('title', editForm.value.title)
    fd.append('author', editForm.value.author)
    fd.append('publisher', editForm.value.publisher)
    fd.append('isbn', editForm.value.isbn || '')
    fd.append('price', String(editForm.value.price))
    fd.append('original_price', String(editForm.value.original_price || 0))
    fd.append('condition', editForm.value.condition)
    fd.append('category', editForm.value.category)
    fd.append('description', editForm.value.description || '')
    if (editFileList.value.length > 0 && editFileList.value[0].raw) {
      fd.append('cover', editFileList.value[0].raw)
    }
    await api.put(`/api/books/${editForm.value.id}`, fd)
    ElMessage.success('编辑成功')
    editDialog.value = false
    loadMyBooks()
  } catch (err) {
    ElMessage.error(err.response?.data?.detail || '编辑失败')
  }
}

async function delistBook(book) {
  try {
    await ElMessageBox.confirm(`确定下架《${book.title}》？`, '下架确认', { type: 'warning' })
    await api.put(`/api/books/${book.id}/status?status=removed`)
    ElMessage.success('已下架')
    loadMyBooks()
  } catch (err) {
    if (err !== 'cancel') ElMessage.error(err.response?.data?.detail || '操作失败')
  }
}

async function relistBook(book) {
  try {
    await ElMessageBox.confirm(`确定重新上架《${book.title}》？`, '重新上架', { type: 'info' })
    await api.put(`/api/books/${book.id}/status?status=available`)
    ElMessage.success('已重新上架')
    loadMyBooks()
  } catch (err) {
    if (err !== 'cancel') ElMessage.error(err.response?.data?.detail || '操作失败')
  }
}

const tabs = [
  { key: 'books', label: '我的发布' },
  { key: 'orders', label: '我的订单' },
  { key: 'coins', label: '书币明细' },
]
</script>

<template>
  <div class="user-page">
    <!-- 用户卡片 -->
    <div class="profile-card wood-panel">
      <div class="profile-card__inner">
        <div class="profile-avatar">
          {{ userStore.userInfo?.nickname?.[0] || '书' }}
        </div>
        <div class="profile-info">
          <h1 class="profile-name">{{ userStore.userInfo?.nickname || userStore.userInfo?.username }}</h1>
          <p class="profile-school">{{ userStore.userInfo?.school || '未设置学校' }}</p>
        </div>
        <div class="profile-balance">
          <div class="balance-amount">
            <span class="balance-icon">◎</span>
            <span class="balance-num">{{ userStore.userInfo?.coin_balance || 0 }}</span>
          </div>
          <span class="balance-label">书币余额</span>
        </div>
      </div>
    </div>

    <!-- 标签页 -->
    <div class="custom-tabs">
      <button
        v-for="tab in tabs"
        :key="tab.key"
        class="tab-btn"
        :class="{ active: activeTab === tab.key }"
        @click="activeTab = tab.key; handleTabChange(tab.key)"
      >
        {{ tab.label }}
      </button>
    </div>

    <!-- 内容区 -->
    <div class="tab-content">
      <!-- 我的发布 -->
      <div v-if="activeTab === 'books'" v-loading="loading">
        <div v-if="myBooks.length === 0" class="empty-hint">暂无发布，去发布你的第一本书吧</div>
        <div v-else class="books-table">
          <div v-for="book in myBooks" :key="book.id" class="table-row">
            <span class="row-title">{{ book.title }}</span>
            <span class="row-price"><span class="coin-icon">◎</span>{{ book.price }}</span>
            <span class="row-status" :class="book.status">
              {{ book.status === 'available' ? '在售' : book.status === 'sold' ? '已售' : '已下架' }}
            </span>
            <span class="row-actions">
              <button v-if="book.status === 'available'" class="link-btn" @click="editBook(book)">编辑</button>
              <button v-if="book.status === 'available'" class="link-btn danger" @click="delistBook(book)">下架</button>
              <button v-if="book.status === 'removed'" class="link-btn" @click="relistBook(book)">重新上架</button>
            </span>
          </div>
        </div>
      </div>

      <!-- 我的订单 -->
      <div v-if="activeTab === 'orders'" v-loading="loading">
        <div v-if="myOrders.length === 0" class="empty-hint">暂无订单</div>
        <div v-else class="books-table">
          <div v-for="order in myOrders" :key="order.id" class="table-row">
            <span class="row-id">#{{ order.id }}</span>
            <span class="row-title">{{ order.book_title }}</span>
            <span class="row-price"><span class="coin-icon">◎</span>{{ order.price }}</span>
            <span class="row-role">{{ order.buyer_id === userStore.userInfo?.id ? '买入' : '卖出' }}</span>
            <span class="row-status" :class="order.status">
              {{ order.status === 'completed' ? '已完成' : '待完成' }}
            </span>
            <span class="row-time">{{ order.created_at }}</span>
            <span class="row-actions">
              <button
                v-if="order.status === 'pending' && order.buyer_id === userStore.userInfo?.id"
                class="btn-warm btn-sm"
                @click="confirmOrder(order.id)"
              >
                确认收货
              </button>
            </span>
          </div>
        </div>
      </div>

      <!-- 书币明细 -->
      <div v-if="activeTab === 'coins'" v-loading="loading">
        <div v-if="coinHistory.length === 0" class="empty-hint">暂无记录</div>
        <div v-else class="books-table">
          <div v-for="tx in coinHistory" :key="tx.id" class="table-row">
            <span class="row-time">{{ tx.created_at }}</span>
            <span class="row-title">{{ tx.description }}</span>
            <span class="row-amount" :class="{ positive: tx.amount > 0 }">
              {{ tx.amount > 0 ? '+' : '' }}{{ tx.amount }}
            </span>
            <span class="row-balance"><span class="coin-icon">◎</span>{{ tx.balance_after }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- 编辑弹窗 -->
    <el-dialog v-model="editDialog" title="编辑书籍" width="520px">
      <div class="edit-form">
        <div class="edit-field">
          <label>书名 *</label>
          <input v-model="editForm.title" class="edit-input" />
        </div>
        <div class="edit-row">
          <div class="edit-field">
            <label>作者 *</label>
            <input v-model="editForm.author" class="edit-input" />
          </div>
          <div class="edit-field">
            <label>出版社 *</label>
            <input v-model="editForm.publisher" class="edit-input" />
          </div>
        </div>
        <div class="edit-row">
          <div class="edit-field">
            <label>ISBN</label>
            <input v-model="editForm.isbn" class="edit-input" />
          </div>
          <div class="edit-field">
            <label>分类 *</label>
            <select v-model="editForm.category" class="edit-input">
              <option value="" disabled>请选择</option>
              <option v-for="c in categories" :key="c" :value="c">{{ c }}</option>
            </select>
          </div>
        </div>
        <div class="edit-row">
          <div class="edit-field">
            <label>售价（书币）*</label>
            <input v-model.number="editForm.price" type="number" class="edit-input" />
          </div>
          <div class="edit-field">
            <label>原价（元）</label>
            <input v-model.number="editForm.original_price" type="number" class="edit-input" />
          </div>
          <div class="edit-field">
            <label>成色</label>
            <select v-model="editForm.condition" class="edit-input">
              <option v-for="c in conditions" :key="c" :value="c">{{ c }}</option>
            </select>
          </div>
        </div>
        <div class="edit-field">
          <label>描述</label>
          <textarea v-model="editForm.description" class="edit-textarea" rows="3"></textarea>
        </div>
        <div class="edit-field">
          <label>更换封面图片</label>
          <el-upload
            v-model:file-list="editFileList"
            action="#"
            list-type="picture-card"
            :auto-upload="false"
            :limit="1"
          >
            <div class="upload-add">+</div>
          </el-upload>
        </div>
      </div>
      <template #footer>
        <button class="btn-ghost" @click="editDialog = false">取消</button>
        <button class="btn-warm" @click="saveEdit" style="margin-left: 8px">保存</button>
      </template>
    </el-dialog>
  </div>
</template>

<style scoped>
.user-page {
  max-width: 900px;
  margin: 0 auto;
}

.profile-card {
  border-radius: 14px 4px 14px 4px;
  padding: 4px;
  margin-bottom: 36px;
}

.profile-card__inner {
  background: var(--page-white);
  border-radius: 11px 2px 11px 2px;
  padding: 32px 36px;
  display: flex;
  align-items: center;
  gap: 24px;
}

.profile-avatar {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--orange-brown), var(--dust-rose));
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  font-family: var(--font-serif);
  flex-shrink: 0;
}

.profile-info { flex: 1; }

.profile-name {
  font-family: var(--font-serif);
  font-size: 22px;
  font-weight: 600;
  color: var(--ink-dark);
}

.profile-school {
  font-size: 13px;
  color: var(--ink-light);
  margin-top: 4px;
}

.profile-balance {
  text-align: center;
  flex-shrink: 0;
}

.balance-amount {
  display: flex;
  align-items: baseline;
  gap: 4px;
  justify-content: center;
}

.balance-icon { font-size: 18px; color: var(--orange-brown); opacity: 0.7; }

.balance-num {
  font-family: var(--font-serif);
  font-size: 32px;
  font-weight: 700;
  color: var(--orange-brown);
}

.balance-label {
  font-size: 12px;
  color: var(--ink-faint);
  margin-top: 2px;
}

.custom-tabs {
  display: flex;
  gap: 4px;
  border-bottom: 1px solid var(--warm-apricot-deep);
  margin-bottom: 28px;
}

.tab-btn {
  padding: 10px 24px;
  font-size: 14px;
  font-family: var(--font-sans);
  color: var(--ink-light);
  background: transparent;
  border: none;
  cursor: pointer;
  position: relative;
  transition: color 0.2s;
}

.tab-btn:hover { color: var(--orange-brown); }

.tab-btn.active {
  color: var(--orange-brown);
  font-weight: 500;
}

.tab-btn.active::after {
  content: '';
  position: absolute;
  bottom: -1px;
  left: 20%;
  right: 20%;
  height: 2px;
  background: var(--orange-brown);
  border-radius: 1px;
}

.books-table {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.table-row {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 14px 18px;
  background: var(--page-white);
  border-radius: 4px;
  font-size: 14px;
  transition: background 0.15s;
}

.table-row:first-child { border-radius: 8px 8px 4px 4px; }
.table-row:last-child { border-radius: 4px 4px 8px 8px; }
.table-row:hover { background: var(--warm-cream); }

.row-title {
  flex: 1;
  color: var(--ink-dark);
  min-width: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.row-id { width: 50px; color: var(--ink-faint); font-size: 13px; }

.row-role {
  font-size: 12px;
  color: var(--ink-light);
  min-width: 40px;
  text-align: center;
}

.btn-sm {
  padding: 5px 14px;
  font-size: 12px;
}

.row-price {
  color: var(--orange-brown);
  font-weight: 500;
  min-width: 60px;
  display: flex;
  align-items: center;
  gap: 2px;
}

.coin-icon { font-size: 13px; opacity: 0.7; }

.row-status {
  font-size: 12px;
  padding: 3px 10px;
  border-radius: 12px;
  min-width: 50px;
  text-align: center;
}

.row-status.available, .row-status.completed {
  color: var(--sage-green);
  background: rgba(143, 166, 142, 0.1);
}

.row-status.sold, .row-status.pending, .row-status.removed {
  color: var(--dust-rose);
  background: rgba(184, 132, 92, 0.1);
}

.row-time { font-size: 12px; color: var(--ink-faint); min-width: 100px; }

.row-amount { font-weight: 500; color: var(--dust-rose); min-width: 60px; }
.row-amount.positive { color: var(--sage-green); }

.row-balance { font-size: 12px; color: var(--ink-light); min-width: 80px; display: flex; align-items: center; gap: 2px; }

.row-actions { display: flex; gap: 8px; }

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

.link-btn:hover { background: rgba(196, 112, 63, 0.08); }
.link-btn.danger { color: var(--ink-light); }
.link-btn.danger:hover { color: #c0392b; background: rgba(192, 57, 43, 0.06); }

.empty-hint {
  text-align: center;
  padding: 60px 20px;
  font-size: 14px;
  color: var(--ink-faint);
}

/* 编辑弹窗 */
.edit-form { display: flex; flex-direction: column; gap: 16px; }
.edit-row { display: flex; gap: 12px; }
.edit-row .edit-field { flex: 1; min-width: 0; }
.edit-field { display: flex; flex-direction: column; gap: 6px; }
.edit-field label { font-size: 13px; color: var(--ink-medium); }
.edit-input, .edit-textarea {
  padding: 10px 12px;
  border: 1.5px solid var(--warm-apricot-deep);
  border-radius: 6px;
  font-size: 14px;
  font-family: var(--font-sans);
  outline: none;
  background: var(--warm-cream);
  width: 100%;
  box-sizing: border-box;
  min-width: 0;
}
.edit-input:focus, .edit-textarea:focus { border-color: var(--orange-brown-light); }
.edit-textarea { resize: vertical; }
.upload-add { font-size: 20px; color: var(--ink-faint); }

@media (max-width: 600px) {
  .profile-card__inner {
    flex-direction: column;
    text-align: center;
    padding: 24px 20px;
  }

  .table-row { flex-wrap: wrap; gap: 8px; }
  .row-time { width: 100%; }
}
</style>
