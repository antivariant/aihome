<!-- src/components/chat/TextMsg.vue -->
<template>
  <div>{{ msg.content }}</div>
</template>

<script setup lang="ts">
defineProps<{
  msg: { content: string }
}>()
</script>

<style scoped>
/* Ваши стили (если нужны) */
</style>
