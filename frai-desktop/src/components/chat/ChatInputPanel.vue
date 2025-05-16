// --- Файл: src/components/chat/ChatInputPanel.vue ---
<template>
  <div class="chat-input q-pa-md row items-center">
    <q-input
      v-model="message"
      placeholder="Введите сообщение"
      @keyup.enter="send"
      dense
      outlined
      class="col"
    >
      <template #append>
        <q-btn flat icon="send" @click="send" />
      </template>
    </q-input>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useChatStore } from 'src/stores/chat'

const chatStore = useChatStore()
const message = ref('')

async function send() {
  if (!message.value.trim()) return
  await chatStore.sendMessage(message.value)
  message.value = ''
}
</script>

<style scoped>
.chat-input {
  border-top: 1px solid var(--q-color-grey-4);
}
</style>
