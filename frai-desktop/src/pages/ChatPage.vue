// --- Файл: src/pages/ChatPage.vue ---
<template>
  <q-page class="chat-page">
    <div class="main-chat">
      <ChatMessagesPanel class="chat-messages" />
      <ChatInputPanel class="chat-input" />
    </div>
    <div class="human-log">
      <HumanLogPanel />
    </div>
  </q-page>
</template>

<script setup lang="ts">
import ChatMessagesPanel from 'src/components/chat/ChatMessagesPanel.vue'
import ChatInputPanel    from 'src/components/chat/ChatInputPanel.vue'
import HumanLogPanel     from 'src/components/chat/humanLogPanel.vue'
</script>

<style scoped>
.chat-page {
  display: grid;
  height: 100%;
  grid-template-columns: 2fr 1fr;
  gap: 8px;
  padding: 8px;
  box-sizing: border-box;
}

.main-chat,
.human-log {
  background-color: #222;
  border-radius: 12px;
  padding: 8px;
  box-sizing: border-box;
  height: 100%;
}


.main-chat {
  display: grid;
  grid-template-rows: 2fr 1fr;
  gap: 8px;
}

.chat-messages,
.chat-input {
  background-color: var(--q-color-grey-9);
  border: 1px solid var(--q-color-grey-8);
  border-radius: 4px;
  padding: 8px;
  box-sizing: border-box;
}

.chat-messages {
  overflow: hidden;
}

.chat-input {
  overflow: hidden;
}
</style>
