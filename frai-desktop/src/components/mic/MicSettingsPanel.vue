<template>
  <q-card flat bordered class="frai-card full-height text-white">
    <q-card-section class="row items-center q-gutter-md full-height justify-between">

      <div class="column items-center q-gutter-sm">
        <q-icon name="mic" size="48px" />
        <div class="text-caption">Уровень</div>
      </div>

      <div class="column q-gutter-sm">
        <q-toggle v-model="micOnModel" label="Микрофон" color="green" />
        <q-slider v-model="micGainModel" :min="0" :max="100" label />
        <div class="text-caption">Gain: {{ micGain }}%</div>
      </div>
    </q-card-section>
  </q-card>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
  micOn: boolean
  micGain: number
}>()

const emit = defineEmits<{
  (e: 'update:micOn', v: boolean): void
  (e: 'update:micGain', v: number): void
}>()

const micOnModel = computed({
  get: () => props.micOn,
  set: v => emit('update:micOn', v)
})
const micGainModel = computed({
  get: () => props.micGain,
  set: v => emit('update:micGain', v)
})

const { micGain } = props
</script>

<style scoped>
.frai-card { background: #1e1e1e; }
</style>
