<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import BookCard from '../components/BookCard.vue'
import api from '../api'

const router = useRouter()
const hotBooks = ref([])
const loading = ref(true)

const demoBooks = [
  { id: 1, title: '高等数学（第七版）上册', author: '同济大学数学系', publisher: '高等教育出版社', price: 15, original_price: 46.5, condition: '九成新', category: '数学', cover_image: '高等数学（第七版）上册.jpg' },
  { id: 2, title: '线性代数', author: '同济大学数学系', publisher: '高等教育出版社', price: 12, original_price: 39, condition: '八成新', category: '数学', cover_image: '线性代数.jpg' },
  { id: 3, title: '数据结构与算法分析', author: 'Mark Allen Weiss', publisher: '机械工业出版社', price: 25, original_price: 69, condition: '九成新', category: '计算机', cover_image: '数据结构与算法分析.jpg' },
  { id: 4, title: '计算机网络', author: '谢希仁', publisher: '电子工业出版社', price: 18, original_price: 52, condition: '八成新', category: '计算机', cover_image: '计算机网络.jpg' },
  { id: 5, title: '大学英语综合教程1', author: '李荫华', publisher: '上海外语教育出版社', price: 10, original_price: 58, condition: '七成新', category: '英语', cover_image: '大学英语综合教程.jpg' },
  { id: 6, title: '概率论与数理统计', author: '浙江大学', publisher: '高等教育出版社', price: 12, original_price: 38, condition: '八成新', category: '数学', cover_image: '概率论与数理统计.jpg' },
  { id: 7, title: '操作系统概念', author: 'Abraham Silberschatz', publisher: '机械工业出版社', price: 30, original_price: 89, condition: '九五新', category: '计算机', cover_image: '操作系统概念.jpg' },
  { id: 8, title: '数据库系统概论', author: '王珊', publisher: '高等教育出版社', price: 15, original_price: 45, condition: '八成新', category: '计算机', cover_image: '数据库系统概论.jpg' }
]

const stats = ref({ users: 10, books: 15 })

onMounted(async () => {
  try {
    const res = await api.get('/api/books?limit=8')
    hotBooks.value = res.data.items?.length ? res.data.items : demoBooks
  } catch {
    hotBooks.value = demoBooks
  } finally {
    loading.value = false
  }
  // 获取真实统计
  try {
    const s = await api.get('/api/stats')
    stats.value = s.data
  } catch {}
})

const quickActions = [
  { icon: 'search', label: '逛书市', desc: '发现好书', path: '/books' },
  { icon: 'edit', label: '卖闲置', desc: '轻松出书', path: '/publish' },
  { icon: 'tag', label: '去求购', desc: '发布需求', path: '/wantbuy' },
]
</script>

