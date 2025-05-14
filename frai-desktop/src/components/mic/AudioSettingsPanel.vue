<template>
  <q-card flat bordered class="frai-card full-height text-white">
    <q-card-section class="row items-center q-gutter-md full-height justify-between">

      <div class="column items-center q-gutter-sm">
        <q-icon name="volume_up" size="48px" />
        <div class="text-caption">Уровень</div>
      </div>

      <div class="column q-gutter-sm">
        <q-toggle v-model="audioOnModel" label="Звук" color="green" />
        <q-slider v-model="volumeModel" :min="0" :max="100" label />
        <div class="text-caption">Vol: {{ volume }}%</div>
      </div>
    </q-card-section>
  </q-card>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
  audioOn: boolean
  volume: number
}>()

const emit = defineEmits<{
  (e: 'update:audioOn', v: boolean): void
  (e: 'update:volume', v: number): void
}>()

const audioOnModel = computed({
  get: () => props.audioOn,
  set: v => emit('update:audioOn', v)
})
const volumeModel = computed({
  get: () => props.volume,
  set: v => emit('update:volume', v)
})

const { volume } = props
</script>

<style scoped>
.frai-card { background: #1e1e1e; }
</style>
