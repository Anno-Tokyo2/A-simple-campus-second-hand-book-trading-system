<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '../stores/user'
import { ElMessage } from 'element-plus'
import SlideVerify from '../components/SlideVerify.vue'

const router = useRouter()
const userStore = useUserStore()

const form = ref({
  username: '', password: '', confirmPassword: '', nickname: '', school: ''
})
const loading = ref(false)
const verified = ref(false)

async function handleRegister() {
  if (!verified.value) { ElMessage.warning('请先完成人机验证'); return }
  if (!form.value.username || !form.value.password) { ElMessage.warning('请填写必填项'); return }
  if (form.value.password !== form.value.confirmPassword) { ElMessage.warning('两次密码不一致'); return }
  if (form.value.password.length < 6) { ElMessage.warning('密码至少6位'); return }
  loading.value = true
  try {
    await userStore.register({
      username: form.value.username,
      password: form.value.password,
      nickname: form.value.nickname || form.value.username,
      school: form.value.school
    })
    ElMessage.success('注册成功，请登录')
    router.push('/login')
  } catch {} finally { loading.value = false }
}
</script>

<template>
  <div class="auth-page">
    <div class="auth-layout">
      <!-- 左侧装饰 -->
      <div class="auth-deco wood-panel">
        <div class="auth-deco-inner">
          <div class="deco-icon-stack">
            <div class="deco-book-a"></div>
            <div class="deco-book-b"></div>
            <div class="deco-pencil"></div>
          </div>
          <h2 class="deco-title">加入我们</h2>
          <p class="deco-text">成为校园书市的一员，开始你的书籍交换之旅</p>
        </div>
      </div>

      <!-- 右侧表单 -->
      <div class="auth-form-area">
        <div class="auth-form-inner">
          <h1 class="auth-heading">注册</h1>
          <p class="auth-subheading">创建账号即可发布和购买书籍</p>

          <form @submit.prevent="handleRegister" class="auth-form">
            <div class="field-group">
              <label class="field-label">用户名 *</label>
              <input v-model="form.username" type="text" class="field-input" placeholder="请输入用户名" />
            </div>

            <div class="field-row">
              <div class="field-group">
                <label class="field-label">密码 *</label>
                <input v-model="form.password" type="password" class="field-input" placeholder="至少6位" />
              </div>
              <div class="field-group">
                <label class="field-label">确认密码 *</label>
                <input v-model="form.confirmPassword" type="password" class="field-input" placeholder="再次输入" />
              </div>
            </div>

            <div class="field-row">
              <div class="field-group">
                <label class="field-label">昵称</label>
                <input v-model="form.nickname" type="text" class="field-input" placeholder="选填" />
              </div>
              <div class="field-group">
                <label class="field-label">学院</label>
                <input v-model="form.school" type="text" class="field-input" placeholder="选填" />
              </div>
            </div>

            <div class="field-group">
              <label class="field-label">人机验证</label>
              <SlideVerify @verified="verified = true" />
            </div>

            <button type="submit" class="btn-warm auth-submit" :disabled="loading">
              {{ loading ? '注册中...' : '注 册' }}
            </button>
          </form>

          <p class="auth-switch">
            已有账号？<router-link to="/login">去登录</router-link>
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
  max-width: 880px;
  min-height: 560px;
  border-radius: 4px 16px 4px 16px;
  overflow: hidden;
  box-shadow: var(--shadow-hover);
}

.auth-deco {
  flex: 0 0 300px;
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

.auth-deco-inner { text-align: center; }

/* 装饰图标 */
.deco-icon-stack {
  position: relative;
  width: 60px;
  height: 70px;
  margin: 0 auto 28px;
}

.deco-book-a {
  position: absolute;
  bottom: 0;
  left: 5px;
  width: 36px;
  height: 50px;
  background: linear-gradient(135deg, var(--sage-green), var(--sage-light));
  border-radius: 2px 6px 6px 2px;
  transform: rotate(-5deg);
  box-shadow: 2px 2px 6px rgba(0,0,0,0.08);
}

.deco-book-b {
  position: absolute;
  bottom: 5px;
  left: 18px;
  width: 34px;
  height: 48px;
  background: linear-gradient(135deg, var(--orange-brown), var(--dust-rose));
  border-radius: 2px 5px 5px 2px;
  transform: rotate(3deg);
  box-shadow: 2px 2px 6px rgba(0,0,0,0.08);
}

.deco-pencil {
  position: absolute;
  top: 0;
  right: 8px;
  width: 3px;
  height: 40px;
  background: linear-gradient(to bottom, var(--orange-brown-light), var(--orange-brown));
  border-radius: 1px;
  transform: rotate(15deg);
}
.deco-pencil::before {
  content: '';
  position: absolute;
  top: -4px;
  left: -1px;
  width: 5px;
  height: 5px;
  background: var(--dust-rose);
  border-radius: 50%;
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

/* 表单区 */
.auth-form-area {
  flex: 1;
  background: var(--page-white);
  padding: 40px 36px;
  display: flex;
  align-items: center;
  overflow-y: auto;
}

.auth-form-inner {
  width: 100%;
  max-width: 420px;
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
  margin-bottom: 28px;
}

.auth-form {
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.field-group {
  display: flex;
  flex-direction: column;
  gap: 5px;
  flex: 1;
}

.field-row {
  display: flex;
  gap: 14px;
}

.field-label {
  font-size: 13px;
  font-weight: 500;
  color: var(--ink-medium);
}

.field-input {
  padding: 9px 12px;
  border: 1.5px solid var(--warm-apricot-deep);
  border-radius: 5px;
  font-size: 14px;
  font-family: var(--font-sans);
  color: var(--ink-dark);
  background: var(--warm-cream);
  transition: border-color 0.2s, box-shadow 0.2s;
  outline: none;
}

.field-input::placeholder { color: var(--ink-faint); }

.field-input:focus {
  border-color: var(--orange-brown-light);
  box-shadow: 0 0 0 3px rgba(196, 112, 63, 0.08);
  background: var(--page-white);
}

.auth-submit {
  width: 100%;
  padding: 12px;
  font-size: 15px;
  margin-top: 4px;
}

.auth-submit:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.auth-switch {
  text-align: center;
  font-size: 13px;
  color: var(--ink-light);
  margin-top: 20px;
}

.auth-switch a {
  color: var(--orange-brown);
  font-weight: 500;
}

@media (max-width: 768px) {
  .auth-layout {
    flex-direction: column;
    max-width: 420px;
    min-height: auto;
  }

  .auth-deco {
    flex: none;
    padding: 28px 24px;
  }

  .auth-deco::after { display: none; }

  .auth-form-area { padding: 28px 20px; }

  .field-row {
    flex-direction: column;
    gap: 14px;
  }
}
</style>
