<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '../stores/user'
import { ElMessage } from 'element-plus'
import api from '../api'

const router = useRouter()
const userStore = useUserStore()
const wantBuys = ref([])
const loading = ref(true)
const showDialog = ref(false)
const form = ref({ title: '', author: '', isbn: '', expected_price: null, description: '' })
const respondDialog = ref(false)
const respondForm = ref({ message: '', price: null })
const respondTarget = ref(null)

const demoWantBuys = [
  { id: 1, title: '机器学习', author: '周志华', isbn: '9787302423287', expected_price: 25, description: '希望是西瓜书，版次不限', user: { nickname: '王同学', school: '计算机学院' }, created_at: '2025-06-15', status: 'open' },
  { id: 2, title: '深入理解计算机系统', author: 'Randal E. Bryant', isbn: '', expected_price: 35, description: '英文原版或中文翻译版均可', user: { nickname: '李同学', school: '软件学院' }, created_at: '2025-06-14', status: 'open' },
  { id: 3, title: '算法导论', author: 'Thomas H. Cormen', isbn: '9787111407010', expected_price: 30, description: '第三版优先', user: { nickname: '赵同学', school: '数学学院' }, created_at: '2025-06-13', status: 'open' },
  { id: 4, title: '经济学原理', author: '曼昆', isbn: '', expected_price: 20, description: '微观经济学分册', user: { nickname: '陈同学', school: '经济学院' }, created_at: '2025-06-12', status: 'matched' }
]

onMounted(async () => {
  try { const r = await api.get('/api/wantbuys'); wantBuys.value = r.data.items || demoWantBuys }
  catch { wantBuys.value = demoWantBuys }
  finally { loading.value = false }
})

async function submitWantBuy() {
  if (!form.value.title) { ElMessage.warning('请填写书名'); return }
  try {
    await api.post('/api/wantbuys', form.value)
    ElMessage.success('发布成功')
    showDialog.value = false
    form.value = { title: '', author: '', isbn: '', expected_price: null, description: '' }
  } catch {}
}

function openPublish() {
  if (!userStore.isLoggedIn) { ElMessage.warning('请先登录'); router.push('/login'); return }
  showDialog.value = true
}

function openRespond(item) {
  if (!userStore.isLoggedIn) { ElMessage.warning('请先登录'); router.push('/login'); return }
  if (item.user?.id === userStore.userInfo?.id) { ElMessage.warning('不能回应自己的求购'); return }
  respondTarget.value = item
  respondForm.value = { message: '', price: null }
  respondDialog.value = true
}

async function submitRespond() {
  if (!respondTarget.value) return
  try {
    await api.post(`/api/wantbuys/${respondTarget.value.id}/respond`, respondForm.value)
    ElMessage.success('回应已发送，求购者会收到你的消息')
    respondDialog.value = false
  } catch {}
}

function daysAgo(dateStr) {
  const d = new Date(dateStr)
  const now = new Date()
  const diff = Math.floor((now - d) / 86400000)
  if (diff === 0) return '今天'
  if (diff === 1) return '昨天'
  return `${diff}天前`
}
</script>

