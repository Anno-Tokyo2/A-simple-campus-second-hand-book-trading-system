<script setup>
import { ref, onMounted, nextTick, computed } from 'vue'
import { useUserStore } from '../stores/user'
import api from '../api'

const userStore = useUserStore()
const selectedConv = ref(null)
const messages = ref([])
const newMessage = ref('')
const loading = ref(false)
const chatBody = ref(null)

// 按用户ID组织的会话数据 — 每个用户只能看到自己的会话
const allConversations = {
  1: [ // admin
    { user_id: 4, nickname: '王同学', last_message: '请问数据结构有配套代码吗？', last_time: '2025-06-14 10:30', unread: 1 },
  ],
  2: [ // zhangsan
    { user_id: 3, nickname: '李同学', last_message: '对的，成色还不错', last_time: '2025-06-15 10:15', unread: 0 },
    { user_id: 6, nickname: '孙同学', last_message: '没有哦，只有纸质版', last_time: '2025-06-12 09:30', unread: 0 },
  ],
  3: [ // lisi
    { user_id: 2, nickname: '张同学', last_message: '好的，那我们约图书馆门口交易吧', last_time: '2025-06-15 14:30', unread: 2 },
    { user_id: 9, nickname: '郑同学', last_message: '建议配合视频课程看', last_time: '2025-06-13 15:00', unread: 0 },
  ],
  4: [ // wangwu
    { user_id: 1, nickname: '管理员', last_message: '有的，在最后一章', last_time: '2025-06-14 11:00', unread: 0 },
  ],
  6: [ // sunqi
    { user_id: 2, nickname: '张同学', last_message: 'Python那本书有电子版吗？', last_time: '2025-06-12 09:00', unread: 1 },
  ],
  9: [ // zhengshi
    { user_id: 3, nickname: '李同学', last_message: '编译原理适合自学吗？', last_time: '2025-06-13 14:00', unread: 0 },
  ],
}

// 按会话双方组织的聊天记录 key: "小id_大id"
const allMessages = {
  '2_3': [
    { id: 1, sender_id: 2, content: '你好，我想问一下那本高等数学还在吗？', created_at: '2025-06-15 10:00' },
    { id: 2, sender_id: 3, content: '在的，15书币', created_at: '2025-06-15 10:05' },
    { id: 3, sender_id: 2, content: '嗯嗯，我直接拍了', created_at: '2025-06-15 10:10' },
    { id: 4, sender_id: 3, content: '好的，成色还不错', created_at: '2025-06-15 10:15' },
    { id: 5, sender_id: 2, content: '好的，那我们约图书馆门口交易吧', created_at: '2025-06-15 14:30' },
  ],
  '2_6': [
    { id: 1, sender_id: 6, content: 'Python那本书有电子版吗？', created_at: '2025-06-12 09:00' },
    { id: 2, sender_id: 2, content: '没有哦，只有纸质版', created_at: '2025-06-12 09:30' },
  ],
  '1_4': [
    { id: 1, sender_id: 4, content: '请问数据结构有配套代码吗？', created_at: '2025-06-14 10:00' },
    { id: 2, sender_id: 1, content: '有的，在最后一章', created_at: '2025-06-14 10:30' },
    { id: 3, sender_id: 4, content: '谢谢！', created_at: '2025-06-14 11:00' },
  ],
  '3_9': [
    { id: 1, sender_id: 9, content: '编译原理适合自学吗？', created_at: '2025-06-13 14:00' },
    { id: 2, sender_id: 3, content: '建议配合视频课程看', created_at: '2025-06-13 15:00' },
  ],
}

function getConvKey(uid1, uid2) {
  return uid1 < uid2 ? `${uid1}_${uid2}` : `${uid2}_${uid1}`
}

const myId = computed(() => userStore.userInfo?.id || 0)

const conversations = ref([])

