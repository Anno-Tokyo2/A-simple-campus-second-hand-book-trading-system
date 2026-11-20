<script setup>
import { ref, computed, onMounted } from 'vue'
import BookCard from '../components/BookCard.vue'
import api from '../api'

const books = ref([])
const loading = ref(true)
const searchQuery = ref('')
const categoryFilter = ref('')
const sortBy = ref('newest')

const demoBooks = [
  { id: 1, title: '高等数学（第七版）上册', author: '同济大学数学系', publisher: '高等教育出版社', price: 15, original_price: 46.5, condition: '九成新', category: '数学', cover_image: '高等数学（第七版）上册.jpg' },
  { id: 2, title: '线性代数', author: '同济大学数学系', publisher: '高等教育出版社', price: 12, original_price: 39, condition: '八成新', category: '数学', cover_image: '线性代数.jpg' },
  { id: 3, title: '数据结构与算法分析', author: 'Mark Allen Weiss', publisher: '机械工业出版社', price: 25, original_price: 69, condition: '九成新', category: '计算机', cover_image: '数据结构与算法分析.jpg' },
  { id: 4, title: '计算机网络', author: '谢希仁', publisher: '电子工业出版社', price: 18, original_price: 52, condition: '八成新', category: '计算机', cover_image: '计算机网络.jpg' },
  { id: 5, title: '大学英语综合教程1', author: '李荫华', publisher: '上海外语教育出版社', price: 10, original_price: 58, condition: '七成新', category: '英语', cover_image: '大学英语综合教程.jpg' },
  { id: 6, title: '概率论与数理统计', author: '浙江大学', publisher: '高等教育出版社', price: 12, original_price: 38, condition: '八成新', category: '数学', cover_image: '概率论与数理统计.jpg' },
  { id: 7, title: '操作系统概念', author: 'Abraham Silberschatz', publisher: '机械工业出版社', price: 30, original_price: 89, condition: '九五新', category: '计算机', cover_image: '操作系统概念.jpg' },
  { id: 8, title: '数据库系统概论', author: '王珊', publisher: '高等教育出版社', price: 15, original_price: 45, condition: '八成新', category: '计算机', cover_image: '数据库系统概论.jpg' },
  { id: 9, title: 'Python编程导论', author: 'John Guttag', publisher: '人民邮电出版社', price: 20, original_price: 65, condition: '九成新', category: '计算机', cover_image: 'Python编程导论.jpg' },
  { id: 10, title: '微观经济学', author: '曼昆', publisher: '北京大学出版社', price: 22, original_price: 72, condition: '九成新', category: '经济', cover_image: '微观经济学.jpg' },
  { id: 11, title: '大学物理', author: '马文蔚', publisher: '高等教育出版社', price: 15, original_price: 49, condition: '八成新', category: '物理', cover_image: '大学物理.jpg' },
  { id: 12, title: '人工智能导论', author: 'Stuart Russell', publisher: '清华大学出版社', price: 28, original_price: 85, condition: '九五新', category: '计算机', cover_image: '人工智能导论.jpg' },
  { id: 13, title: '毛泽东思想概论', author: '教材编写组', publisher: '高等教育出版社', price: 8, original_price: 25, condition: '七成新', category: '政治', cover_image: '毛泽东思想概论.jpg' },
  { id: 14, title: '离散数学', author: '屈婉玲', publisher: '高等教育出版社', price: 14, original_price: 42, condition: '八成新', category: '数学', cover_image: '离散数学.jpg' },
  { id: 15, title: '编译原理', author: 'Alfred V. Aho', publisher: '机械工业出版社', price: 22, original_price: 68, condition: '九成新', category: '计算机', cover_image: '编译原理.png' },
]

const categories = ['全部', '数学', '计算机', '英语', '经济', '物理', '政治', '文学', '其他']

