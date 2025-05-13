<template>
  <q-page padding class="frai-page bg-dark text-white">
    <div class="column q-gutter-md items-center">

      <!-- Верхний ряд -->
      <div class="row q-gutter-md full-width justify-center items-start">
        <!-- Камера -->
        <CameraPanel
          v-model:camera-on="isCameraOn"
          :camera-fps="cameraFps"
          v-model:actuator-angle-x="actuatorAngleX"
          v-model:actuator-angle-y="actuatorAngleY"
          :preview-width="cameraPreview.width"
          :preview-height="cameraPreview.height"
          @toggle-camera="toggleCamera"
        />

        <!-- Экран F.R.A.I -->
        <TFTScreenPanel
          v-model:isAvatarOn="isAvatarOn"
          :avatar-video="avatarVideo"
          :placeholder-text="placeholderText"
        />
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
                  <q-icon name="mic" size="48px" />
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
                  <q-icon name="volume_up" size="48px" />
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
import { ref, onBeforeUnmount } from 'vue'
import CameraPanel from 'components/camera/CameraPanel.vue'
import TFTScreenPanel from 'components/screen/TFTScreenPanel.vue'
import { useFraiDeviceStore } from 'src/stores/fraiDevice'
import { storeToRefs } from 'pinia'

const isMicOn = ref(true)
const micSignalLevel = ref(0.3)
const isSpeakerOn = ref(true)
const speakerSignalLevel = ref(0.4)

const isCameraOn = ref(false)
const actuatorAngleX = ref(90)
const actuatorAngleY = ref(90)
const cameraFps = ref(30)

const isAvatarOn = ref(true)
const avatarVideo = ref('')
const placeholderText = ref('Привет! Я F.R.A.I.')
const volume = ref(50)

const { tftResolution } = storeToRefs(useFraiDeviceStore())
const cameraPreview = {
  get width() {
    return tftResolution.value.width
  },
  get height() {
    return tftResolution.value.height
  }
}

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
  width: 500px;
  height: 380px;
}
</style>
