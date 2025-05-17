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
              clickable
              dense
              outline
              class="interaction-badge q-ml-sm"
              :class="{ 'interaction-selected': msg.interactionId === selectedInteraction }"
              :text-color="msg.interactionId === selectedInteraction ? 'white' : 'grey-9'"
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
import { useChatStore } from 'stores/chat'

const chatStore = useChatStore()

interface Msg {
  id: string
  interactionId: string
  name: string
  text: string
  stamp: string
  sent: boolean
}

// Подготовка списка сообщений
const messages = computed<Msg[]>(() =>
  chatStore.messages.map(entry => ({
    id: entry.id,
    interactionId: entry.interaction_id ?? '',
    name: entry.fromUser ? 'You' : 'Bot',
    text: entry.text,
    stamp: new Date(entry.timestamp).toLocaleTimeString(),
    sent: entry.fromUser
  }))
)

// Текущий выбранный interaction_id из стора
const selectedInteraction = computed<string | undefined>(
  () => chatStore.interaction_id
)

// По клику устанавливаем новый interaction_id
function selectInteraction(id: string) {
  chatStore.setInteractionId(id)
}
</script>

<style scoped>
.full-height {
  height: 100%;
}

.interaction-badge {
  cursor: pointer;
  border-radius: 12px;
}

/* Выделенный бейдж: белый текст и белая рамка */
.interaction-selected {
  border-color: white !important;
}
</style>