<template>
  <div class="wantbuy-page">
    <!-- 头部 -->
    <header class="wb-header">
      <div class="wb-header__left">
        <h1 class="wb-title">求购广场</h1>
        <p class="wb-sub">找不到的书，让同学帮你留意</p>
      </div>
      <button class="btn-warm" @click="openPublish">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="margin-right: 6px">
          <line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/>
        </svg>
        发布求购
      </button>
    </header>

    <!-- 求购列表 - 时间线式布局 -->
    <div class="wb-list" v-loading="loading">
      <div v-if="wantBuys.length === 0" class="wb-empty">
        <p>暂无求购信息</p>
      </div>

      <div v-else class="timeline">
        <div
          v-for="item in wantBuys"
          :key="item.id"
          class="timeline-item"
        >
          <!-- 时间线装饰 -->
          <div class="timeline-dot" :class="item.status"></div>
          <div class="timeline-line"></div>

          <!-- 内容卡片 -->
          <div class="wb-card">
            <div class="wb-card__head">
              <h3 class="wb-card__title">{{ item.title }}</h3>
              <span class="wb-card__status" :class="item.status">
                {{ item.status === 'open' ? '求购中' : item.status === 'matched' ? '已找到' : '已关闭' }}
              </span>
            </div>

            <div class="wb-card__meta">
              <span v-if="item.author">作者：{{ item.author }}</span>
              <span v-if="item.isbn">ISBN：{{ item.isbn }}</span>
            </div>

            <p v-if="item.description" class="wb-card__desc">{{ item.description }}</p>

            <div class="wb-card__footer">
              <div class="wb-card__user">
                <div class="wb-user-avatar">{{ item.user?.nickname?.[0] || '同' }}</div>
                <div>
                  <span class="wb-user-name">{{ item.user?.nickname }}</span>
                  <span class="wb-user-school">{{ item.user?.school }}</span>
                </div>
              </div>

              <div class="wb-card__right">
                <span v-if="item.expected_price" class="wb-price">◎{{ item.expected_price }}</span>
                <span class="wb-time">{{ daysAgo(item.created_at) }}</span>
                <button
                  v-if="item.status === 'open' && item.user?.id !== userStore.userInfo?.id"
                  class="btn-warm respond-btn"
                  @click.stop="openRespond(item)"
                >
                  我有这本书
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 发布弹窗 -->
    <el-dialog v-model="showDialog" title="发布求购" width="480px">
      <div class="dialog-form">
        <div class="field-group">
          <label class="field-label">书名 *</label>
          <input v-model="form.title" class="field-input" placeholder="想购买什么书？" />
        </div>
        <div class="field-row">
          <div class="field-group">
            <label class="field-label">作者</label>
            <input v-model="form.author" class="field-input" placeholder="选填" />
          </div>
          <div class="field-group">
            <label class="field-label">ISBN</label>
            <input v-model="form.isbn" class="field-input" placeholder="选填" />
          </div>
        </div>
        <div class="field-group">
          <label class="field-label">预期价格（书币）</label>
          <input v-model.number="form.expected_price" type="number" class="field-input" placeholder="0" />
        </div>
        <div class="field-group">
          <label class="field-label">补充说明</label>
          <textarea v-model="form.description" class="field-textarea" placeholder="如版本要求、成色要求等" rows="3"></textarea>
        </div>
      </div>
      <template #footer>
        <button class="btn-ghost" @click="showDialog = false">取消</button>
        <button class="btn-warm" @click="submitWantBuy" style="margin-left: 8px">发布</button>
      </template>
    </el-dialog>

    <!-- 回应求购弹窗 -->
    <el-dialog v-model="respondDialog" title="回应求购" width="460px">
      <p class="respond-hint" v-if="respondTarget">
        向 <strong>{{ respondTarget.user?.nickname }}</strong> 回应《{{ respondTarget.title }}》
      </p>
      <div class="dialog-form">
        <div class="field-group">
          <label class="field-label">你的售价（书币）</label>
          <input v-model.number="respondForm.price" type="number" class="field-input" placeholder="输入你希望的价格" />
        </div>
        <div class="field-group">
          <label class="field-label">留言</label>
          <textarea v-model="respondForm.message" class="field-textarea" placeholder="介绍一下书的成色、版次等..." rows="3"></textarea>
        </div>
      </div>
      <template #footer>
        <button class="btn-ghost" @click="respondDialog = false">取消</button>
        <button class="btn-warm" @click="submitRespond" style="margin-left: 8px">发送回应</button>
      </template>
    </el-dialog>
  </div>
</template>

<style scoped>
.wantbuy-page {
  max-width: 800px;
  margin: 0 auto;
}

.wb-header {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  margin-bottom: 36px;
  padding: 16px 0;
}

.wb-title {
  font-family: var(--font-serif);
  font-size: 26px;
  font-weight: 600;
  color: var(--ink-dark);
}

.wb-sub {
  font-size: 13px;
  color: var(--ink-light);
  margin-top: 4px;
}

/* 时间线 */
.timeline {
  position: relative;
  padding-left: 32px;
}