<template>
  <div class="home">
    <!-- Hero - 非对称双栏布局 -->
    <section class="hero-section">
      <div class="hero-content">
        <div class="hero-text-area">
          <p class="hero-kicker">校园二手书交易平台</p>
          <h1 class="hero-title">
            让闲置的书<br />
            <span class="hero-highlight">重新被翻阅</span>
          </h1>
          <p class="hero-desc">
            每一本旧书都藏着上一位读者的笔记与温度。<br />
            用书币交易，让知识在校园里流转。
          </p>
          <div class="hero-actions">
            <button class="btn-warm hero-btn" @click="router.push('/books')">
              浏览书市
            </button>
            <button class="btn-ghost hero-btn" @click="router.push('/publish')">
              发布书籍
            </button>
          </div>
        </div>

        <!-- 右侧装饰 - 书堆插画 (纯CSS) -->
        <div class="hero-visual">
          <div class="book-stack">
            <div class="stack-book stack-book--1"></div>
            <div class="stack-book stack-book--2"></div>
            <div class="stack-book stack-book--3"></div>
            <div class="stack-book stack-book--4"></div>
            <div class="stack-book stack-book--5"></div>
          </div>
          <div class="hero-stats">
            <div class="stat-item">
              <span class="stat-num">{{ stats.books }}</span>
              <span class="stat-label">本在售</span>
            </div>
            <div class="stat-divider"></div>
            <div class="stat-item">
              <span class="stat-num">{{ stats.users }}</span>
              <span class="stat-label">位同学</span>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- 快捷入口 - 横向错落卡片 -->
    <section class="quick-section">
      <div
        v-for="(action, idx) in quickActions"
        :key="action.label"
        class="quick-card"
        :class="`quick-card--${idx}`"
        @click="router.push(action.path)"
      >
        <div class="quick-icon">
          <svg v-if="action.icon === 'search'" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
            <circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/>
          </svg>
          <svg v-if="action.icon === 'edit'" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
            <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/>
          </svg>
          <svg v-if="action.icon === 'tag'" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
            <path d="M20.59 13.41l-7.17 7.17a2 2 0 0 1-2.83 0L2 12V2h10l8.59 8.59a2 2 0 0 1 0 2.82z"/><line x1="7" y1="7" x2="7.01" y2="7"/>
          </svg>
        </div>
        <div class="quick-text">
          <span class="quick-label">{{ action.label }}</span>
          <span class="quick-desc">{{ action.desc }}</span>
        </div>
        <div class="quick-arrow">→</div>
      </div>
    </section>

    <!-- 热门书籍 - 不规则网格 -->
    <section class="hot-section">
      <div class="section-header">
        <div class="section-header-text">
          <h2 class="section-title">近期上架</h2>
          <p class="section-sub">同学们刚刚发布的书籍</p>
        </div>
        <button class="btn-ghost" @click="router.push('/books')">全部书籍 →</button>
      </div>

      <div v-if="loading" class="loading-placeholder">
        <div v-for="i in 4" :key="i" class="skeleton-card"></div>
      </div>

      <div v-else class="books-grid">
        <BookCard
          v-for="book in hotBooks.slice(0, 8)"
          :key="book.id"
          :book="book"
        />
      </div>
    </section>

    <!-- 底部装饰 -->
    <section class="deco-section">
      <div class="deco-inner">
        <div class="deco-line"></div>
        <p class="deco-quote">「书非借不能读也」</p>
        <p class="deco-author">—— 袁枚《黄生借书说》</p>
      </div>
    </section>
  </div>
</template>

<style scoped>
.home {
  width: 100%;
}

/* ===== Hero 区域 ===== */
.hero-section {
  padding: 40px 0 50px;
}

.hero-content {
  display: flex;
  align-items: center;
  gap: 60px;
}

.hero-text-area {
  flex: 1;
}

.hero-kicker {
  font-size: 12px;
  letter-spacing: 0.2em;
  color: var(--ink-faint);
  text-transform: uppercase;
  margin-bottom: 16px;
  font-family: var(--font-sans);
}

.hero-title {
  font-family: var(--font-serif);
  font-size: 40px;
  font-weight: 600;
  line-height: 1.35;
  color: var(--ink-dark);
  margin-bottom: 20px;
  letter-spacing: 0.02em;
}

.hero-highlight {
  color: var(--orange-brown);
  position: relative;
}

.hero-highlight::after {
  content: '';
  position: absolute;
  bottom: 2px;
  left: 0;
  right: 0;
  height: 8px;
  background: rgba(196, 112, 63, 0.1);
  border-radius: 2px;
  z-index: -1;
}

.hero-desc {
  font-size: 15px;
  color: var(--ink-light);
  line-height: 1.8;
  margin-bottom: 32px;
  max-width: 380px;
}

.hero-actions {
  display: flex;
  gap: 12px;
}

.hero-btn {
  padding: 12px 28px;
  font-size: 15px;
}

/* 书堆 CSS 插画 */
.hero-visual {
  flex-shrink: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 28px;
}

.book-stack {
  position: relative;
  width: 160px;
  height: 180px;
}

.stack-book {
  position: absolute;
  border-radius: 2px 6px 6px 2px;
  box-shadow: 2px 2px 6px rgba(61, 43, 31, 0.08);
}

