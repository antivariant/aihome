<template>
  <q-card class="q-pa-md">
    <q-card-section class="row items-center justify-between">
      <div class="text-h6">🎙️ Уровень микрофона</div>
      <q-linear-progress
        :value="micLevel"
        size="10px"
        color="primary"
        class="q-mt-sm"
        style="width: 200px"
        :buffer="1"
      />
    </q-card-section>
  </q-card>
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount } from 'vue'

const micLevel = ref(0)
let audioContext: AudioContext | null = null
let analyser: AnalyserNode | null = null
let dataArray: Uint8Array | null = null
let animationFrameId: number

function updateLevel() {
  if (analyser && dataArray) {
    analyser.getByteTimeDomainData(dataArray)

    // Вычисляем среднеквадратичное отклонение
    const rms = Math.sqrt(dataArray.reduce((sum, v) => {
      const normalized = (v - 128) / 128
      return sum + normalized * normalized
    }, 0) / dataArray.length)

    micLevel.value = rms // уже от 0 до 1
  }

  animationFrameId = requestAnimationFrame(updateLevel)
}

onMounted(async () => {
  try {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
    audioContext = new AudioContext()
    const source = audioContext.createMediaStreamSource(stream)
    analyser = audioContext.createAnalyser()
    analyser.fftSize = 2048
    dataArray = new Uint8Array(analyser.fftSize)
    source.connect(analyser)
    updateLevel()
  } catch (e) {
    console.error('Ошибка при получении доступа к микрофону:', e)
  }
})

onBeforeUnmount(() => {
  if (animationFrameId) cancelAnimationFrame(animationFrameId)
  audioContext?.close()
})
</script>
