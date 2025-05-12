<template>
  <q-card class="q-pa-md">
    <q-card-section class="row items-center justify-between">
      <div class="text-h6">
        🎙️ Микрофон
      </div>
      <q-toggle
        v-model="micActive"
        label="Передача звука"
        color="green"
        left-label
      />
    </q-card-section>
  </q-card>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const micActive = ref(false)
</script>