onMounted(async () => {
  try {
    const r = await api.get('/api/messages/conversations')
    conversations.value = r.data.items?.length ? r.data.items : (allConversations[myId.value] || [])
  } catch {
    conversations.value = allConversations[myId.value] || []
  }
})

function resolveMessages(otherId) {
  const key = getConvKey(myId.value, otherId)
  return allMessages[key] || []
}

async function selectConversation(conv) {
  selectedConv.value = conv
  conv.unread = 0
  try {
    const r = await api.get(`/api/messages/conversations/${conv.user_id}`)
    messages.value = r.data.items?.length ? r.data.items : resolveMessages(conv.user_id)
  } catch {
    messages.value = resolveMessages(conv.user_id)
  }
  await nextTick()
  scrollToBottom()
}

async function sendMessage() {
  if (!newMessage.value.trim() || !selectedConv.value) return
  try {
    await api.post('/api/messages', { receiver_id: selectedConv.value.user_id, content: newMessage.value })
  } catch {}
  messages.value.push({
    id: Date.now(),
    sender_id: myId.value,
    content: newMessage.value,
    created_at: new Date().toISOString().slice(0, 16).replace('T', ' ')
  })
  newMessage.value = ''
  await nextTick()
  scrollToBottom()
}

function scrollToBottom() {
  if (chatBody.value) chatBody.value.scrollTop = chatBody.value.scrollHeight
}

function formatTime(t) {
  if (!t) return ''
  return t.slice(11, 16)
}
</script>

<template>
  <div class="msg-page">
    <header class="msg-header">
      <h1 class="msg-title">消息</h1>
      <p class="msg-sub">与同学沟通交流</p>
    </header>

    <div class="msg-layout">
      <!-- 会话列表 -->
      <div class="conv-list">
        <div v-if="conversations.length === 0" class="conv-empty">
          <p>暂无会话</p>
          <p class="conv-empty-hint">在求购区回应或联系卖家后会出现在这里</p>
        </div>
        <div
          v-for="conv in conversations"
          :key="conv.user_id"
          class="conv-item"
          :class="{ active: selectedConv?.user_id === conv.user_id }"
          @click="selectConversation(conv)"
        >
          <div class="conv-avatar">{{ conv.nickname?.[0] || '用' }}</div>
          <div class="conv-info">
            <span class="conv-name">{{ conv.nickname }}</span>
            <span class="conv-last">{{ conv.last_message }}</span>
          </div>
          <div class="conv-meta">
            <span class="conv-time">{{ formatTime(conv.last_time) }}</span>
            <span v-if="conv.unread" class="conv-badge">{{ conv.unread }}</span>
          </div>
        </div>
      </div>

      <!-- 聊天区 -->
      <div class="chat-area">
        <template v-if="selectedConv">
          <div class="chat-header">
            <div class="chat-avatar">{{ selectedConv.nickname?.[0] || '用' }}</div>
            <span class="chat-name">{{ selectedConv.nickname }}</span>
          </div>

          <div ref="chatBody" class="chat-body">
            <div
              v-for="msg in messages"
              :key="msg.id"
              class="chat-msg"
              :class="{ mine: msg.sender_id === myId }"
            >
              <div class="msg-bubble">{{ msg.content }}</div>
              <span class="msg-time">{{ formatTime(msg.created_at) }}</span>
            </div>
          </div>

          <div class="chat-input-bar">
            <input
              v-model="newMessage"
              type="text"
              class="chat-input"
              placeholder="输入消息..."
              @keyup.enter="sendMessage"
            />
            <button class="btn-warm send-btn" @click="sendMessage">发送</button>
          </div>
        </template>

        <div v-else class="chat-placeholder">
          <div class="placeholder-icon">
            <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.2">
              <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
            </svg>
          </div>
          <p>选择一个会话开始聊天</p>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.msg-page {
  max-width: 900px;
  margin: 0 auto;
}

.msg-header { margin-bottom: 28px; }

.msg-title {
  font-family: var(--font-serif);
  font-size: 24px;
  font-weight: 600;
  color: var(--ink-dark);
}

