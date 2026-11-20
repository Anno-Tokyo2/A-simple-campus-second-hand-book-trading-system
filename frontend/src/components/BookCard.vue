<script setup>
import { useRouter } from 'vue-router'
import { computed } from 'vue'
import BookCover from './BookCover.vue'

const props = defineProps({
  book: { type: Object, required: true },
  variant: { type: String, default: 'default' } // default / featured / compact
})

const router = useRouter()

const hasRealCover = computed(() => {
  return props.book.cover_image && props.book.cover_image !== ''
})

function getCoverUrl() {
  return props.book.cover_image.startsWith('http')
    ? props.book.cover_image
    : `/static/uploads/${props.book.cover_image}`
}

// 不统一的圆角 - 根据位置变化
const radiusStyle = computed(() => {
  const variants = [
    '3px 10px 4px 12px',
    '8px 3px 12px 5px',
    '4px 12px 6px 10px',
    '10px 5px 8px 3px',
  ]
  const idx = (props.book.id || 0) % variants.length
  return { borderRadius: variants[idx] }
})

// 条件标签颜色
const conditionColor = computed(() => {
  const map = {
    '九五新': 'var(--sage-green)',
    '九成新': 'var(--orange-brown)',
    '八成新': 'var(--dust-rose)',
    '七成新': 'var(--ink-light)',
    '六成新及以下': 'var(--ink-faint)',
  }
  return map[props.book.condition] || 'var(--dust-rose)'
})

function handleClick() {
  router.push(`/books/${props.book.id}`)
}
</script>

<template>
  <div
    class="book-card"
    :class="[`book-card--${variant}`]"
    @click="handleClick"
  >
    <!-- 书脊装饰 -->
    <div class="book-card__spine"></div>

    <!-- 封面 -->
    <div class="book-card__cover" :style="radiusStyle">
      <img v-if="hasRealCover" :src="getCoverUrl()" :alt="book.title" loading="lazy" />
      <BookCover
        v-else
        :title="book.title"
        :author="book.author"
        :category="book.category"
        :publisher="book.publisher"
      />
      <!-- 条件标签 - 贴在封面上 -->
      <span class="book-card__badge" :style="{ background: conditionColor }">
        {{ book.condition }}
      </span>
    </div>

    <!-- 信息区 -->
    <div class="book-card__info">
      <h3 class="book-card__title">{{ book.title }}</h3>
      <p class="book-card__author">{{ book.author }}</p>
      <div class="book-card__footer">
        <span class="book-card__price">
          <span class="coin-symbol">◎</span>{{ book.price }}
        </span>
        <span v-if="book.original_price" class="book-card__original">
          原价 ¥{{ book.original_price }}
        </span>
      </div>
    </div>
  </div>
</template>

<style scoped>
.book-card {
  position: relative;
  cursor: pointer;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  display: flex;
  flex-direction: column;
}

.book-card:hover {
  transform: translateY(-6px) rotate(-0.5deg);
}

/* 书脊 */
.book-card__spine {
  position: absolute;
  left: -2px;
  top: 8%;
  bottom: 8%;
  width: 3px;
  background: linear-gradient(to bottom, transparent, var(--orange-brown), var(--dust-rose-muted), transparent);
  border-radius: 2px;
  opacity: 0;
  transition: opacity 0.3s;
}

.book-card:hover .book-card__spine {
  opacity: 0.5;
}

/* 封面 */
.book-card__cover {
  position: relative;
  aspect-ratio: 3 / 4;
  overflow: hidden;
  background: var(--warm-apricot-deep);
  box-shadow: var(--shadow-card);
  transition: box-shadow 0.3s ease;
}

.book-card:hover .book-card__cover {
  box-shadow: var(--shadow-hover);
}

.book-card__cover img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.4s ease;
}

.book-card:hover .book-card__cover img {
  transform: scale(1.03);
}

/* 条件标签 */
.book-card__badge {
  position: absolute;
  top: 10px;
  right: 10px;
  padding: 3px 10px;
  font-size: 11px;
  color: white;
  border-radius: 3px 1px 3px 1px;
  letter-spacing: 0.05em;
  box-shadow: 0 1px 4px rgba(0,0,0,0.15);
}

/* 信息区 */
.book-card__info {
  padding: 12px 4px 6px;
}

.book-card__title {
  font-family: var(--font-serif);
  font-size: 14px;
  font-weight: 500;
  color: var(--ink-dark);
  line-height: 1.5;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  margin-bottom: 4px;
}

.book-card__author {
  font-size: 12px;
  color: var(--ink-light);
  margin-bottom: 8px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.book-card__footer {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  gap: 8px;
}

.book-card__price {
  font-family: var(--font-serif);
  font-size: 18px;
  font-weight: 600;
  color: var(--orange-brown);
  display: flex;
  align-items: baseline;
  gap: 2px;
}

.coin-symbol {
  font-size: 14px;
  opacity: 0.7;
}

.book-card__original {
  font-size: 11px;
  color: var(--ink-faint);
  text-decoration: line-through;
}

/* Featured 变体 - 稍大的展示卡片 */
.book-card--featured .book-card__cover {
  aspect-ratio: 3 / 4;
}

.book-card--featured .book-card__title {
  font-size: 16px;
}

.book-card--featured .book-card__price {
  font-size: 20px;
}

/* Compact 变体 - 横向小卡片 */
.book-card--compact {
  flex-direction: row;
  gap: 14px;
}

.book-card--compact .book-card__cover {
  width: 80px;
  min-width: 80px;
  aspect-ratio: 3 / 4;
  border-radius: 2px 6px 6px 2px;
}

.book-card--compact .book-card__info {
  padding: 4px 0;
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.book-card--compact .book-card__title {
  font-size: 13px;
  -webkit-line-clamp: 1;
}

.book-card--compact .book-card__price {
  font-size: 15px;
}
</style>
