<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import api from '../api'

const router = useRouter()
const loading = ref(false)
const isbnLoading = ref(false)
const fileList = ref([])

const form = reactive({
  title: '', author: '', publisher: '', isbn: '',
  price: null, original_price: null,
  condition: '九成新', category: '', description: ''
})

const conditions = ['九五新', '九成新', '八成新', '七成新', '六成新及以下']
const categories = ['数学', '计算机', '英语', '经济', '物理', '政治', '文学', '其他']

async function queryISBN() {
  if (!form.isbn) return
  isbnLoading.value = true
  try {
    const res = await api.get(`/api/books/isbn/${form.isbn}`)
    Object.assign(form, res.data)
    ElMessage.success('ISBN 信息已填充')
  } catch {
    const mockData = {
      '9787040396638': { title: '高等数学（第七版）上册', author: '同济大学数学系', publisher: '高等教育出版社' },
      '9787040396645': { title: '高等数学（第七版）下册', author: '同济大学数学系', publisher: '高等教育出版社' },
      '9787302334569': { title: '数据结构（C语言版）', author: '严蔚敏', publisher: '清华大学出版社' }
    }
    const data = mockData[form.isbn.replace(/-/g, '')]
    if (data) {
      Object.assign(form, data)
      ElMessage.success('已从本地缓存填充')
    } else {
      ElMessage.info('未找到 ISBN 信息，请手动填写')
    }
  } finally { isbnLoading.value = false }
}

function beforeUpload(file) {
  const ok = file.type.startsWith('image/') && file.size / 1024 / 1024 < 5
  if (!ok) ElMessage.error('请上传小于5MB的图片')
  return ok
}

async function handleSubmit() {
  if (!form.title) { ElMessage.warning('请填写书名'); return }
  if (!form.author) { ElMessage.warning('请填写作者'); return }
  if (!form.publisher) { ElMessage.warning('请填写出版社'); return }
  if (!form.price) { ElMessage.warning('请填写售价'); return }
  if (!form.category) { ElMessage.warning('请选择分类'); return }
  if (fileList.value.length === 0) { ElMessage.warning('请上传封面图片'); return }
  loading.value = true
  try {
    const fd = new FormData()
    Object.keys(form).forEach(k => {
      if (form[k] !== null && form[k] !== '') fd.append(k, form[k])
    })
    // 只取第一张图片作为封面
    if (fileList.value.length > 0 && fileList.value[0].raw) {
      fd.append('cover', fileList.value[0].raw)
    }
    await api.post('/api/books', fd)
    ElMessage.success('发布成功！')
    router.push('/books')
  } catch (err) {
    ElMessage.error(err.response?.data?.detail || '发布失败，请稍后重试')
  } finally { loading.value = false }
}
</script>

