<template>
  <q-page padding class="frai-page bg-dark text-white">
    <div class="column q-gutter-md items-center">

      <!-- Верхний ряд -->
      <div class="row q-gutter-md full-width justify-center items-start">
        <!-- Камера -->
        <div class="frai-block" style="width: 500px; height: 320px">
          <q-card flat bordered class="bg-grey-10 text-white full-height">
            <q-card-section class="row items-start q-gutter-md full-height">
              <div class="frai-frame">
                <video
                  ref="cameraVideo"
                  autoplay
                  muted
                  playsinline
                  class="frai-video-shifted"
                  v-if="isCameraOn"
                  :style="{ transform: `translateX(-${actuatorOffset}px)` }"
                />
              </div>
              <div class="column justify-between full-height" style="width: 140px;">
                <div class="column items-center q-mt-xs">
                  <div class="text-h6 text-center">Камера</div>
                  <q-toggle v-model="isCameraOn" label="Трансляция" color="green" @update:model-value="toggleCamera" class="self-center" />
                  <div v-if="isCameraOn" class="text-caption self-start">FPS: {{ cameraFps }}</div>
                </div>
                <div class="column items-center q-mb-sm">
                  <q-slider v-model="actuatorAngle" :min="0" :max="180" label label-always class="q-mt-sm" />
                  <div class="text-caption">Актуатор: {{ actuatorAngle }}°</div>
                </div>
              </div>
            </q-card-section>
          </q-card>
        </div>

        <!-- Экран F.R.A.I -->
        <div class="frai-block" style="width: 500px; height: 320px">
          <q-card flat bordered class="bg-grey-10 text-white full-height">
            <q-card-section class="row items-start q-gutter-md full-height">
              <div class="frai-screen">
                <video
                  v-if="isAvatarOn && avatarVideo"
                  :src="avatarVideo"
                  autoplay
                  loop
                  muted
                  class="frai-video"
                />
                <div v-else class="frai-placeholder flex flex-center text-center">
                  {{ placeholderText }}
                </div>
              </div>
              <div class="column items-center" style="width: 140px;">
                <div class="text-h6 text-center">Экран F.R.A.I</div>
                <q-toggle v-model="isAvatarOn" label="Видео" color="green" class="self-center" />
                <div v-if="isAvatarOn" class="text-caption self-start">FPS: 25</div>
              </div>
            </q-card-section>
          </q-card>
        </div>
      </div>

      <!-- Нижний ряд -->
      <div class="row q-gutter-md full-width justify-center">
        <!-- Микрофон -->
        <div class="frai-block" style="width: 500px">
          <q-card flat bordered class="bg-grey-10 text-white">
            <q-card-section class="row items-center justify-between">
              <div class="column items-center q-gutter-xs">
                <q-circular-progress
                  :value="micSignalLevel * 100"
                  size="100px"
                  show-value
                  font-size="12px"
                  color="lime"
                >
                  <q-icon name="mic" size="30px" />
                </q-circular-progress>
                <div class="text-caption text-center">Уровень</div>
              </div>
              <div class="column items-center q-gutter-xs">
                <q-toggle v-model="isMicOn" color="green" />
                <div class="text-caption">Микрофон</div>
              </div>
            </q-card-section>
          </q-card>
        </div>

        <!-- Динамик -->
        <div class="frai-block" style="flex: 1">
          <q-card flat bordered class="bg-grey-10 text-white">
            <q-card-section class="row items-center justify-around">
              <div class="column items-center q-gutter-xs">
                <q-circular-progress
                  :value="speakerSignalLevel * 100"
                  size="100px"
                  show-value
                  font-size="12px"
                  color="blue"
                >
                  <q-icon name="volume_up" size="30px" />
                </q-circular-progress>
                <div class="text-caption text-center">Уровень</div>
              </div>
              <div class="column items-center q-gutter-xs">
                <q-slider
                  v-model="volume"
                  :min="0"
                  :max="100"
                  vertical
                  style="height: 100px;"
                />
                <div class="text-caption">Громкость</div>
              </div>
              <div class="column items-center q-gutter-xs">
                <q-toggle v-model="isSpeakerOn" color="green" />
                <div class="text-caption">Звук</div>
              </div>
            </q-card-section>
          </q-card>
        </div>
      </div>

    </div>
  </q-page>
</template>



<script setup lang="ts">
import { ref, onBeforeUnmount, computed } from 'vue'

const isMicOn = ref(true)
const micSignalLevel = ref(0.3)
const isSpeakerOn = ref(true)
const speakerSignalLevel = ref(0.4)
const isCameraOn = ref(false)
const isAvatarOn = ref(true)
const cameraFps = ref(30)
const avatarVideo = ref('')
const placeholderText = ref('Привет! Я F.R.A.I.')
const volume = ref(50)
const actuatorAngle = ref(90) // от 0 до 180

const actuatorOffset = computed(() => (50 / 180) * actuatorAngle.value)

const cameraVideo = ref<HTMLVideoElement | null>(null)
let stream: MediaStream | null = null

function toggleCamera(val: boolean) {
  if (val) {
    navigator.mediaDevices.getUserMedia({ video: true }).then((mediaStream) => {
      stream = mediaStream
      if (cameraVideo.value) cameraVideo.value.srcObject = stream
    })
  } else {
    stream?.getTracks().forEach((track) => track.stop())
    stream = null
  }
}

onBeforeUnmount(() => {
  if (stream) {
    stream.getTracks().forEach((t) => t.stop())
  }
})
</script>

<style scoped>
.frai-page {
  max-width: 1200px;
  margin: auto;
}
.frai-block {
  width: 100%;
  max-width: 500px;
  min-height: 300px;
}
.frai-frame {
  width: 250px;
  height: 250px;
  overflow: hidden;
  position: relative;
  background: black;
}
.frai-video-shifted {
  width: 300px;
  height: 250px;
  object-fit: cover;
  border: 1px solid white;
  position: absolute;
  top: 0;
  left: 0;
  transition: transform 0.3s ease-out;
}
.frai-screen {
  width: 250px;
  height: 250px;
  background: black;
  position: relative;
  flex-shrink: 0;
}
.frai-video {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border: 1px solid white;
}
.frai-placeholder {
  color: white;
  font-size: 16px;
  padding: 10px;
  height: 100%;
  background: black;
}
</style>
