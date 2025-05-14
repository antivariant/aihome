<template>
  <q-page class="frai-page">

    <div class="frai-grid">
      <!-- 1. Камера -->
      <div class="frai-cell camera-cell">
        <CameraPanel
          v-model:cameraOn="cameraOn"
          v-model:cameraFps="cameraFps"
          v-model:actuatorAngleX="actuatorAngleX"
          v-model:actuatorAngleY="actuatorAngleY"
          :previewWidth="previewWidth"
          :previewHeight="previewHeight"
        />
      </div>

      <!-- 2. TFT-эмулятор -->
      <div class="frai-cell tft-cell">
        <TFTScreenPanel
          v-model:isAvatarOn="isAvatarOn"
          avatarVideo="Привет! Я F.R.A.I."
          placeholderText="Здесь будет ваш TFT"
        />
      </div>

      <!-- 3. Настройки микрофона -->
      <div class="frai-cell mic-cell">
        <MicSettingsPanel
          v-model:micOn="micOn"
          v-model:micGain="micGain"
        />
      </div>

      <!-- 4. Настройки динамика -->
      <div class="frai-cell audio-cell">
        <AudioSettingsPanel
          v-model:audioOn="speakerOn"
          v-model:volume="speakerVolume"
        />
      </div>
    </div>

  </q-page>
</template>

<script setup lang="ts">
import { ref } from 'vue'

// относительные импорты
import CameraPanel from '../components/camera/CameraPanel.vue'
import TFTScreenPanel from '../components/screen/TFTScreenPanel.vue'
import MicSettingsPanel from '../components/mic/MicSettingsPanel.vue'
import AudioSettingsPanel from '../components/mic/AudioSettingsPanel.vue'

// 📷 Камера
const cameraOn = ref(false)
const cameraFps = ref(30)
const actuatorAngleX = ref(90)
const actuatorAngleY = ref(90)
const previewWidth = ref(300)
const previewHeight = ref(250)

// 📺 TFT-эмулятор
const isAvatarOn = ref(false)

// 🎤 Микрофон
const micOn = ref(false)
const micGain = ref(0.5)

// 🔊 Динамик
const speakerOn = ref(false)
const speakerVolume = ref(0.5)
</script>

<style scoped>
.frai-page {
  padding: 20px;
  box-sizing: border-box;
  height: 100vh;
  overflow: hidden;
}

.frai-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  grid-template-rows: 1fr 1fr;
  gap: 20px;
  height: 100%;
}

.frai-cell {
  display: flex;
}
.frai-cell > * {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.camera-cell {
  grid-column: 1 / 3;
  grid-row: 1;
}
.tft-cell {
  grid-column: 3 / 5;
  grid-row: 1;
  align-items: center;
}
.mic-cell {
  grid-column: 1 / 3;
  grid-row: 2;
}
.audio-cell {
  grid-column: 3 / 5;
  grid-row: 2;
}
</style>