<template>
  <div class="publish-page">
    <!-- 页面头部 -->
    <header class="publish-header">
      <div class="header-deco">
        <div class="deco-stroke"></div>
      </div>
      <div class="header-text">
        <h1 class="publish-title">发布书籍</h1>
        <p class="publish-sub">让你的闲置书籍找到下一位读者</p>
      </div>
    </header>

    <div class="publish-body">
      <!-- 左侧：ISBN 快速填充提示 -->
      <aside class="publish-sidebar">
        <div class="sidebar-card">
          <div class="sidebar-icon">ISBN</div>
          <h3 class="sidebar-title">快速填充</h3>
          <p class="sidebar-desc">输入书籍 ISBN 号，自动获取书名、作者、出版社等信息</p>
          <div class="isbn-input-group">
            <input
              v-model="form.isbn"
              type="text"
              class="isbn-input"
              placeholder="输入 ISBN 号..."
              @keyup.enter="queryISBN"
            />
            <button class="btn-warm isbn-btn" :loading="isbnLoading" @click="queryISBN">
              {{ isbnLoading ? '查询中...' : '查询' }}
            </button>
          </div>
        </div>

        <div class="sidebar-tips">
          <h4 class="tips-title">发布提示</h4>
          <ul class="tips-list">
            <li>如实描述书籍成色</li>
            <li>上传实物图片更容易售出</li>
            <li>合理定价有助于快速交易</li>
            <li>书籍一经售出不可撤回</li>
          </ul>
        </div>
      </aside>

      <!-- 右侧：表单 -->
      <div class="publish-form-area">
        <form @submit.prevent="handleSubmit" class="publish-form">
          <!-- 基本信息 -->
          <div class="form-section">
            <h3 class="section-label">基本信息</h3>
            <div class="field-group full">
              <label class="field-label">书名 *</label>
              <input v-model="form.title" type="text" class="field-input" placeholder="请输入书名" />
            </div>
            <div class="field-row">
              <div class="field-group">
                <label class="field-label">作者</label>
                <input v-model="form.author" type="text" class="field-input" placeholder="请输入作者" />
              </div>
              <div class="field-group">
                <label class="field-label">出版社</label>
                <input v-model="form.publisher" type="text" class="field-input" placeholder="请输入出版社" />
              </div>
            </div>
          </div>

          <!-- 价格与成色 -->
          <div class="form-section">
            <h3 class="section-label">价格与成色</h3>
            <div class="field-row three">
              <div class="field-group">
                <label class="field-label">售价（书币）*</label>
                <input v-model.number="form.price" type="number" class="field-input" placeholder="0" min="1" />
              </div>
              <div class="field-group">
                <label class="field-label">原价（元）</label>
                <input v-model.number="form.original_price" type="number" class="field-input" placeholder="0" />
              </div>
              <div class="field-group">
                <label class="field-label">成色</label>
                <select v-model="form.condition" class="field-input">
                  <option v-for="c in conditions" :key="c" :value="c">{{ c }}</option>
                </select>
              </div>
            </div>
            <div class="field-group full">
              <label class="field-label">分类</label>
              <div class="category-pills">
                <button
                  v-for="c in categories"
                  :key="c"
                  type="button"
                  class="cat-pill"
                  :class="{ active: form.category === c }"
                  @click="form.category = c"
                >
                  {{ c }}
                </button>
              </div>
            </div>
          </div>

          <!-- 描述与图片 -->
          <div class="form-section">
            <h3 class="section-label">描述与图片</h3>
            <div class="field-group full">
              <label class="field-label">书籍描述</label>
              <textarea v-model="form.description" class="field-textarea" placeholder="描述书籍的使用情况、笔记标注等..." rows="4"></textarea>
            </div>
            <div class="field-group full">
              <label class="field-label">成色图片（最多5张）</label>
              <el-upload
                v-model:file-list="fileList"
                action="#"
                list-type="picture-card"
                :auto-upload="false"
                :before-upload="beforeUpload"
                :limit="5"
              >
                <div class="upload-add">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                    <line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/>
                  </svg>
                </div>
              </el-upload>
            </div>
          </div>

          <button type="submit" class="btn-warm submit-btn" :disabled="loading">
            {{ loading ? '发布中...' : '确认发布' }}
          </button>
        </form>
      </div>
    </div>
  </div>
</template>

<style scoped>
.publish-page {
  max-width: 1000px;
  margin: 0 auto;
}

/* 头部 */
.publish-header {
  display: flex;
  align-items: center;
  gap: 20px;
  margin-bottom: 36px;
  padding: 20px 0;
}

.header-deco {
  flex-shrink: 0;
}

.deco-stroke {
  width: 4px;
  height: 48px;
  background: linear-gradient(to bottom, var(--orange-brown), var(--dust-rose-muted));
  border-radius: 2px;
}

.publish-title {
  font-family: var(--font-serif);
  font-size: 28px;
  font-weight: 600;
  color: var(--ink-dark);
}

.publish-sub {
  font-size: 14px;
  color: var(--ink-light);
  margin-top: 4px;
}

/* 布局 */
.publish-body {
  display: flex;
  gap: 36px;
  align-items: flex-start;
}

