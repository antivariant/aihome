<template>
  <!-- Quasar QImg для отображения картинки -->
  <q-img
    :src="msg.content"
    style="max-width: 200px; border-radius: 8px"
    spinner-color="primary"
  />
</template>

<script setup lang="ts">
defineProps<{
  msg: { content: string }
}>()
</script>

<style scoped>
/* при необходимости свои стили */
</style>
