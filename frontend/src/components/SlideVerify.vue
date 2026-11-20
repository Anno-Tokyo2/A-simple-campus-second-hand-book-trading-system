<script setup>
import { ref, onMounted } from 'vue'

const emit = defineEmits(['verified'])

const canvasRef = ref(null)
const sliderX = ref(0)
const isDragging = ref(false)
const startX = ref(0)
const verified = ref(false)
const canvasWidth = 320
const canvasHeight = 150
const blockSize = 38
const puzzleX = ref(0)
const tolerance = 12
let displayScale = 1

onMounted(() => {
  initCanvas()
})

function initCanvas() {
  const canvas = canvasRef.value
  if (!canvas) return
  const ctx = canvas.getContext('2d')

  // 计算 canvas 实际显示缩放比例
  const rect = canvas.getBoundingClientRect()
  displayScale = rect.width > 0 ? canvasWidth / rect.width : 1

  puzzleX.value = 60 + Math.floor(Math.random() * (canvasWidth - 120 - blockSize))

  // 暖色渐变背景
  const grad = ctx.createLinearGradient(0, 0, canvasWidth, canvasHeight)
  grad.addColorStop(0, '#F5E6D3')
  grad.addColorStop(0.5, '#EDD8C1')
  grad.addColorStop(1, '#E8D0B8')
  ctx.fillStyle = grad
  ctx.fillRect(0, 0, canvasWidth, canvasHeight)

  // 随机装饰元素
  for (let i = 0; i < 30; i++) {
    ctx.fillStyle = `rgba(196, 112, 63, ${Math.random() * 0.06 + 0.01})`
    ctx.beginPath()
    ctx.arc(
      Math.random() * canvasWidth,
      Math.random() * canvasHeight,
      Math.random() * 3 + 1, 0, Math.PI * 2
    )
    ctx.fill()
  }

  for (let i = 0; i < 5; i++) {
    ctx.strokeStyle = `rgba(184, 132, 92, ${Math.random() * 0.08 + 0.02})`
    ctx.lineWidth = 0.5
    ctx.beginPath()
    ctx.moveTo(Math.random() * canvasWidth, Math.random() * canvasHeight)
    ctx.lineTo(Math.random() * canvasWidth, Math.random() * canvasHeight)
    ctx.stroke()
  }

  // 拼图缺口
  const x = puzzleX.value
  const y = (canvasHeight - blockSize) / 2

  ctx.fillStyle = 'rgba(61, 43, 31, 0.12)'
  ctx.beginPath()
  ctx.rect(x, y, blockSize, blockSize)
  ctx.fill()

  ctx.strokeStyle = 'rgba(61, 43, 31, 0.15)'
  ctx.lineWidth = 1
  ctx.setLineDash([3, 2])
  ctx.strokeRect(x, y, blockSize, blockSize)
  ctx.setLineDash([])

  // 提示文字
  ctx.fillStyle = 'rgba(92, 64, 51, 0.5)'
  ctx.font = '13px "PingFang SC", "Microsoft YaHei", sans-serif'
  ctx.textAlign = 'center'
  ctx.fillText('拖动滑块至缺口位置', canvasWidth / 2, canvasHeight - 12)
}

function onDragStart(e) {
  if (verified.value) return
  isDragging.value = true
  startX.value = e.clientX || e.touches?.[0]?.clientX || 0

  // 每次拖动开始时重新计算缩放比例
  const canvas = canvasRef.value
  if (canvas) {
    const rect = canvas.getBoundingClientRect()
    displayScale = rect.width > 0 ? canvasWidth / rect.width : 1
  }

  document.addEventListener('mousemove', onDragMove)
  document.addEventListener('mouseup', onDragEnd)
  document.addEventListener('touchmove', onDragMove)
  document.addEventListener('touchend', onDragEnd)
}

function onDragMove(e) {
  if (!isDragging.value) return
  const clientX = e.clientX || e.touches?.[0]?.clientX || 0
  const diff = (clientX - startX.value) * displayScale
  sliderX.value = Math.max(0, Math.min(diff, canvasWidth - blockSize - 16))
}

function onDragEnd() {
  if (!isDragging.value) return
  isDragging.value = false
  document.removeEventListener('mousemove', onDragMove)
  document.removeEventListener('mouseup', onDragEnd)
  document.removeEventListener('touchmove', onDragMove)
  document.removeEventListener('touchend', onDragEnd)

  if (Math.abs(sliderX.value - puzzleX.value) <= tolerance) {
    verified.value = true
    emit('verified')
  } else {
    sliderX.value = 0
    initCanvas()
  }
}

const sliderStyle = () => ({
  left: (sliderX.value / displayScale) + 'px'
})
</script>

<template>
  <div class="verify-wrap">
    <div class="verify-canvas-area">
      <canvas ref="canvasRef" :width="canvasWidth" :height="canvasHeight" class="verify-canvas" />
      <div
        class="verify-slider"
        :class="{ dragging: isDragging, done: verified }"
        :style="{ left: (sliderX / (displayScale || 1)) + 'px' }"
        @mousedown="onDragStart"
        @touchstart.prevent="onDragStart"
      >
        <svg v-if="!verified" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
          <path d="M5 12h14M12 5l7 7-7 7"/>
        </svg>
        <svg v-else width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
          <path d="M20 6L9 17l-5-5"/>
        </svg>
      </div>
    </div>

    <div class="verify-track">
      <div class="verify-track-fill" :style="{ width: (sliderX / (displayScale || 1)) + 'px' }"></div>
    </div>

    <p v-if="verified" class="verify-msg success">验证通过</p>
    <p v-else class="verify-msg">请拖动滑块完成验证</p>
  </div>
</template>

<style scoped>
.verify-wrap {
  width: 100%;
  max-width: 320px;
}

.verify-canvas-area {
  position: relative;
  overflow: hidden;
  border-radius: 8px 3px 8px 3px;
  box-shadow: inset 0 1px 3px rgba(61, 43, 31, 0.08);
}

.verify-canvas {
  display: block;
  width: 100%;
}

.verify-slider {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  width: 42px;
  height: 42px;
  background: var(--orange-brown);
  border-radius: 4px 8px 4px 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  cursor: grab;
  transition: box-shadow 0.2s, background 0.2s;
  box-shadow: 0 2px 8px rgba(196, 112, 63, 0.3);
  z-index: 2;
}

.verify-slider:hover {
  box-shadow: 0 3px 12px rgba(196, 112, 63, 0.4);
}

.verify-slider.dragging {
  cursor: grabbing;
  box-shadow: 0 4px 16px rgba(196, 112, 63, 0.4);
  background: var(--orange-brown-dark);
}

.verify-slider.done {
  background: var(--sage-green);
  box-shadow: 0 2px 8px rgba(143, 166, 142, 0.3);
}

.verify-track {
  height: 4px;
  background: var(--warm-apricot-deep);
  border-radius: 2px;
  margin-top: 8px;
  overflow: hidden;
}

.verify-track-fill {
  height: 100%;
  background: linear-gradient(90deg, var(--dust-rose-muted), var(--orange-brown));
  border-radius: 2px;
  transition: width 0.05s linear;
}

.verify-msg {
  font-size: 12px;
  color: var(--ink-light);
  margin-top: 6px;
  text-align: center;
  letter-spacing: 0.05em;
}

.verify-msg.success {
  color: var(--sage-green);
}
</style>
