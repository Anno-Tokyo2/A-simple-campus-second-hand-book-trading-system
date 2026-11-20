<script setup>
import { computed } from 'vue'

const props = defineProps({
  title: { type: String, default: '' },
  author: { type: String, default: '' },
  category: { type: String, default: '' },
  publisher: { type: String, default: '' },
  src: { type: String, default: '' }
})

function hash(str) {
  let h = 0
  for (let i = 0; i < str.length; i++) {
    h = ((h << 5) - h) + str.charCodeAt(i)
    h |= 0
  }
  return Math.abs(h)
}

const seed = computed(() => hash(props.title || 'book'))

// 分类 → 封面设计方案
const designs = {
  '数学': {
    bg: ['#1a5276', '#2471a3', '#1b4f72', '#154360'],
    accent: ['#f39c12', '#e67e22', '#d4ac0d', '#f1c40f'],
    style: 'geometric' // 几何图形
  },
  '计算机': {
    bg: ['#145a32', '#1e8449', '#0b5345', '#196f3d'],
    accent: ['#2ecc71', '#82e0aa', '#76d7c4', '#a3e4d7'],
    style: 'circuit' // 电路线条
  },
  '英语': {
    bg: ['#6c3483', '#7d3c98', '#5b2c6f', '#4a235a'],
    accent: ['#d2b4de', '#e8daef', '#aed6f1', '#a9cce3'],
    style: 'classic' // 经典优雅
  },
  '经济': {
    bg: ['#784212', '#6e2c00', '#7b5e3a', '#6d4c2a'],
    accent: ['#f0d9b5', '#e8c579', '#d4a547', '#c9a23a'],
    style: 'formal' // 正式商务
  },
  '物理': {
    bg: ['#1b2631', '#2c3e50', '#212f3d', '#1c2833'],
    accent: ['#5dade2', '#85c1e9', '#7fb3d8', '#48c9b0'],
    style: 'wave' // 波动/粒子
  },
  '政治': {
    bg: ['#922b21', '#a93226', '#7b241c', '#641e16'],
    accent: ['#f5b041', '#f9e79f', '#fad7a0', '#f8c471'],
    style: 'banner' // 横幅/徽章
  },
  '文学': {
    bg: ['#4a2c2a', '#5d4037', '#6d4c41', '#3e2723'],
    accent: ['#d7ccc8', '#bcaaa4', '#a1887f', '#efebe9'],
    style: 'ink' // 水墨风
  }
}
const defaultDesign = {
  bg: ['#5c4033', '#6b4f3f', '#7a5f4b', '#4a3728'],
  accent: ['#d4a574', '#c9956b', '#b8860b', '#daa520'],
  style: 'classic'
}

const design = computed(() => designs[props.category] || defaultDesign)
const bgColor = computed(() => design.value.bg[seed.value % design.value.bg.length])
const accentColor = computed(() => design.value.accent[seed.value % design.value.accent.length])
const secondAccent = computed(() => design.value.accent[(seed.value + 1) % design.value.accent.length])
const spineWidth = computed(() => 5 + (seed.value % 4))

// 装饰元素位置
const decoPositions = computed(() => {
  const s = seed.value
  return {
    line1: 18 + (s % 15),
    line2: 72 + (s % 12),
    dotX: 20 + (s % 60),
    dotY: 80 + (s % 10)
  }
})

// 出版社简称
const shortPublisher = computed(() => {
  const p = props.publisher || ''
  if (p.includes('高等教育')) return '高教社'
  if (p.includes('机械工业')) return '机工社'
  if (p.includes('人民邮电')) return '人邮社'
  if (p.includes('电子工业')) return '电子社'
  if (p.includes('清华大学')) return '清华社'
  if (p.includes('北京大学')) return '北大社'
  if (p.includes('外语教育')) return '外教社'
  return p.slice(0, 4)
})

// 标题拆行（竖排或横排）
const titleChars = computed(() => {
  const t = props.title || ''
  // 如果标题短，竖排；长标题横排
  if (t.length <= 6) return t.split('')
  return null
})