.stack-book--1 {
  bottom: 0;
  left: 10px;
  width: 120px;
  height: 28px;
  background: linear-gradient(90deg, var(--orange-brown), var(--orange-brown-light));
}
.stack-book--2 {
  bottom: 26px;
  left: 20px;
  width: 110px;
  height: 24px;
  background: linear-gradient(90deg, var(--dust-rose), var(--dust-rose-light));
  transform: rotate(-2deg);
}
.stack-book--3 {
  bottom: 48px;
  left: 15px;
  width: 130px;
  height: 30px;
  background: linear-gradient(90deg, var(--sage-green), var(--sage-light));
  transform: rotate(1deg);
}
.stack-book--4 {
  bottom: 76px;
  left: 25px;
  width: 100px;
  height: 22px;
  background: linear-gradient(90deg, #B8945C, #CCA870);
  transform: rotate(-1.5deg);
}
.stack-book--5 {
  bottom: 96px;
  left: 30px;
  width: 90px;
  height: 26px;
  background: linear-gradient(90deg, var(--orange-brown-dark), var(--orange-brown));
  transform: rotate(2deg);
}

.hero-stats {
  display: flex;
  align-items: center;
  gap: 20px;
  padding: 16px 24px;
  background: var(--page-white);
  border-radius: 8px 3px 8px 3px;
  box-shadow: var(--shadow-card);
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.stat-num {
  font-family: var(--font-serif);
  font-size: 24px;
  font-weight: 600;
  color: var(--orange-brown);
}

.stat-label {
  font-size: 12px;
  color: var(--ink-faint);
  margin-top: 2px;
}

.stat-divider {
  width: 1px;
  height: 30px;
  background: var(--warm-apricot-deep);
}

/* ===== 快捷入口 ===== */
.quick-section {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
  margin-bottom: 56px;
}

.quick-card {
  background: var(--page-white);
  padding: 24px 20px;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 16px;
  position: relative;
  overflow: hidden;
}

/* 每个卡片不同圆角 */
.quick-card--0 {
  border-radius: 12px 4px 12px 4px;
}
.quick-card--1 {
  border-radius: 4px 14px 4px 10px;
  margin-top: 12px;
}
.quick-card--2 {
  border-radius: 8px 4px 14px 6px;
  margin-top: -8px;
}

.quick-card:hover {
  transform: translateY(-3px);
  box-shadow: var(--shadow-hover);
}

.quick-icon {
  width: 44px;
  height: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 10px 3px 10px 3px;
  background: var(--warm-apricot);
  color: var(--orange-brown);
  flex-shrink: 0;
}

.quick-text {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.quick-label {
  font-family: var(--font-serif);
  font-size: 16px;
  font-weight: 500;
  color: var(--ink-dark);
}

.quick-desc {
  font-size: 12px;
  color: var(--ink-light);
  margin-top: 2px;
}

.quick-arrow {
  font-size: 16px;
  color: var(--ink-faint);
  transition: transform 0.2s;
}

.quick-card:hover .quick-arrow {
  transform: translateX(4px);
  color: var(--orange-brown);
}

/* ===== 热门书籍区 ===== */
.hot-section {
  margin-bottom: 48px;
}

.section-header {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  margin-bottom: 28px;
}

.section-title {
  font-family: var(--font-serif);
  font-size: 22px;
  font-weight: 600;
  color: var(--ink-dark);
  letter-spacing: 0.05em;
}

.section-sub {
  font-size: 13px;
  color: var(--ink-light);
  margin-top: 4px;
}

/* 均匀四列网格 */
.books-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 18px;
  align-items: start;
}

/* 加载占位 */
.loading-placeholder {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
}

.skeleton-card {
  aspect-ratio: 4 / 5;
  background: var(--warm-apricot-deep);
  border-radius: 6px 10px 4px 8px;
  animation: gentlePulse 1.5s ease-in-out infinite;
}

/* ===== 底部装饰 ===== */
.deco-section {
  padding: 40px 0 20px;
}

.deco-inner {
  text-align: center;
}

.deco-line {
  width: 40px;
  height: 1px;
  background: var(--dust-rose-muted);
  margin: 0 auto 20px;
}

.deco-quote {
  font-family: var(--font-serif);
  font-size: 16px;
  color: var(--ink-medium);
  letter-spacing: 0.15em;
}

.deco-author {
  font-size: 12px;
  color: var(--ink-faint);
  margin-top: 8px;
  letter-spacing: 0.1em;
}

/* ===== 响应式 ===== */
@media (max-width: 1000px) {
  .hero-content {
    flex-direction: column;
    gap: 32px;
    text-align: center;
  }

  .hero-title {
    font-size: 32px;
  }

  .hero-desc {
    max-width: 100%;
    margin-left: auto;
    margin-right: auto;
  }

  .hero-actions {
    justify-content: center;
  }

  .books-grid {
    grid-template-columns: repeat(3, 1fr);
    gap: 14px;
  }

  .quick-section {
    grid-template-columns: repeat(3, 1fr);
    gap: 12px;
  }

  .quick-card--1, .quick-card--2 {
    margin-top: 0;
  }
}

@media (max-width: 700px) {
  .books-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 12px;
  }

  .quick-section {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 600px) {
  .hero-title {
    font-size: 26px;
  }

  .loading-placeholder {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>
