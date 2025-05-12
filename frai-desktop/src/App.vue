<template>
  <router-view />
</template>

<script setup lang="ts">
import { Dark } from 'quasar'

Dark.set(true)

defineOptions({
  name: 'App'
});
</script>
