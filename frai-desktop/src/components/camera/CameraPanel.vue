<template>
  <q-card flat bordered class="bg-grey-10 text-white full-height">
    <q-card-section class="row items-start q-gutter-md full-height justify-between">

      <!-- Превью камеры -->
      <div
        class="frai-frame"
        :style="{
          width: previewWidth + 'px',
          height: previewHeight + 'px'
        }"
      >
        <video
          ref="cameraVideo"
          autoplay
          muted
          class="frai-video"
          :style="{ objectPosition: objectPosition }"
        />
      </div>

      <!-- Панель управления -->
      <div class="column q-gutter-sm items-start">
        <div class="text-h6">Камера</div>

        <q-toggle
          v-model="cameraOnModel"
          label="Трансляция"
          color="green"
        />

        <div class="text-caption">FPS: {{ cameraFps }}</div>

        <q-slider
          v-model="actuatorXModel"
          :min="0"
          :max="180"
          label
        />
        <div class="text-caption">
          Горизонт: {{ actuatorAngleX }}°
        </div>

        <q-slider
          v-model="actuatorYModel"
          :min="0"
          :max="180"
          label
        />
        <div class="text-caption">
          Вертикаль: {{ actuatorAngleY }}°
        </div>
      </div>
    </q-card-section>
  </q-card>
</template>

<script setup lang="ts">
import { ref, watch, onMounted, computed } from 'vue'

/* ==== Props ==== */
const props = defineProps<{
  cameraOn: boolean
  cameraFps: number
  actuatorAngleX: number
  actuatorAngleY: number
  previewWidth: number
  previewHeight: number
}>()

/* ==== Emits и v-model ==== */
const emit = defineEmits<{
  (e: 'update:camera-on', v: boolean): void
  (e: 'update:actuator-angle-x', v: number): void
  (e: 'update:actuator-angle-y', v: number): void
}>()

const cameraOnModel = computed<boolean>({
  get:  () => props.cameraOn,
  set: v => emit('update:camera-on', v)
})

const actuatorXModel = computed<number>({
  get:  () => props.actuatorAngleX,
  set: v => emit('update:actuator-angle-x', v)
})

const actuatorYModel = computed<number>({
  get:  () => props.actuatorAngleY,
  set: v => emit('update:actuator-angle-y', v)
})

/* ==== Видео ==== */
const cameraVideo = ref<HTMLVideoElement | null>(null)

watch(cameraOnModel, enabled => {
  const vid = cameraVideo.value
  if (!vid) return

  if (enabled) {
    navigator.mediaDevices.getUserMedia({ video: true })
      .then(stream => { vid.srcObject = stream })
      .catch(console.error)
  }
  else {
    const s = vid.srcObject as MediaStream | null
    s?.getTracks().forEach(t => t.stop())
    vid.srcObject = null
  }
})

onMounted(() => {
  if (cameraOnModel.value && cameraVideo.value) {
    navigator.mediaDevices.getUserMedia({ video: true })
      .then(stream => {
        if (cameraVideo.value) {
          cameraVideo.value.srcObject = stream
        }
      })
      .catch(console.error)
  }
})

/* ==== Смещение видео (object-position: –50%…150%) ==== */
const objectPosition = computed(() => {
  // 0°→180° → –50…150%
  const x = (props.actuatorAngleX / 180) * 200 - 50
  const y = (props.actuatorAngleY / 180) * 200 - 50
  return `${x}% ${y}%`
})

/* ==== Быстрые ссылки на props для шаблона ==== */
const {
  cameraFps,
  actuatorAngleX,
  actuatorAngleY,
  previewWidth,
  previewHeight
} = props
</script>

<style scoped>
.frai-frame {
  position: relative;
  overflow: hidden;
  background: black;
}

.frai-video {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  /* object-position задаётся inline-стилем через computed */
}
</style>
