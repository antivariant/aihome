<template>
  <q-page class="q-pa-md row">
    <div class="col-8">
      <q-card flat bordered class="q-pa-md bg-dark text-white">
        <div v-for="(msg, index) in messages" :key="msg.id" class="q-mb-md">
          <div v-if="msg.fromUser" class="text-right">
            <q-badge
              v-if="messages[index + 1]?.interaction_id"
              color="primary"
              :label="messages[index + 1]?.interaction_id!.slice(0, 4)"
              class="q-mb-xs cursor-pointer"
              @click="selectInteraction(messages[index + 1].interaction_id!)"
            />
            <q-chat-message
              :text="[msg.text]"
              sent
              bg-color="blue"
              text-color="white"
            />
          </div>
          <div v-else>
            <q-chat-message
              :text="[msg.text]"
              bg-color="grey-8"
              text-color="white"
            />
          </div>
        </div>

        <q-input
          v-model="text"
          label="Введите сообщение"
          outlined
          dense
          class="q-mt-md"
          @keyup.enter="send"
        >
          <template v-slot:append>
            <q-btn icon="send" flat round dense @click="send" />
          </template>
        </q-input>
      </q-card>
    </div>

    <div class="col-4 q-pl-md">
      <HumanLogPanel
        v-if="selectedInteractionId"
        :interaction-id="selectedInteractionId"
      />
    </div>
  </q-page>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useChatStore } from 'src/stores/chat'
import HumanLogPanel from 'src/components/chat/humanLogPanel.vue'

const store = useChatStore()
const messages = store.messages
const text = ref('')
const selectedInteractionId = ref('')

const send = async () => {
  if (text.value.trim()) {
    await store.sendMessage(text.value.trim())
    text.value = ''
    const lastAI = [...store.messages].reverse().find((m) => !m.fromUser);
    selectedInteractionId.value = lastAI?.interaction_id || ''
  }
}

const selectInteraction = (id: string) => {
  selectedInteractionId.value = id
}
</script>

<style scoped>
.bg-dark {
  background-color: #121212;
}
</style>
