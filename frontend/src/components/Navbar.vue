<script setup>
import { useRouter, useRoute } from 'vue-router'
import { useUserStore } from '../stores/user'
import { ElMessageBox } from 'element-plus'
import { ref, computed } from 'vue'

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()
const mobileMenuOpen = ref(false)

const navLinks = [
  { path: '/', label: '首页' },
  { path: '/books', label: '书市' },
  { path: '/wantbuy', label: '求购' },
]

const activePath = computed(() => route.path)

async function handleLogout() {
  await ElMessageBox.confirm('确定退出登录？', '提示', { type: 'warning' })
  userStore.logout()
  router.push('/')
}

function go(path) {
  router.push(path)
  mobileMenuOpen.value = false
}
</script>

<template>
  <nav class="navbar wood-panel">
    <div class="navbar-inner">
      <!-- Logo - 书本造型 -->
      <div class="logo-area" @click="go('/')">
        <div class="logo-book">
          <div class="logo-book-spine"></div>
          <div class="logo-book-page"></div>
        </div>
        <div class="logo-text">
          <span class="logo-main">旧书集</span>
          <span class="logo-sub">Campus Book Exchange</span>
        </div>
      </div>

      <!-- 导航链接 - 非对称布局 -->
      <div class="nav-links" :class="{ open: mobileMenuOpen }">
        <a
          v-for="link in navLinks"
          :key="link.path"
          class="nav-link"
          :class="{ active: activePath === link.path }"
          @click="go(link.path)"
        >
          {{ link.label }}
        </a>
        <a
          v-if="userStore.isLoggedIn"
          class="nav-link"
          :class="{ active: activePath === '/publish' }"
          @click="go('/publish')"
        >
          发布
        </a>
      </div>

      <!-- 用户区域 -->
      <div class="user-area">
        <template v-if="userStore.isLoggedIn">
          <!-- 消息图标 -->
          <button class="icon-btn" @click="go('/messages')" title="消息">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
              <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
            </svg>
          </button>

          <!-- 用户头像下拉 -->
          <div class="user-dropdown">
            <div class="user-pill">
              <div class="user-avatar">
                {{ userStore.userInfo?.nickname?.[0] || '书' }}
              </div>
              <span class="user-name">{{ userStore.userInfo?.nickname || userStore.userInfo?.username }}</span>
              <span class="user-coins">
                <span class="coin-icon">◎</span>{{ userStore.userInfo?.coin_balance || 0 }}
              </span>
            </div>
            <div class="dropdown-menu">
              <a @click="go('/user')">个人中心</a>
              <a v-if="userStore.isAdmin" @click="go('/admin')">后台管理</a>
              <a class="logout-link" @click="handleLogout">退出登录</a>
            </div>
          </div>
        </template>

        <template v-else>
          <button class="btn-ghost" @click="go('/login')">登录</button>
          <button class="btn-warm" @click="go('/register')">注册</button>
        </template>

        <!-- 移动端菜单按钮 -->
        <button class="mobile-toggle" @click="mobileMenuOpen = !mobileMenuOpen">
          <span></span><span></span><span></span>
        </button>
      </div>
    </div>
  </nav>
</template>

<style scoped>
.navbar {
  position: sticky;
  top: 0;
  z-index: 100;
  padding: 0 24px;
  border-bottom: 1px solid rgba(139, 115, 85, 0.08);
}

.navbar-inner {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 64px;
  gap: 20px;
}

/* Logo - 书本造型 */
.logo-area {
  display: flex;
  align-items: center;
  gap: 12px;
  cursor: pointer;
  flex-shrink: 0;
}

.logo-book {
  position: relative;
  width: 28px;
  height: 32px;
}

.logo-book-spine {
  position: absolute;
  left: 0;
  top: 2px;
  width: 4px;
  height: 28px;
  background: var(--orange-brown);
  border-radius: 1px;
}

.logo-book-page {
  position: absolute;
  left: 5px;
  top: 0;
  width: 20px;
  height: 32px;
  background: var(--page-white);
  border-radius: 1px 4px 4px 1px;
  box-shadow: 1px 1px 3px rgba(61, 43, 31, 0.1);
}

.logo-book-page::after {
  content: '';
  position: absolute;
  right: 3px;
  top: 6px;
  width: 10px;
  height: 1.5px;
  background: var(--dust-rose-muted);
  box-shadow: 0 5px 0 var(--dust-rose-muted), 0 10px 0 var(--dust-rose-muted);
}