.timeline-item {
  position: relative;
  margin-bottom: 20px;
}

.timeline-dot {
  position: absolute;
  left: -28px;
  top: 24px;
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: var(--dust-rose-muted);
  border: 2px solid var(--warm-apricot);
  z-index: 1;
}

.timeline-dot.open {
  background: var(--orange-brown);
  box-shadow: 0 0 0 3px rgba(196, 112, 63, 0.15);
}

.timeline-dot.matched {
  background: var(--sage-green);
}

.timeline-line {
  position: absolute;
  left: -24px;
  top: 36px;
  bottom: -20px;
  width: 1px;
  background: var(--warm-apricot-deep);
}

.timeline-item:last-child .timeline-line {
  display: none;
}

/* 卡片 */
.wb-card {
  background: var(--page-white);
  padding: 20px 24px;
  border-radius: 8px 3px 8px 3px;
  box-shadow: var(--shadow-soft);
  transition: box-shadow 0.2s;
}

.wb-card:hover {
  box-shadow: var(--shadow-card);
}

.wb-card__head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 10px;
}

.wb-card__title {
  font-family: var(--font-serif);
  font-size: 17px;
  font-weight: 500;
  color: var(--ink-dark);
}

.wb-card__status {
  font-size: 12px;
  padding: 3px 12px;
  border-radius: 12px;
}

.wb-card__status.open {
  color: var(--orange-brown);
  background: rgba(196, 112, 63, 0.08);
}

.wb-card__status.matched {
  color: var(--sage-green);
  background: rgba(143, 166, 142, 0.1);
}

.wb-card__status.closed {
  color: var(--ink-faint);
  background: rgba(139, 115, 85, 0.08);
}

.wb-card__meta {
  display: flex;
  gap: 20px;
  font-size: 13px;
  color: var(--ink-light);
  margin-bottom: 8px;
}

.wb-card__desc {
  font-size: 13px;
  color: var(--ink-medium);
  line-height: 1.6;
  margin-bottom: 14px;
  padding: 10px 14px;
  background: var(--warm-cream);
  border-radius: 4px;
  border-left: 3px solid var(--warm-apricot-deep);
}

.wb-card__footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.wb-card__user {
  display: flex;
  align-items: center;
  gap: 10px;
}

.wb-user-avatar {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--sage-light), var(--sage-green));
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-family: var(--font-serif);
}

.wb-user-name {
  font-size: 13px;
  font-weight: 500;
  color: var(--ink-dark);
  display: block;
}

.wb-user-school {
  font-size: 11px;
  color: var(--ink-faint);
}

.wb-card__right {
  display: flex;
  align-items: center;
  gap: 14px;
}

.wb-price {
  font-family: var(--font-serif);
  font-size: 18px;
  font-weight: 600;
  color: var(--orange-brown);
}

.wb-time {
  font-size: 12px;
  color: var(--ink-faint);
}

.wb-empty {
  text-align: center;
  padding: 60px;
  color: var(--ink-faint);
}

/* 弹窗表单 */
.dialog-form {
  display: flex;
  flex-direction: column;
  gap: 16px;
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
  outline: none;
  transition: border-color 0.2s;
}

.field-input:focus {
  border-color: var(--orange-brown-light);
  background: var(--page-white);
}

.field-textarea {
  padding: 10px 12px;
  border: 1.5px solid var(--warm-apricot-deep);
  border-radius: 6px;
  font-size: 14px;
  font-family: var(--font-sans);
  color: var(--ink-dark);
  background: var(--warm-cream);
  outline: none;
  resize: vertical;
  line-height: 1.6;
}

.field-textarea:focus {
  border-color: var(--orange-brown-light);
  background: var(--page-white);
}

@media (max-width: 600px) {
  .wb-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }

  .timeline {
    padding-left: 24px;
  }

  .field-row {
    flex-direction: column;
  }
}

.respond-btn {
  padding: 6px 16px;
  font-size: 13px;
  white-space: nowrap;
}

.respond-hint {
  font-size: 14px;
  color: var(--ink-medium);
  margin-bottom: 16px;
  line-height: 1.6;
}
</style>
