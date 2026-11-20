<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useUserStore } from '../stores/user'
import { ElMessage, ElMessageBox } from 'element-plus'
import api from '../api'
import BookCover from '../components/BookCover.vue'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

const book = ref(null)
const loading = ref(true)
const messageDialog = ref(false)
const messageText = ref('')

const demoBook = {
  id: 1, title: '高等数学（第七版）上册', author: '同济大学数学系',
  publisher: '高等教育出版社', isbn: '9787040396638',
  price: 15, original_price: 46.5, condition: '九成新', category: '数学',
  description: '经典高数教材，少量笔记标注，重点章节有荧光笔标记。',
  cover_image: '高等数学（第七版）上册.jpg',
  seller: { id: 1, nickname: '管理员', school: '系统管理' },
  view_count: 150, created_at: '2025-06-10'
}

onMounted(async () => {
  try {
    const res = await api.get(`/api/books/${route.params.id}`)
    book.value = res.data
  } catch {
    book.value = demoBook
  } finally {
    loading.value = false
  }
})

function getCoverUrl() {
  if (book.value?.cover_image) {
    return book.value.cover_image.startsWith('http') ? book.value.cover_image : `/static/uploads/${book.value.cover_image}`
  }
  return ''
}

const hasRealCover = computed(() => {
  return book.value?.cover_image && book.value.cover_image !== ''
})

const discount = computed(() => {
  if (!book.value?.original_price || !book.value?.price) return null
  return Math.round((book.value.price / book.value.original_price) * 100)
})

async function handleBuy() {
  if (!userStore.isLoggedIn) { ElMessage.warning('请先登录'); router.push('/login'); return }
  await ElMessageBox.confirm(`确定花费 ${book.value.price} 书币购买此书？`, '确认购买', { type: 'info' })
  try {
    await api.post('/api/orders', { book_id: book.value.id })
    ElMessage.success('购买成功！')
    userStore.fetchUserInfo()
  } catch {}
}

function openMessage() {
  if (!userStore.isLoggedIn) { ElMessage.warning('请先登录'); router.push('/login'); return }
  messageDialog.value = true
}

async function sendMessage() {
  if (!messageText.value.trim()) return
  try {
    await api.post('/api/messages', { receiver_id: book.value.seller.id, content: messageText.value, book_id: book.value.id })
    ElMessage.success('消息已发送')
    messageDialog.value = false
    messageText.value = ''
  } catch {}
}
</script>

