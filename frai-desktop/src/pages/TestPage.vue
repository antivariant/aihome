<template>
  <q-page padding class="column q-gutter-md">

    <!-- 🔊 Микрофон -->
    <q-card flat bordered>
      <q-card-section>
        <div class="text-h6">🎙️ Голосовой ввод</div>
        <q-btn
          color="primary"
          label="Начать запись"
          @click="startRecording"
          :disable="isRecording"
        />
        <q-btn
          color="negative"
          label="Остановить"
          @click="stopRecording"
          :disable="!isRecording"
          class="q-ml-sm"
        />
      </q-card-section>
    </q-card>

    <!-- 📷 Камера -->
    <q-card flat bordered>
      <q-card-section>
        <div class="text-h6">📷 Камера</div>
        <video ref="videoRef" autoplay playsinline muted class="full-width" style="max-height: 240px;" />
      </q-card-section>
    </q-card>

    <!-- 🧠 Ответ -->
    <q-card flat bordered>
      <q-card-section>
        <div class="text-h6">🧠 Ответ AI</div>
        <div v-if="responseType === 'text'">{{ responseData }}</div>
        <audio v-if="responseType === 'voice'" :src="responseData" controls autoplay />
        <video v-if="responseType === 'video'" :src="responseData" controls autoplay />
      </q-card-section>
    </q-card>

    <!-- 📦 Инфо -->
    <q-card flat bordered>
      <q-card-section>
        <div class="text-subtitle2">📌 Debug Info</div>
        <div>Device ID: {{ deviceId }}</div>
        <div>User ID: {{ userId }}</div>
        <div>Input Type: {{ inputType }}</div>
        <div>Response Type: {{ responseType }}</div>
      </q-card-section>
    </q-card>

  </q-page>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'

const videoRef = ref<HTMLVideoElement | null>(null)
const isRecording = ref(false)

const deviceId = 'frai-macbook-001'
const userId = ref('unknown')
const inputType = ref('voice')
const responseType = ref<'text' | 'voice' | 'video'>('text')
const responseData = ref('')

function startRecording() {
  isRecording.value = true
  // TODO: start sending audio chunks to backend
}

function stopRecording() {
  isRecording.value = false
  // TODO: finalize and send audio blob to svc-audio-in
}

onMounted(async () => {
  const stream = await navigator.mediaDevices.getUserMedia({ video: true })
  if (videoRef.value) {
    videoRef.value.srcObject = stream
  }
})
</script>
