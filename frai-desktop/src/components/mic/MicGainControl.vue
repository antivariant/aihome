<template>
  <q-card class="q-pa-md q-mb-md">
    <q-card-section class="row items-center justify-between">
      <div class="text-h6">
        🎛️ Усиление микрофона
      </div>
      <q-circular-progress
        show-value
        :value="gainDisplay"
        size="70px"
        :thickness="0.15"
        color="primary"
        track-color="grey-3"
        class="cursor-pointer"
        @wheel="onWheel"
      >
        <q-icon name="mic" class="q-mr-xs" />
        {{ gainDisplay }}%
      </q-circular-progress>
    </q-card-section>
  </q-card>
</template>

<script setup lang="ts">
import { ref, defineExpose } from 'vue'

const micGain = ref(2.0) // Усиление микрофона (0.5 – 5.0)
const gainDisplay = ref(Math.round(micGain.value * 20)) // Отображаемое значение в %

function onWheel(e: WheelEvent) {
  e.preventDefault()
  const delta = e.deltaY > 0 ? -0.1 : 0.1
  micGain.value = Math.min(5, Math.max(0.5, micGain.value + delta))
  gainDisplay.value = Math.round(micGain.value * 20)
}

// Делаем micGain доступным родителю
defineExpose({ micGain })
</script>
