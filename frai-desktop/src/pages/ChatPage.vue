<!-- src/pages/ChatPage.vue -->
<template>
  <q-page padding class="row">
    <!-- Header -->
    <q-toolbar class="col-12">
      <q-btn flat round dense icon="arrow_back" @click="goBack" />
      <q-toolbar-title>Чат</q-toolbar-title>
    </q-toolbar>

    <!-- Chat area -->
    <div class="chat-container col-12">
      <!-- Message list -->
      <div class="messages">
        <div
          v-for="msg in messages"
          :key="msg.id"
          :class="['message', msg.from === 'user' ? 'user' : 'ai']"
        >
          <div class="bubble">
            <component :is="getComponent(msg)" :msg="msg" />
          </div>
          <div class="time">{{ formatTime(msg.time) }}</div>
        </div>
      </div>

      <!-- Input row -->
      <div class="input-row">
        <q-btn flat round dense icon="attach_file" @click="attachFile" />
        <q-input
          v-model="draft"
          placeholder="Напишите сообщение…"
          @keyup.enter="sendText"
          dense
          class="flex"
        />
        <q-btn flat round dense icon="send" color="primary" @click="sendText" />
      </div>
    </div>
  </q-page>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import TextMsg from 'src/components/chat/TextMsg.vue'
import MarkdownMsg from 'src/components/chat/MarkdownMsg.vue'
import ImageMsg from 'src/components/chat/ImageMsg.vue'

// Тип для сообщений
interface ChatMessage {
  id: number
  from: 'user' | 'ai'
  type: 'text' | 'markdown' | 'image'
  content: string
  time: Date
}

const router = useRouter()

// Мок-данные
const messages = ref<ChatMessage[]>([
  {
    id: 1,
    from: 'ai',
    type: 'text',
    content: 'Привет! Чем могу помочь?',
    time: new Date(),
  },
  {
    id: 2,
    from: 'user',
    type: 'text',
    content: 'Покажи мне список последних событий в доме.',
    time: new Date(),
  },
  {
    id: 3,
    from: 'ai',
    type: 'markdown',
    content: `
| Датчик       | Статус  |
|--------------|---------|
| Дверь входа  | открыт  |
| Температура  | 22°C    |
`,
    time: new Date(),
  },
  {
    id: 4,
    from: 'user',
    type: 'image',
    content: 'https://via.placeholder.com/120x80.png?text=Camera+shot',
    time: new Date(),
  },
])

const draft = ref('')

// Выбираем компонент по типу сообщения
function getComponent(msg: ChatMessage) {
  switch (msg.type) {
    case 'text':
      return TextMsg
    case 'markdown':
      return MarkdownMsg
    case 'image':
      return ImageMsg
    default:
      return TextMsg
  }
}

// Формат времени в HH:MM
function formatTime(date: Date) {
  return date.toLocaleTimeString().slice(0, 5)
}

// Отправка текстового сообщения
function sendText() {
  if (!draft.value.trim()) {
    return
  }
  messages.value.push({
    id: messages.value.length + 1,
    from: 'user',
    type: 'text',
    content: draft.value,
    time: new Date(),
  })
  draft.value = ''
}

// Обработчик прикрепления файлов (заглушка)
function attachFile() {
  // TODO: открыть файловый селектор и добавить прикреплённый файл в messages
}

// Переход назад
function goBack() {
  router.back()
}
</script>

<style scoped>
.chat-container {
  display: flex;
  flex-direction: column;
  height: calc(100vh - 56px); /* учёт тулбара */
}

.messages {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
}

.message {
  display: flex;
  flex-direction: column;
  max-width: 65%;
  margin-bottom: 12px;
}

.message.ai {
  align-self: flex-start;
}

.message.user {
  align-self: flex-end;
}

.bubble {
  padding: 8px 12px;
  border-radius: 12px;
  background: var(--q-color-grey-2);
}

.message.user .bubble {
  background: var(--q-color-primary);
  color: white;
}

.time {
  font-size: 0.7em;
  color: var(--q-color-grey-5);
  margin-top: 2px;
  text-align: right;
}

.input-row {
  display: flex;
  align-items: center;
  padding: 8px;
  border-top: 1px solid var(--q-color-grey-4);
}
</style>
