<template>
  <q-card flat bordered class="camera-panel">
    <div class="camera-grid">
      <!-- 1. Preview-window -->
      <div class="preview-container">
        <video
          ref="cameraVideo"
          class="preview-video"
          autoplay
          muted
          playsinline
          :style="videoStyle"
        />
      </div>

      <!-- 2. Controls -->
      <div class="controls-container">
        <!-- Заголовок -->
        <div class="header-block">
          <div class="camera-title">Камера</div>
        </div>

        <!-- Переключатель + FPS -->
        <div class="indicators-block">
          <q-toggle v-model="cameraOnModel" label="Трансляция" color="green" />
          <div class="fps-text">FPS: {{ cameraFpsModel }}</div>
        </div>

        <!-- Список ползунков -->
        <q-list dense class="sliders-list">
          <!-- FPS -->
          <q-item>
            <q-item-section avatar>
              <q-icon name="timer" color="blue" />
            </q-item-section>
            <q-item-section>
              <q-slider
                v-model="cameraFpsModel"
                :min="1"
                :max="60"
                label
                track-color="grey-7"
                thumb-color="blue"
              />
            </q-item-section>
          </q-item>

          <!-- Горизонт -->
          <q-item>
            <q-item-section avatar>
              <q-icon name="swap_horiz" color="blue" />
            </q-item-section>
            <q-item-section>
              <q-slider
                v-model="actuatorAngleXModel"
                :min="0"
                :max="180"
                label
                track-color="grey-7"
                thumb-color="blue"
              />
            </q-item-section>
          </q-item>

          <!-- Вертикаль -->
          <q-item>
            <q-item-section avatar>
              <q-icon name="swap_vert" color="blue" />
            </q-item-section>
            <q-item-section>
              <q-slider
                v-model="actuatorAngleYModel"
                :min="0"
                :max="180"
                label
                track-color="grey-7"
                thumb-color="blue"
              />
            </q-item-section>
          </q-item>

          <!-- Масштаб -->
          <q-item>
            <q-item-section avatar>
              <q-icon name="zoom_in" color="blue" />
            </q-item-section>
            <q-item-section>
              <q-slider
                v-model="videoScaleModel"
                :min="1"
                :max="4"
                :step="0.1"
                label
                track-color="grey-7"
                thumb-color="blue"
              />
            </q-item-section>
          </q-item>
        </q-list>
      </div>
    </div>
  </q-card>
</template>

<script setup lang="ts">
import { ref, defineProps, defineEmits, watch, computed, onMounted } from 'vue'

const props = defineProps<{
  cameraOn: boolean
  cameraFps: number
  actuatorAngleX: number
  actuatorAngleY: number
}>()

const emit = defineEmits<{
  (e: 'update:cameraOn', val: boolean): void
  (e: 'update:cameraFps', val: number): void
  (e: 'update:actuatorAngleX', val: number): void
  (e: 'update:actuatorAngleY', val: number): void
}>()

const cameraOnModel = ref(props.cameraOn)
const cameraFpsModel = ref(props.cameraFps)
const actuatorAngleXModel = ref(props.actuatorAngleX)
const actuatorAngleYModel = ref(props.actuatorAngleY)
const videoScaleModel = ref(2)

watch(cameraOnModel, v => emit('update:cameraOn', v))
watch(cameraFpsModel, v => emit('update:cameraFps', v))
watch(actuatorAngleXModel, v => emit('update:actuatorAngleX', v))
watch(actuatorAngleYModel, v => emit('update:actuatorAngleY', v))

const cameraVideo = ref<HTMLVideoElement | null>(null)
async function startStream() {
  if (!cameraVideo.value) return
  try {
    const s = await navigator.mediaDevices.getUserMedia({ video: true })
    cameraVideo.value.srcObject = s
  } catch (err) { console.error(err) }
}
function stopStream() {
  if (!cameraVideo.value) return
  const st = cameraVideo.value.srcObject as MediaStream | null
  st?.getTracks().forEach(t => t.stop())
  cameraVideo.value.srcObject = null
}

onMounted(() => { if (cameraOnModel.value) startStream() })
watch(cameraOnModel, on => on ? startStream() : stopStream())

// базовый сдвиг при масштабировании
const baseOffset = computed(() => -(videoScaleModel.value - 1) * 50)
// сдвиги по углам
const angleOffsetX = computed(() =>
  ((actuatorAngleXModel.value - 90) / 90) * 50
)
const angleOffsetY = computed(() =>
  ((actuatorAngleYModel.value - 90) / 90) * 50
)
// итоговый стиль для <video>
const videoStyle = computed(() => ({
  width: `${videoScaleModel.value * 100}%`,
  height: `${videoScaleModel.value * 100}%`,
  transform: `
    translate(
      ${baseOffset.value + angleOffsetX.value}%,
      ${baseOffset.value + angleOffsetY.value}%
    )
  `
}))
</script>


<style scoped>
.camera-panel {
  height: 100%;
  padding: 20px;
  box-sizing: border-box;
}
.camera-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  height: 100%;
}

.preview-container {
  position: relative;
  background: #000;
  aspect-ratio: 4 / 3;
  overflow: hidden;
}
.preview-video {
  position: absolute;
  top: 0;
  left: 0;
}

.controls-container {
  display: flex;
  flex-direction: column;
  row-gap: 20px;
  height: 100%;
}
.header-block {
  display: flex;
  justify-content: center;
}
.camera-title {
  font-size: 1.25rem;
  font-weight: 500;
}
.indicators-block {
  display: flex;
  align-items: center;
  column-gap: 12px;
}
.fps-text {
  font-size: 1rem;
}
.sliders-list {
  flex-grow: 1;
  overflow-y: auto;
}
</style>
