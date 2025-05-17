<template>
  <div class="chat-messages column full-height">
    <q-scroll-area class="fit">
      <div class="column q-gutter-sm q-pa-md" style="width: 100%;">
        <q-chat-message
          v-for="msg in messages"
          :key="msg.id"
          :name="msg.name"
          :text="[msg.text]"
          :sent="msg.sent"
        >
          <template #stamp>
            <span class="text-grey-9">{{ msg.stamp }}</span>
            <q-chip
              v-if="!msg.sent && msg.interactionId"
              dense
              outline
              class="interaction-badge q-ml-sm"
              text-color="grey-9"
              @click.prevent="selectInteraction(msg.interactionId)"
            >
              {{ msg.interactionId }}
            </q-chip>
          </template>
        </q-chat-message>
      </div>
    </q-scroll-area>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { defineEmits } from 'vue'
import { useChatStore } from 'stores/chat'

// Событие на выбор human log
const emit = defineEmits<{
  (e: 'select-interaction', id: string): void
}>()

function selectInteraction(id: string) {
  emit('select-interaction', id)
}

const chatStore = useChatStore()

interface Msg {
  id: string
  interactionId: string
  name: string
  text: string
  stamp: string
  sent: boolean
}

// Подготовка данных для QChatMessage
const messages = computed<Msg[]>(() => {
  return chatStore.messages.map(entry => {
    // безопасно подставляем interaction_id или пустую строку
    const interactionId = entry.interaction_id ?? ''

    return {
      id: entry.id,
      interactionId,
      name: entry.fromUser ? 'You' : 'Bot',
      text: entry.text,
      stamp: new Date(entry.timestamp).toLocaleTimeString(),
      sent: entry.fromUser
    }
  })
})
</script>

<style scoped>
.full-height {
  height: 100%;
}

.interaction-badge {
  cursor: pointer;
  border-radius: 12px;
}
</style>
