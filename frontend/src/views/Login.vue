<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '../stores/user'
import { ElMessage } from 'element-plus'
import SlideVerify from '../components/SlideVerify.vue'

const router = useRouter()
const userStore = useUserStore()

const form = ref({ username: '', password: '' })
const loading = ref(false)
const verified = ref(false)

async function handleLogin() {
  if (!verified.value) {
    ElMessage.warning('请先完成人机验证')
    return
  }
  if (!form.value.username || !form.value.password) {
    ElMessage.warning('请输入用户名和密码')
    return
  }
  loading.value = true
  try {
    await userStore.login(form.value.username, form.value.password)
    ElMessage.success('登录成功')
    router.push('/')
  } catch (err) {
    const msg = err.response?.data?.detail || '登录失败，请稍后重试'
    ElMessage.error(msg)
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="auth-page">
    <div class="auth-layout">
      <!-- 左侧装饰面板 -->
      <div class="auth-deco wood-panel">
        <div class="auth-deco-inner">
          <div class="deco-book-icon">
            <div class="deco-book-cover"></div>
            <div class="deco-book-page1"></div>
            <div class="deco-book-page2"></div>
          </div>
          <h2 class="deco-title">欢迎回来</h2>
          <p class="deco-text">你的书架上，有新的故事在等你</p>
          <div class="deco-dots">
            <span></span><span></span><span></span>
          </div>
        </div>
      </div>

      <!-- 右侧表单 -->
      <div class="auth-form-area">
        <div class="auth-form-inner">
          <h1 class="auth-heading">登录</h1>
          <p class="auth-subheading">输入你的账号继续浏览书市</p>

          <form @submit.prevent="handleLogin" class="auth-form">
            <div class="field-group">
              <label class="field-label">用户名</label>
              <input
                v-model="form.username"
                type="text"
                class="field-input"
                placeholder="请输入用户名"
                autocomplete="username"
              />
            </div>

            <div class="field-group">
              <label class="field-label">密码</label>
              <input
                v-model="form.password"
                type="password"
                class="field-input"
                placeholder="请输入密码"
                autocomplete="current-password"
              />
            </div>

            <div class="field-group">
              <label class="field-label">人机验证</label>
              <SlideVerify @verified="verified = true" />
            </div>

            <button
              type="submit"
              class="btn-warm auth-submit"
              :disabled="loading"
            >
              {{ loading ? '登录中...' : '登 录' }}
            </button>
          </form>

          <p class="auth-switch">
            还没有账号？
            <router-link to="/register">立即注册</router-link>
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.auth-page {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: calc(100vh - 200px);
  padding: 20px;
}

.auth-layout {
  display: flex;
  width: 100%;
  max-width: 820px;
  min-height: 520px;
  border-radius: 16px 4px 16px 4px;
  overflow: hidden;
  box-shadow: var(--shadow-hover);
}

/* 左侧装饰 */
.auth-deco {
  flex: 0 0 340px;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px;
  position: relative;
}

.auth-deco::after {
  content: '';
  position: absolute;
  right: 0;
  top: 10%;
  bottom: 10%;
  width: 1px;
  background: linear-gradient(to bottom, transparent, var(--dust-rose-muted), transparent);
}

.auth-deco-inner {
  text-align: center;
}

/* CSS 书本装饰 */
.deco-book-icon {
  position: relative;
  width: 60px;
  height: 72px;
  margin: 0 auto 28px;
}

.deco-book-cover {
  position: absolute;
  left: 0;
  top: 0;
  width: 44px;
  height: 72px;
  background: linear-gradient(135deg, var(--orange-brown), var(--orange-brown-light));
  border-radius: 2px 6px 6px 2px;
  box-shadow: 2px 2px 8px rgba(196, 112, 63, 0.2);
}

.deco-book-page1 {
  position: absolute;
  left: 6px;
  top: 4px;
  width: 42px;
  height: 64px;
  background: var(--page-white);
  border-radius: 1px 4px 4px 1px;
}

.deco-book-page2 {
  position: absolute;
  left: 10px;
  top: 8px;
  width: 40px;
  height: 60px;
  background: var(--warm-apricot);
  border-radius: 1px 3px 3px 1px;
}

.deco-title {
  font-family: var(--font-serif);
  font-size: 22px;
  color: var(--ink-dark);
  margin-bottom: 10px;
  letter-spacing: 0.08em;
}

.deco-text {
  font-size: 13px;
  color: var(--ink-light);
  line-height: 1.6;
}

.deco-dots {
  display: flex;
  justify-content: center;
  gap: 6px;
  margin-top: 24px;
}

.deco-dots span {
  width: 4px;
  height: 4px;
  border-radius: 50%;
  background: var(--dust-rose-muted);
}

/* 右侧表单 */
.auth-form-area {
  flex: 1;
  background: var(--page-white);
  padding: 48px 40px;
  display: flex;
  align-items: center;
}

.auth-form-inner {
  width: 100%;
  max-width: 320px;
  margin: 0 auto;
}

.auth-heading {
  font-family: var(--font-serif);
  font-size: 26px;
  font-weight: 600;
  color: var(--ink-dark);
  margin-bottom: 6px;
}

.auth-subheading {
  font-size: 13px;
  color: var(--ink-light);
  margin-bottom: 32px;
}

.auth-form {
  display: flex;
  flex-direction: column;
  gap: 22px;
}

.field-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.field-label {
  font-size: 13px;
  font-weight: 500;
  color: var(--ink-medium);
  letter-spacing: 0.05em;
}

.field-input {
  padding: 10px 14px;
  border: 1.5px solid var(--warm-apricot-deep);
  border-radius: 6px;
  font-size: 14px;
  font-family: var(--font-sans);
  color: var(--ink-dark);
  background: var(--warm-cream);
  transition: border-color 0.2s, box-shadow 0.2s;
  outline: none;
}

.field-input::placeholder {
  color: var(--ink-faint);
}

.field-input:focus {
  border-color: var(--orange-brown-light);
  box-shadow: 0 0 0 3px rgba(196, 112, 63, 0.08);
  background: var(--page-white);
}

.auth-submit {
  width: 100%;
  padding: 12px;
  font-size: 15px;
  margin-top: 8px;
}

.auth-submit:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.auth-switch {
  text-align: center;
  font-size: 13px;
  color: var(--ink-light);
  margin-top: 24px;
}

.auth-switch a {
  color: var(--orange-brown);
  font-weight: 500;
}

@media (max-width: 768px) {
  .auth-layout {
    flex-direction: column;
    max-width: 420px;
  }

  .auth-deco {
    flex: none;
    padding: 32px 24px;
  }

  .auth-deco::after {
    display: none;
  }

  .auth-form-area {
    padding: 32px 24px;
  }
}
</style>
