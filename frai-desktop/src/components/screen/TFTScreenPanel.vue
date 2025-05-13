<template>
  <div class="frai-block fixed-panel">
    <q-card flat bordered class="bg-grey-10 text-white full-height">
      <q-card-section class="row items-start q-gutter-md full-height">
        <!-- TFT экран -->
        <div
          class="frai-screen"
          :style="{ width: resolution.width + 'px', height: resolution.height + 'px' }"
        >
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

        <!-- Панель управления -->
        <div class="column justify-between" style="width: 140px;">
          <div class="column items-center q-mt-xs">
            <div class="text-h6 text-center">Экран F.R.A.I</div>
            <q-toggle
              :model-value="isAvatarOn"
              @update:model-value="val => emit('update:isAvatarOn', val)"
              label="Видео"
              color="green"
              class="self-center"
            />
            <div v-if="isAvatarOn" class="text-caption self-start">FPS: 25</div>
          </div>
          <div class="q-mb-sm" style="width: 100%;">
            <q-select
              v-model="store.tftResolution.label"
              :options="resolutions"
              emit-value
              map-options
              dense
              outlined
              label="Размер TFT"
              color="primary"
            />
          </div>
        </div>
      </q-card-section>
    </q-card>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useFraiDeviceStore } from 'src/stores/fraiDevice'

type TFTLabel = '1.8" 128x160' | '2.2" 240x320'

defineProps<{
  isAvatarOn: boolean
  avatarVideo: string
  placeholderText: string
}>()

const emit = defineEmits<{
  (e: 'update:isAvatarOn', val: boolean): void
}>()

const store = useFraiDeviceStore()

const resolutionMap: Record<TFTLabel, { width: number; height: number; label: TFTLabel }> = {
  '1.8" 128x160': { width: 128, height: 160, label: '1.8" 128x160' },
  '2.2" 240x320': { width: 240, height: 320, label: '2.2" 240x320' }
}

const resolutions = Object.keys(resolutionMap).map((key) => ({
  label: key,
  value: key
}))

const resolution = computed(() => {
  return resolutionMap[store.tftResolution.label as TFTLabel]
})
</script>

<style scoped>
.fixed-panel {
  width: 500px;
  height: 380px;
}
.frai-screen {
  background: black;
  position: relative;
  flex-shrink: 0;
  border: 1px solid white;
}
.frai-video {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
.frai-placeholder {
  color: white;
  font-size: 16px;
  padding: 10px;
  height: 100%;
  width: 100%;
  background: black;
}
</style>
