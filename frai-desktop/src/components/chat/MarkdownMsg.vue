<template>
  <!-- Quasar-плагин q-markdown -->
  <q-markdown :src="msg.content" />
</template>

<script setup lang="ts">
defineProps<{
  msg: { content: string }
}>()
</script>

<style scoped>
/* при необходимости свои стили */
</style>