const titleLines = computed(() => {
  if (titleChars.value) return null
  const t = props.title || ''
  // 拆成2-3行
  const len = t.length
  if (len <= 10) return [t]
  const mid = Math.ceil(len / 2)
  // 找中间的标点或括号断行
  for (let i = mid; i < Math.min(mid + 3, len); i++) {
    if ('（(、· '.includes(t[i])) return [t.slice(0, i + 1), t.slice(i + 1)]
  }
  for (let i = mid; i > Math.max(mid - 3, 0); i--) {
    if ('（(、· '.includes(t[i])) return [t.slice(0, i + 1), t.slice(i + 1)]
  }
  return [t.slice(0, mid), t.slice(mid)]
})
</script>

<template>
  <div class="cover" :style="{ background: bgColor }">
    <!-- 纸张纹理 -->
    <div class="cover__texture"></div>

    <!-- 书脊 -->
    <div class="cover__spine" :style="{ width: spineWidth + 'px' }">
      <div class="spine__line" :style="{ background: accentColor }"></div>
    </div>

    <!-- 顶部装饰线 -->
    <div class="cover__top-line" :style="{ background: accentColor }"></div>
    <!-- 底部装饰线 -->
    <div class="cover__bottom-line" :style="{ background: accentColor }"></div>

    <!-- 装饰元素 - 根据风格不同 -->
    <!-- 几何风（数学） -->
    <svg v-if="design.style === 'geometric'" class="cover__deco" viewBox="0 0 200 280" fill="none">
      <circle :cx="decoPositions.dotX + 20" cy="40" r="18" :stroke="accentColor" stroke-width="0.8" opacity="0.25"/>
      <line x1="20" :y1="decoPositions.line1" x2="80" :y2="decoPositions.line1" :stroke="secondAccent" stroke-width="0.5" opacity="0.2"/>
      <rect x="140" y="200" width="30" height="30" :stroke="accentColor" stroke-width="0.6" opacity="0.15" transform="rotate(15 155 215)"/>
      <polygon points="160,60 175,85 145,85" :stroke="secondAccent" stroke-width="0.6" opacity="0.2" fill="none"/>
    </svg>

    <!-- 电路风（计算机） -->
    <svg v-if="design.style === 'circuit'" class="cover__deco" viewBox="0 0 200 280" fill="none">
      <path d="M 20 40 L 60 40 L 60 70 L 100 70" :stroke="accentColor" stroke-width="0.8" opacity="0.2"/>
      <circle cx="60" cy="40" r="3" :fill="accentColor" opacity="0.15"/>
      <circle cx="60" cy="70" r="3" :fill="accentColor" opacity="0.15"/>
      <path d="M 150 200 L 150 230 L 180 230" :stroke="secondAccent" stroke-width="0.6" opacity="0.15"/>
      <rect x="15" y="210" width="8" height="8" :stroke="accentColor" stroke-width="0.5" opacity="0.15"/>
    </svg>

    <!-- 经典风（英语） -->
    <svg v-if="design.style === 'classic'" class="cover__deco" viewBox="0 0 200 280" fill="none">
      <line x1="30" y1="30" x2="170" y2="30" :stroke="accentColor" stroke-width="0.5" opacity="0.2"/>
      <line x1="30" y1="35" x2="120" y2="35" :stroke="secondAccent" stroke-width="0.3" opacity="0.15"/>
      <circle cx="100" cy="240" r="20" :stroke="accentColor" stroke-width="0.5" opacity="0.15"/>
    </svg>

    <!-- 正式风（经济） -->
    <svg v-if="design.style === 'formal'" class="cover__deco" viewBox="0 0 200 280" fill="none">
      <rect x="25" y="25" width="150" height="230" :stroke="accentColor" stroke-width="0.5" opacity="0.12" rx="2"/>
      <line x1="40" y1="240" x2="160" y2="240" :stroke="secondAccent" stroke-width="0.4" opacity="0.15"/>
    </svg>

    <!-- 波动风（物理） -->
    <svg v-if="design.style === 'wave'" class="cover__deco" viewBox="0 0 200 280" fill="none">
      <path d="M 0 60 Q 50 40, 100 60 T 200 60" :stroke="accentColor" stroke-width="0.8" opacity="0.15" fill="none"/>
      <path d="M 0 70 Q 50 50, 100 70 T 200 70" :stroke="secondAccent" stroke-width="0.5" opacity="0.1" fill="none"/>
      <circle cx="50" cy="220" r="4" :fill="accentColor" opacity="0.12"/>
      <circle cx="150" cy="210" r="3" :fill="secondAccent" opacity="0.1"/>
    </svg>

    <!-- 横幅风（政治） -->
    <svg v-if="design.style === 'banner'" class="cover__deco" viewBox="0 0 200 280" fill="none">
      <line x1="30" y1="35" x2="170" y2="35" :stroke="accentColor" stroke-width="0.8" opacity="0.25"/>
      <line x1="50" y1="40" x2="150" y2="40" :stroke="secondAccent" stroke-width="0.4" opacity="0.15"/>
      <line x1="30" y1="240" x2="170" y2="240" :stroke="accentColor" stroke-width="0.8" opacity="0.25"/>
    </svg>

    <!-- 水墨风（文学） -->
    <svg v-if="design.style === 'ink'" class="cover__deco" viewBox="0 0 200 280" fill="none">
      <circle cx="140" cy="60" r="30" :stroke="accentColor" stroke-width="0.4" opacity="0.1" fill="none"/>
      <circle cx="140" cy="60" r="22" :stroke="secondAccent" stroke-width="0.3" opacity="0.08" fill="none"/>
      <path d="M 20 220 Q 60 200, 100 220 T 180 220" :stroke="accentColor" stroke-width="0.5" opacity="0.12" fill="none"/>
    </svg>

    <!-- 主内容区 -->
    <div class="cover__content">
      <!-- 竖排标题（短标题） -->
      <div v-if="titleChars" class="cover__title-vertical">
        <span v-for="(ch, i) in titleChars" :key="i" class="v-char">{{ ch }}</span>
      </div>

      <!-- 横排标题（长标题） -->
      <div v-else class="cover__title-horizontal">
        <div v-for="(line, i) in titleLines" :key="i" class="h-line">{{ line }}</div>
      </div>

      <!-- 作者 -->
      <div class="cover__author" v-if="author">{{ author }}</div>
    </div>

    <!-- 底部出版社 -->
    <div class="cover__footer">
      <span class="cover__publisher">{{ shortPublisher }}</span>
    </div>
  </div>