.msg-sub { font-size: 13px; color: var(--ink-light); margin-top: 4px; }

.msg-layout {
  display: flex;
  height: 560px;
  background: var(--page-white);
  border-radius: 12px 4px 12px 4px;
  overflow: hidden;
  box-shadow: var(--shadow-card);
}

.conv-list {
  width: 280px;
  border-right: 1px solid var(--warm-apricot-deep);
  overflow-y: auto;
  flex-shrink: 0;
}

.conv-empty {
  padding: 40px 20px;
  text-align: center;
  color: var(--ink-faint);
  font-size: 14px;
}

.conv-empty-hint {
  font-size: 12px;
  margin-top: 8px;
  color: var(--ink-faint);
  opacity: 0.7;
}

.conv-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px 16px;
  cursor: pointer;
  transition: background 0.15s;
  border-bottom: 1px solid rgba(237, 216, 193, 0.5);
}

.conv-item:hover { background: var(--warm-cream); }
.conv-item.active { background: var(--warm-apricot); }

.conv-avatar {
  width: 38px;
  height: 38px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--dust-rose-light), var(--dust-rose));
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  font-family: var(--font-serif);
  flex-shrink: 0;
}

.conv-info { flex: 1; min-width: 0; display: flex; flex-direction: column; }
.conv-name { font-size: 14px; font-weight: 500; color: var(--ink-dark); }
.conv-last { font-size: 12px; color: var(--ink-faint); margin-top: 2px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }

.conv-meta { display: flex; flex-direction: column; align-items: flex-end; gap: 4px; flex-shrink: 0; }
.conv-time { font-size: 11px; color: var(--ink-faint); }
.conv-badge { width: 18px; height: 18px; border-radius: 50%; background: var(--orange-brown); color: white; font-size: 11px; display: flex; align-items: center; justify-content: center; }

.chat-area { flex: 1; display: flex; flex-direction: column; }

.chat-header {
  padding: 14px 20px;
  border-bottom: 1px solid var(--warm-apricot-deep);
  display: flex;
  align-items: center;
  gap: 10px;
}

.chat-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--orange-brown-light), var(--orange-brown));
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 13px;
  font-family: var(--font-serif);
}

.chat-name { font-size: 14px; font-weight: 500; color: var(--ink-dark); }

.chat-body {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.chat-msg { display: flex; flex-direction: column; max-width: 70%; }
.chat-msg.mine { align-self: flex-end; align-items: flex-end; }

.msg-bubble {
  padding: 10px 16px;
  border-radius: 12px 12px 4px 12px;
  background: var(--warm-apricot);
  font-size: 14px;
  color: var(--ink-dark);
  line-height: 1.5;
}

.chat-msg.mine .msg-bubble {
  background: var(--orange-brown);
  color: white;
  border-radius: 12px 12px 12px 4px;
}

.msg-time { font-size: 11px; color: var(--ink-faint); margin-top: 4px; padding: 0 4px; }

.chat-input-bar {
  padding: 14px 16px;
  border-top: 1px solid var(--warm-apricot-deep);
  display: flex;
  gap: 10px;
}

.chat-input {
  flex: 1;
  padding: 10px 14px;
  border: 1.5px solid var(--warm-apricot-deep);
  border-radius: 20px;
  font-size: 14px;
  font-family: var(--font-sans);
  outline: none;
  background: var(--warm-cream);
}

.chat-input:focus { border-color: var(--orange-brown-light); background: var(--page-white); }

.send-btn { padding: 10px 20px; border-radius: 20px; }

.chat-placeholder {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: var(--ink-faint);
  gap: 12px;
}

.placeholder-icon { opacity: 0.3; }

@media (max-width: 700px) {
  .msg-layout { flex-direction: column; height: auto; }
  .conv-list { width: 100%; max-height: 200px; border-right: none; border-bottom: 1px solid var(--warm-apricot-deep); }
  .chat-body { min-height: 300px; }
}
</style>
