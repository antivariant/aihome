// --- Файл: src/components/chat/ChatMessagesPanel.vue ---
<template>
  <div class="chat-messages column full-height">
    <q-scroll-area class="fit">
      <div class="column q-gutter-sm q-pa-md" style="width: 100%;">
        <!-- Основной чат без аватаров -->
        <q-chat-message
          v-for="msg in messages"
          :key="msg.id"
          :name="msg.name"
          :text="[msg.text]"
          :stamp="msg.stamp"
          :sent="msg.sent"
        />
      </div>
    </q-scroll-area>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useChatStore } from 'src/stores/chat'

const chatStore = useChatStore()
const messages = computed(() =>
  chatStore.messages.map(entry => ({
    id: entry.id,
    name: entry.fromUser ? 'You' : 'Frai',
    text: entry.text,
    stamp: new Date(entry.timestamp).toLocaleTimeString(),
    sent: entry.fromUser
  }))
)
</script>

<style scoped>
.full-height {
  height: 100%;
}
</style>