</template>

<style scoped>
.cover {
  width: 100%;
  height: 100%;
  position: relative;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  box-sizing: border-box;
}

.cover__texture {
  position: absolute;
  inset: 0;
  background-image:
    url("data:image/svg+xml,%3Csvg width='80' height='80' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='80' height='80' filter='url(%23n)' opacity='0.04'/%3E%3C/svg%3E");
  pointer-events: none;
}

/* 书脊 */
.cover__spine {
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.15);
}

.spine__line {
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  width: 1px;
  opacity: 0.5;
}

/* 装饰线 */
.cover__top-line {
  position: absolute;
  top: 10%;
  left: 14%;
  right: 8%;
  height: 1px;
  opacity: 0.3;
}

.cover__bottom-line {
  position: absolute;
  bottom: 12%;
  left: 14%;
  right: 8%;
  height: 1px;
  opacity: 0.2;
}

/* SVG装饰 */
.cover__deco {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
}

/* 内容 */
.cover__content {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  padding: 20% 16% 12% 18%;
  position: relative;
  z-index: 1;
}

/* 竖排标题 */
.cover__title-vertical {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
}

.v-char {
  font-family: 'STKaiti', 'KaiTi', 'Noto Serif SC', 'SimSun', serif;
  font-size: 22px;
  font-weight: 700;
  color: rgba(255, 255, 255, 0.93);
  text-shadow: 0 1px 4px rgba(0, 0, 0, 0.2);
  letter-spacing: 0.1em;
  line-height: 1.3;
}

/* 横排标题 */
.cover__title-horizontal {
  text-align: center;
  max-width: 100%;
}

.h-line {
  font-family: 'STKaiti', 'KaiTi', 'Noto Serif SC', 'SimSun', serif;
  font-size: 16px;
  font-weight: 700;
  color: rgba(255, 255, 255, 0.93);
  text-shadow: 0 1px 4px rgba(0, 0, 0, 0.2);
  letter-spacing: 0.06em;
  line-height: 1.5;
}

/* 作者 */
.cover__author {
  margin-top: 16px;
  font-size: 11px;
  color: rgba(255, 255, 255, 0.5);
  text-align: center;
  letter-spacing: 0.08em;
  max-width: 100%;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

/* 出版社 */
.cover__footer {
  padding: 0 16% 8%;
  text-align: center;
  position: relative;
  z-index: 1;
}

.cover__publisher {
  font-size: 10px;
  color: rgba(255, 255, 255, 0.35);
  letter-spacing: 0.15em;
  font-family: var(--font-sans);
}
</style>
