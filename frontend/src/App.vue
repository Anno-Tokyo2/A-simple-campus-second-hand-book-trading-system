<script setup>
import { RouterView, useRoute } from 'vue-router'
import { computed } from 'vue'
import Navbar from './components/Navbar.vue'

const route = useRoute()
const isFullWidth = computed(() => ['/', '/books'].includes(route.path))
</script>

<template>
  <div class="app-shell">
    <!-- 顶部装饰条 - 模拟书页边缘 -->
    <div class="top-deco-strip"></div>

    <Navbar />

    <main
      class="main-content"
      :class="{ 'full-width': isFullWidth }"
    >
      <RouterView v-slot="{ Component }">
        <transition name="page-fade" mode="out-in">
          <component :is="Component" :key="route.path" />
        </transition>
      </RouterView>
    </main>

    <!-- 底部 -->
    <footer class="site-footer">
      <div class="footer-inner">
        <div class="footer-spine"></div>
        <p class="footer-text">校园二手书交易平台 · 让闲置书籍重获新生</p>
        <p class="footer-sub">用书币连接每一本被珍视的书</p>
      </div>
    </footer>
  </div>
</template>

<style scoped>
.app-shell {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.top-deco-strip {
  height: 3px;
  background: linear-gradient(
    90deg,
    transparent 0%,
    var(--dust-rose-muted) 15%,
    var(--orange-brown) 50%,
    var(--dust-rose-muted) 85%,
    transparent 100%
  );
  opacity: 0.5;
}

.main-content {
  flex: 1;
  max-width: 1160px;
  width: 100%;
  margin: 0 auto;
  padding: 28px 32px 60px;
}

.main-content.full-width {
  max-width: 1280px;
  padding: 28px 32px 60px;
}

/* 页面切换 */
.page-fade-enter-active {
  transition: opacity 0.35s ease, transform 0.35s ease;
}
.page-fade-leave-active {
  transition: opacity 0.15s ease;
  position: absolute;
  width: 100%;
}
.page-fade-enter-from {
  opacity: 0;
  transform: translateY(8px);
}
.page-fade-leave-to {
  opacity: 0;
}

/* 底部 */
.site-footer {
  margin-top: auto;
  padding: 40px 24px 32px;
  background: var(--warm-apricot-deep);
  position: relative;
}

.site-footer::before {
  content: '';
  position: absolute;
  top: 0;
  left: 10%;
  right: 10%;
  height: 1px;
  background: linear-gradient(
    90deg,
    transparent,
    var(--dust-rose-muted),
    transparent
  );
}

.footer-inner {
  max-width: 600px;
  margin: 0 auto;
  text-align: center;
  position: relative;
}

.footer-spine {
  width: 1px;
  height: 24px;
  background: var(--orange-brown);
  margin: 0 auto 16px;
  opacity: 0.4;
}

.footer-text {
  font-family: var(--font-serif);
  font-size: 14px;
  color: var(--ink-medium);
  letter-spacing: 0.15em;
}

.footer-sub {
  font-size: 12px;
  color: var(--ink-faint);
  margin-top: 6px;
  letter-spacing: 0.1em;
}

@media (max-width: 768px) {
  .main-content {
    padding: 20px 16px 40px;
  }
}
</style>