<template>
  <div class="detail-page" v-loading="loading">
    <!-- 面包屑 -->
    <nav class="breadcrumb">
      <span @click="router.push('/')">首页</span>
      <span class="bc-sep">/</span>
      <span @click="router.push('/books')">书市</span>
      <span class="bc-sep">/</span>
      <span class="bc-current">{{ book?.title }}</span>
    </nav>

    <div v-if="book" class="detail-layout">
      <!-- 左侧：封面（不规则圆角 + 立体效果） -->
      <div class="detail-cover-area">
        <div class="cover-frame">
          <img v-if="hasRealCover" :src="getCoverUrl()" :alt="book.title" />
          <BookCover
            v-else
            :title="book.title"
            :author="book.author"
            :category="book.category"
            :publisher="book.publisher"
          />
          <!-- 书脊效果 -->
          <div class="cover-spine"></div>
        </div>
        <!-- 小缩略图 -->
        <div class="cover-thumbs">
          <div class="thumb active"></div>
          <div class="thumb"></div>
          <div class="thumb"></div>
        </div>
      </div>

      <!-- 右侧：信息（非卡片式，直接在背景上展示） -->
      <div class="detail-info">
        <div class="info-top">
          <span class="info-category">{{ book.category }}</span>
          <span class="info-condition" :class="book.condition">{{ book.condition }}</span>
        </div>

        <h1 class="detail-title">{{ book.title }}</h1>

        <div class="info-meta">
          <span><strong>作者</strong> {{ book.author }}</span>
          <span><strong>出版社</strong> {{ book.publisher }}</span>
          <span><strong>ISBN</strong> {{ book.isbn }}</span>
        </div>

        <!-- 价格区 - 独立的暖色面板 -->
        <div class="price-panel">
          <div class="price-main">
            <span class="price-symbol">◎</span>
            <span class="price-amount">{{ book.price }}</span>
            <span class="price-unit">书币</span>
          </div>
          <div v-if="book.original_price" class="price-original">
            <span class="original-label">原价</span>
            <span class="original-value">¥{{ book.original_price }}</span>
            <span v-if="discount" class="discount-tag">约{{ discount }}折</span>
          </div>
        </div>

        <!-- 操作按钮 -->
        <div class="action-row">
          <button class="btn-warm action-buy" @click="handleBuy">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="9" cy="21" r="1"/><circle cx="20" cy="21" r="1"/>
              <path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"/>
            </svg>
            立即购买
          </button>
          <button class="btn-ghost action-msg" @click="openMessage">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
            </svg>
            联系卖家
          </button>
        </div>

        <!-- 卖家信息 -->
        <div class="seller-bar">
          <div class="seller-avatar">{{ book.seller?.nickname?.[0] || '书' }}</div>
          <div class="seller-info">
            <span class="seller-name">{{ book.seller?.nickname }}</span>
            <span class="seller-school">{{ book.seller?.school }}</span>
          </div>
          <div class="seller-meta">
            <span>{{ book.view_count }} 次浏览</span>
            <span>{{ book.created_at }}</span>
          </div>
        </div>

        <!-- 书籍描述 -->
        <div class="description-area">
          <h3 class="desc-heading">
            <span class="desc-line"></span>
            书籍描述
          </h3>
          <p class="desc-text">{{ book.description }}</p>
        </div>
      </div>
    </div>

    <!-- 联系卖家弹窗 -->
    <el-dialog v-model="messageDialog" title="发送消息" width="460px">
      <p class="dialog-hint">向 {{ book?.seller?.nickname }} 发送消息</p>
      <input v-model="messageText" class="dialog-input" placeholder="输入你想说的话..." />
      <template #footer>
        <button class="btn-ghost" @click="messageDialog = false">取消</button>
        <button class="btn-warm" @click="sendMessage" style="margin-left: 8px">发送</button>
      </template>
    </el-dialog>
  </div>
</template>

<style scoped>
.detail-page {
  max-width: 1000px;
  margin: 0 auto;
}

/* 面包屑 */
.breadcrumb {
  font-size: 13px;
  color: var(--ink-light);
  margin-bottom: 24px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.breadcrumb span:not(.bc-sep):not(.bc-current) {
  cursor: pointer;
  transition: color 0.2s;
}

.breadcrumb span:not(.bc-sep):not(.bc-current):hover {
  color: var(--orange-brown);
}

.bc-sep { color: var(--ink-faint); opacity: 0.5; }
.bc-current { color: var(--ink-medium); }

/* 布局 */
.detail-layout {
  display: flex;
  gap: 48px;
  align-items: flex-start;
}

/* 封面区 */
.detail-cover-area {
  flex: 0 0 340px;
  position: sticky;
  top: 100px;
}

.cover-frame {
  position: relative;
  border-radius: 4px 14px 8px 4px;
  overflow: hidden;
  box-shadow: 6px 6px 0 rgba(61, 43, 31, 0.04), var(--shadow-card);
  aspect-ratio: 4 / 5;
  background: var(--warm-apricot-deep);
}

.cover-frame img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.cover-spine {
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  width: 8px;
  background: linear-gradient(to right, rgba(61, 43, 31, 0.12), transparent);
}

.cover-thumbs {
  display: flex;
  gap: 8px;
  margin-top: 12px;
}

.thumb {
  width: 56px;
  height: 70px;
  background: var(--warm-apricot-deep);
  border-radius: 2px 5px 5px 2px;
  cursor: pointer;
  transition: opacity 0.2s;
  opacity: 0.5;
}

.thumb.active {
  opacity: 1;
  box-shadow: 0 0 0 2px var(--orange-brown);
}

/* 信息区 */
.detail-info {
  flex: 1;
  min-width: 0;
}

.info-top {
  display: flex;
  gap: 10px;
  margin-bottom: 12px;
}

.info-category {
  font-size: 12px;
  color: var(--ink-light);
  padding: 3px 12px;
  background: var(--warm-apricot);
  border-radius: 12px;
  letter-spacing: 0.05em;
}

.info-condition {
  font-size: 12px;
  padding: 3px 12px;
  border-radius: 12px;
  letter-spacing: 0.05em;
}

.info-condition.九五新, .info-condition.九成新 {
  color: var(--sage-green);
  background: rgba(143, 166, 142, 0.1);
}

.info-condition.八成新 {
  color: var(--orange-brown);
  background: rgba(196, 112, 63, 0.08);
}

.info-condition.七成新 {
  color: var(--ink-light);
  background: rgba(139, 115, 85, 0.08);
}

.detail-title {
  font-family: var(--font-serif);
  font-size: 28px;
  font-weight: 600;
  color: var(--ink-dark);
  line-height: 1.4;
  margin-bottom: 16px;
}

.info-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  font-size: 14px;
  color: var(--ink-medium);
  margin-bottom: 28px;
}