/* 侧边栏 */
.publish-sidebar {
  flex: 0 0 260px;
  position: sticky;
  top: 100px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.sidebar-card {
  background: var(--page-white);
  padding: 24px 20px;
  border-radius: 12px 4px 12px 4px;
  box-shadow: var(--shadow-card);
}

.sidebar-icon {
  font-family: var(--font-serif);
  font-size: 18px;
  font-weight: 700;
  color: var(--orange-brown);
  margin-bottom: 8px;
  letter-spacing: 0.1em;
}

.sidebar-title {
  font-family: var(--font-serif);
  font-size: 15px;
  color: var(--ink-dark);
  margin-bottom: 8px;
}

.sidebar-desc {
  font-size: 12px;
  color: var(--ink-light);
  line-height: 1.6;
  margin-bottom: 16px;
}

.isbn-input-group {
  display: flex;
  gap: 8px;
}

.isbn-input {
  flex: 1;
  padding: 8px 12px;
  border: 1.5px solid var(--warm-apricot-deep);
  border-radius: 6px;
  font-size: 13px;
  font-family: var(--font-sans);
  outline: none;
  background: var(--warm-cream);
}

.isbn-input:focus {
  border-color: var(--orange-brown-light);
}

.isbn-btn {
  padding: 8px 14px;
  font-size: 13px;
}

.sidebar-tips {
  background: var(--warm-apricot);
  padding: 18px 20px;
  border-radius: 8px 3px 8px 3px;
}

.tips-title {
  font-size: 13px;
  font-weight: 500;
  color: var(--ink-medium);
  margin-bottom: 10px;
}

.tips-list {
  list-style: none;
  padding: 0;
  font-size: 12px;
  color: var(--ink-light);
  line-height: 1.8;
}

.tips-list li::before {
  content: '·';
  color: var(--orange-brown);
  margin-right: 6px;
  font-weight: bold;
}

/* 表单区 */
.publish-form-area {
  flex: 1;
  min-width: 0;
}

.form-section {
  margin-bottom: 32px;
}

.section-label {
  font-family: var(--font-serif);
  font-size: 16px;
  font-weight: 500;
  color: var(--ink-dark);
  margin-bottom: 18px;
  padding-bottom: 8px;
  border-bottom: 1px solid var(--warm-apricot-deep);
  display: flex;
  align-items: center;
  gap: 8px;
}

.section-label::before {
  content: '';
  width: 3px;
  height: 14px;
  background: var(--orange-brown);
  border-radius: 2px;
}

.field-group {
  display: flex;
  flex-direction: column;
  gap: 5px;
  flex: 1;
  margin-bottom: 16px;
}

.field-group.full {
  width: 100%;
}

.field-row {
  display: flex;
  gap: 16px;
}

.field-row.three {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap: 16px;
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
  transition: border-color 0.2s;
  line-height: 1.6;
}

.field-textarea:focus {
  border-color: var(--orange-brown-light);
  background: var(--page-white);
}

/* 分类药丸 */
.category-pills {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.cat-pill {
  padding: 6px 16px;
  font-size: 13px;
  font-family: var(--font-sans);
  border: 1.5px solid var(--warm-apricot-deep);
  border-radius: 18px;
  background: transparent;
  color: var(--ink-light);
  cursor: pointer;
  transition: all 0.2s;
}

.cat-pill:hover {
  border-color: var(--dust-rose);
  color: var(--orange-brown);
}

.cat-pill.active {
  border-color: var(--orange-brown);
  background: rgba(196, 112, 63, 0.08);
  color: var(--orange-brown);
  font-weight: 500;
}

.upload-add {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--ink-faint);
}

.submit-btn {
  width: 100%;
  padding: 14px;
  font-size: 16px;
  margin-top: 8px;
}

.submit-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

@media (max-width: 800px) {
  .publish-body {
    flex-direction: column;
  }

  .publish-sidebar {
    flex: none;
    width: 100%;
    position: static;
  }

  .field-row, .field-row.three {
    flex-direction: column;
    display: flex;
  }
}
</style>