const filteredBooks = computed(() => {
  let result = [...books.value]
  if (searchQuery.value) {
    const q = searchQuery.value.toLowerCase()
    result = result.filter(b =>
      b.title.toLowerCase().includes(q) || b.author.toLowerCase().includes(q)
    )
  }
  if (categoryFilter.value && categoryFilter.value !== '全部') {
    result = result.filter(b => b.category === categoryFilter.value)
  }
  if (sortBy.value === 'price-asc') result.sort((a, b) => a.price - b.price)
  else if (sortBy.value === 'price-desc') result.sort((a, b) => b.price - a.price)
  return result
})

const totalBooks = computed(() => filteredBooks.value.length)

onMounted(async () => {
  try {
    const res = await api.get('/api/books')
    books.value = res.data.items?.length ? res.data.items : demoBooks
  } catch {
    books.value = demoBooks
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <div class="book-list-page">
    <!-- 页面头部 - 独特的左右不对称布局 -->
    <header class="list-header">
      <div class="list-header__left">
        <h1 class="list-title">书 市</h1>
        <p class="list-subtitle">Book Market</p>
        <div class="list-count">
          <span class="count-num">{{ totalBooks }}</span>
          <span class="count-label">本在售</span>
        </div>
      </div>
      <div class="list-header__right">
        <p class="header-quote">「每一本旧书都值得被再次翻开」</p>
      </div>
    </header>

    <!-- 筛选栏 - 横向标签式，非传统表单 -->
    <div class="filter-bar">
      <div class="filter-tabs">
        <button
          v-for="cat in categories"
          :key="cat"
          class="filter-tab"
          :class="{ active: (categoryFilter || '全部') === cat }"
          @click="categoryFilter = cat === '全部' ? '' : cat"
        >
          {{ cat }}
        </button>
      </div>

      <div class="filter-right">
        <div class="search-box">
          <svg class="search-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/>
          </svg>
          <input
            v-model="searchQuery"
            type="text"
            class="search-input"
            placeholder="搜索书名或作者..."
          />
        </div>
        <select v-model="sortBy" class="sort-select">
          <option value="newest">最新发布</option>
          <option value="price-asc">价格从低到高</option>
          <option value="price-desc">价格从高到低</option>
        </select>
      </div>
    </div>

    <!-- 书籍网格 - 错落布局 -->
    <div class="books-area" v-loading="loading">
      <div v-if="filteredBooks.length === 0 && !loading" class="empty-state">
        <div class="empty-book">
          <div class="empty-book-spine"></div>
          <div class="empty-book-body"></div>
        </div>
        <p class="empty-text">暂未找到相关书籍</p>
        <p class="empty-hint">试试其他关键词或分类</p>
      </div>

      <div v-else class="books-masonry">
        <div
          v-for="(book, idx) in filteredBooks"
          :key="book.id"
          class="masonry-item"
          :class="`masonry-item--${idx % 5}`"
        >
          <BookCard :book="book" />
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.book-list-page {
  width: 100%;
}

/* ===== 页面头部 ===== */
.list-header {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  padding: 20px 0 32px;
  border-bottom: 1px solid var(--warm-apricot-deep);
  margin-bottom: 28px;
}

.list-title {
  font-family: var(--font-serif);
  font-size: 36px;
  font-weight: 600;
  color: var(--ink-dark);
  letter-spacing: 0.15em;
  line-height: 1;
}

.list-subtitle {
  font-size: 11px;
  color: var(--ink-faint);
  letter-spacing: 0.2em;
  text-transform: uppercase;
  margin-top: 4px;
}

.list-count {
  display: flex;
  align-items: baseline;
  gap: 6px;
  margin-top: 12px;
}

.count-num {
  font-family: var(--font-serif);
  font-size: 28px;
  font-weight: 600;
  color: var(--orange-brown);
}

.count-label {
  font-size: 13px;
  color: var(--ink-light);
}

.header-quote {
  font-family: var(--font-serif);
  font-size: 14px;
  color: var(--ink-faint);
  letter-spacing: 0.08em;
  font-style: italic;
}

/* ===== 筛选栏 - 标签式 ===== */
.filter-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 20px;
  margin-bottom: 32px;
  flex-wrap: wrap;
}

.filter-tabs {
  display: flex;
  gap: 4px;
  flex-wrap: wrap;
}

.filter-tab {
  padding: 7px 18px;
  font-size: 13px;
  font-family: var(--font-sans);
  color: var(--ink-light);
  background: transparent;
  border: 1.5px solid transparent;
  border-radius: 20px;
  cursor: pointer;
  transition: all 0.2s ease;
  letter-spacing: 0.04em;
}

.filter-tab:hover {
  color: var(--orange-brown);
  background: rgba(196, 112, 63, 0.04);
}

.filter-tab.active {
  color: var(--orange-brown);
  border-color: var(--orange-brown);
  background: rgba(196, 112, 63, 0.06);
  font-weight: 500;
}

.filter-right {
  display: flex;
  gap: 12px;
  align-items: center;
}

.search-box {
  position: relative;
  display: flex;
  align-items: center;
}

.search-icon {
  position: absolute;
  left: 12px;
  color: var(--ink-faint);
  pointer-events: none;
}

.search-input {
  padding: 8px 14px 8px 36px;
  border: 1.5px solid var(--warm-apricot-deep);
  border-radius: 20px;
  font-size: 13px;
  font-family: var(--font-sans);
  color: var(--ink-dark);
  background: var(--page-white);
  outline: none;
  width: 220px;
  transition: border-color 0.2s, width 0.3s;
}

.search-input:focus {
  border-color: var(--orange-brown-light);
  width: 280px;
}

.search-input::placeholder {
  color: var(--ink-faint);
}

.sort-select {
  padding: 8px 12px;
  border: 1.5px solid var(--warm-apricot-deep);
  border-radius: 6px;
  font-size: 13px;
  font-family: var(--font-sans);
  color: var(--ink-medium);
  background: var(--page-white);
  outline: none;
  cursor: pointer;
}

/* ===== 书籍网格 - 错落布局 ===== */
.books-masonry {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 18px;
  align-items: start;
}

/* 错落效果：每个位置微调 */
.masonry-item--0 { transform: translateY(0); }
.masonry-item--1 { transform: translateY(8px); }
.masonry-item--2 { transform: translateY(-4px); }
.masonry-item--3 { transform: translateY(12px); }
.masonry-item--4 { transform: translateY(2px); }

/* 空状态 */
.empty-state {
  text-align: center;
  padding: 80px 20px;
}

.empty-book {
  position: relative;
  width: 48px;
  height: 60px;
  margin: 0 auto 20px;
}

.empty-book-spine {
  position: absolute;
  left: 0;
  top: 0;
  width: 4px;
  height: 60px;
  background: var(--dust-rose-muted);
  border-radius: 1px;
}

.empty-book-body {
  position: absolute;
  left: 5px;
  top: 2px;
  width: 38px;
  height: 56px;
  background: var(--warm-apricot-deep);
  border-radius: 1px 4px 4px 1px;
}

.empty-text {
  font-family: var(--font-serif);
  font-size: 16px;
  color: var(--ink-medium);
  margin-bottom: 6px;
}

.empty-hint {
  font-size: 13px;
  color: var(--ink-faint);
}

/* 响应式 */
@media (max-width: 1000px) {
  .books-masonry {
    grid-template-columns: repeat(3, 1fr);
    gap: 14px;
  }
}

@media (max-width: 600px) {
  .list-title {
    font-size: 28px;
  }
  .list-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }

  .filter-bar {
    flex-direction: column;
    align-items: flex-start;
  }

  .filter-right {
    width: 100%;
  }

  .search-input {
    width: 100%;
  }
  .search-input:focus {
    width: 100%;
  }

  .books-masonry {
    grid-template-columns: repeat(2, 1fr);
    gap: 12px;
  }

  .masonry-item {
    transform: none !important;
  }
}
</style>