.info-meta strong {
  color: var(--ink-light);
  font-weight: 400;
  margin-right: 6px;
  font-size: 12px;
}

/* 价格面板 */
.price-panel {
  background: var(--warm-apricot);
  border-radius: 10px 4px 10px 4px;
  padding: 20px 24px;
  margin-bottom: 24px;
  display: flex;
  align-items: baseline;
  gap: 24px;
}

.price-main {
  display: flex;
  align-items: baseline;
  gap: 4px;
}

.price-symbol {
  font-size: 18px;
  color: var(--orange-brown);
  opacity: 0.7;
}

.price-amount {
  font-family: var(--font-serif);
  font-size: 36px;
  font-weight: 700;
  color: var(--orange-brown);
  line-height: 1;
}

.price-unit {
  font-size: 14px;
  color: var(--ink-light);
  margin-left: 4px;
}

.price-original {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
}

.original-label { color: var(--ink-faint); }
.original-value { color: var(--ink-light); text-decoration: line-through; }
.discount-tag {
  padding: 2px 8px;
  background: rgba(196, 112, 63, 0.1);
  color: var(--orange-brown);
  border-radius: 4px;
  font-size: 12px;
}

/* 操作按钮 */
.action-row {
  display: flex;
  gap: 14px;
  margin-bottom: 28px;
}

.action-buy, .action-msg {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 28px;
  font-size: 15px;
}

/* 卖家栏 */
.seller-bar {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 16px 20px;
  background: var(--page-white);
  border-radius: 8px;
  box-shadow: var(--shadow-soft);
  margin-bottom: 32px;
}

.seller-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--dust-rose), var(--dust-rose-light));
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
  font-family: var(--font-serif);
}

.seller-info {
  display: flex;
  flex-direction: column;
  flex: 1;
}

.seller-name {
  font-size: 14px;
  font-weight: 500;
  color: var(--ink-dark);
}

.seller-school {
  font-size: 12px;
  color: var(--ink-light);
  margin-top: 2px;
}

.seller-meta {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  font-size: 12px;
  color: var(--ink-faint);
  gap: 2px;
}

/* 描述区 */
.description-area {
  border-top: 1px solid var(--warm-apricot-deep);
  padding-top: 24px;
}

.desc-heading {
  font-family: var(--font-serif);
  font-size: 16px;
  font-weight: 500;
  color: var(--ink-medium);
  margin-bottom: 14px;
  display: flex;
  align-items: center;
  gap: 10px;
}

.desc-line {
  width: 3px;
  height: 16px;
  background: var(--orange-brown);
  border-radius: 2px;
}

.desc-text {
  font-size: 14px;
  color: var(--ink-medium);
  line-height: 1.8;
}

/* 弹窗 */
.dialog-hint {
  font-size: 13px;
  color: var(--ink-light);
  margin-bottom: 12px;
}

.dialog-input {
  width: 100%;
  padding: 12px 14px;
  border: 1.5px solid var(--warm-apricot-deep);
  border-radius: 6px;
  font-size: 14px;
  font-family: var(--font-sans);
  outline: none;
  resize: none;
  min-height: 100px;
}

.dialog-input:focus {
  border-color: var(--orange-brown-light);
}

@media (max-width: 800px) {
  .detail-layout {
    flex-direction: column;
    gap: 28px;
  }

  .detail-cover-area {
    flex: none;
    width: 100%;
    position: static;
  }

  .cover-frame {
    max-width: 300px;
    margin: 0 auto;
  }

  .detail-title {
    font-size: 22px;
  }

  .price-panel {
    flex-direction: column;
    gap: 8px;
  }

  .action-row {
    flex-direction: column;
  }

  .action-buy, .action-msg {
    justify-content: center;
  }
}
</style>