.logo-text {
  display: flex;
  flex-direction: column;
  line-height: 1.1;
}

.logo-main {
  font-family: var(--font-serif);
  font-size: 18px;
  font-weight: 600;
  color: var(--ink-dark);
  letter-spacing: 0.08em;
}

.logo-sub {
  font-size: 9px;
  color: var(--ink-faint);
  letter-spacing: 0.12em;
  text-transform: uppercase;
  margin-top: 1px;
}

/* 导航链接 */
.nav-links {
  display: flex;
  align-items: center;
  gap: 4px;
  flex: 1;
  justify-content: center;
}

.nav-link {
  padding: 8px 18px;
  font-size: 14px;
  color: var(--ink-medium);
  cursor: pointer;
  border-radius: 4px;
  transition: all 0.2s ease;
  letter-spacing: 0.06em;
  position: relative;
  user-select: none;
}

.nav-link:hover {
  color: var(--orange-brown);
  background: rgba(196, 112, 63, 0.04);
}

.nav-link.active {
  color: var(--orange-brown);
  font-weight: 500;
}

.nav-link.active::after {
  content: '';
  position: absolute;
  bottom: 2px;
  left: 50%;
  transform: translateX(-50%);
  width: 16px;
  height: 2px;
  background: var(--orange-brown);
  border-radius: 1px;
  opacity: 0.6;
}

/* 用户区域 */
.user-area {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-shrink: 0;
}

.icon-btn {
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: none;
  background: transparent;
  color: var(--ink-medium);
  cursor: pointer;
  border-radius: 6px;
  transition: all 0.2s;
}
.icon-btn:hover {
  color: var(--orange-brown);
  background: rgba(196, 112, 63, 0.06);
}

/* 用户下拉 */
.user-dropdown {
  position: relative;
}

.user-pill {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 5px 14px 5px 5px;
  background: var(--page-white);
  border-radius: 20px;
  cursor: pointer;
  transition: box-shadow 0.2s;
  box-shadow: 0 1px 3px rgba(61, 43, 31, 0.06);
}

.user-pill:hover {
  box-shadow: 0 2px 8px rgba(61, 43, 31, 0.1);
}

.user-avatar {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--orange-brown-light), var(--dust-rose));
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: 500;
}

.user-name {
  font-size: 13px;
  color: var(--ink-medium);
  max-width: 80px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.user-coins {
  font-size: 12px;
  color: var(--orange-brown);
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 2px;
}

.coin-icon {
  font-size: 14px;
  opacity: 0.7;
}

.dropdown-menu {
  position: absolute;
  top: calc(100% + 8px);
  right: 0;
  min-width: 140px;
  background: var(--page-white);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-hover);
  padding: 6px 0;
  opacity: 0;
  visibility: hidden;
  transform: translateY(-4px);
  transition: all 0.2s ease;
  z-index: 200;
}

.user-dropdown:hover .dropdown-menu {
  opacity: 1;
  visibility: visible;
  transform: translateY(0);
}

.dropdown-menu a {
  display: block;
  padding: 8px 16px;
  font-size: 13px;
  color: var(--ink-medium);
  cursor: pointer;
  transition: background 0.15s;
}

.dropdown-menu a:hover {
  background: var(--warm-apricot);
  color: var(--orange-brown);
}

.logout-link {
  border-top: 1px solid var(--warm-apricot);
  margin-top: 4px;
  padding-top: 10px !important;
  color: var(--ink-light) !important;
}

/* 移动端菜单 */
.mobile-toggle {
  display: none;
  flex-direction: column;
  gap: 4px;
  padding: 8px;
  background: none;
  border: none;
  cursor: pointer;
}
.mobile-toggle span {
  display: block;
  width: 18px;
  height: 1.5px;
  background: var(--ink-medium);
  border-radius: 1px;
  transition: all 0.2s;
}

@media (max-width: 768px) {
  .navbar {
    padding: 0 16px;
  }

  .nav-links {
    display: none;
    position: absolute;
    top: 64px;
    left: 0;
    right: 0;
    background: var(--warm-apricot-deep);
    flex-direction: column;
    padding: 12px;
    box-shadow: var(--shadow-card);
  }

  .nav-links.open {
    display: flex;
  }

  .mobile-toggle {
    display: flex;
  }

  .user-name {
    display: none;
  }

  .logo-sub {
    display: none;
  }
}
</style>
