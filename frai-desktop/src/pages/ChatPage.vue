<template>
  <q-page class="column q-pa-md">
    <q-card class="column items-stretch">
      <q-card-section class="col">
        <div class="text-h6">F.R.A.I Chat</div>
      </q-card-section>

      <q-separator />

      <q-card-section class="col scroll" style="max-height: 400px; overflow-y: auto;">
        <div v-for="(msg, index) in messages" :key="index" class="q-mb-sm">
          <q-chip square>{{ msg }}</q-chip>
        </div>
      </q-card-section>

      <q-separator />

      <q-card-actions align="right">
        <q-input
          filled
          v-model="input"
          label="Введите сообщение"
          class="col"
          @keyup.enter="sendMessage"
        />
        <q-btn label="Отправить" color="primary" @click="sendMessage" />
      </q-card-actions>
    </q-card>
  </q-page>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const input = ref('')
const messages = ref<string[]>([])

function sendMessage() {
  if (input.value.trim() !== '') {
    messages.value.push(input.value)
    input.value = ''
  }
}
</script>
