<template>
  <q-scroll-area class="fit q-pa-md">
    <div class="column q-gutter-sm" style="max-width: 100%;">
      <div style="width: 100%; max-width: 480px; margin: auto">
        <q-chat-message
          v-for="entry in logs"
          :key="entry._id"
          :avatar="getAvatar(entry.actor)"
          :name="entry.profile?.name"
          :text="[entry.message]"
          :stamp="formatStamp(entry)"
          :sent="entry.actor === 'ai-engine'"
          :bg-color="bgColor(entry.actor)"
          text-color="black"
        />
      </div>
    </div>
  </q-scroll-area>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import { useChatStore } from 'src/stores/chat'
import { apiHub } from 'src/api'

interface HumanLogEntry {
  _id: string
  timestamp: string
  actor: string
  target: string
  message: string
  session_id: string
  interaction_id: string
  profile: {
    name: string
    avatar: string
  }
}

const chatStore = useChatStore()
const logs = ref<HumanLogEntry[]>([])
const avatarMap = ref(new Map<string, string>())
const hubBaseURL = apiHub.defaults.baseURL || ''  // ✅ получаем http://localhost:5105

watch(
  () => chatStore.interaction_id,
  async (newId) => {
    if (!newId) return
    try {
      const res = await apiHub.get(`/human-log?interaction_id=${newId}`)
      logs.value = res.data
      avatarMap.value.clear()

      // 1. Аватары по actor
      for (const log of logs.value) {
        if (log.actor && log.profile?.avatar) {
          avatarMap.value.set(log.actor, `${hubBaseURL}${log.profile.avatar}`)
        }
      }

      // 2. Аватары по target, если не добавлены
      for (const log of logs.value) {
        if (log.target && !avatarMap.value.has(log.target)) {
          const match = logs.value.find(
            l => l.actor === log.target && l.profile?.avatar
          )
          if (match) {
            avatarMap.value.set(log.target, `${hubBaseURL}${match.profile.avatar}`)
          } else {
            avatarMap.value.set(log.target, `${hubBaseURL}/avatars/${log.target}.png`)
          }
        }
      }
    } catch (err) {
      console.error('Ошибка получения human log:', err)
    }
  },
  { immediate: true }
)

function formatStamp(entry: HumanLogEntry) {
  const time = new Date(entry.timestamp).toLocaleTimeString([], {
    hour: '2-digit',
    minute: '2-digit'
  })
  return `${entry.actor} → ${entry.target} • ${time}`
}

function bgColor(actor: string): string {
  switch (actor) {
    case 'gw-chat':
      return 'green-3'
    case 'gw-hub':
      return 'grey-3'
    case 'ai-engine':
      return 'amber-2'
    default:
      return 'blue-grey-1'
  }
}

function getAvatar(system: string): string {
  return avatarMap.value.get(system) || `${hubBaseURL}/avatars/default.png`
}
</script>

<style scoped>
::v-deep(.q-message-avatar) {
  background: white !important;
  border-radius: 20% !important;
  padding: 2px;
  width: 40px !important;
  height: 40px !important;
  box-shadow: 0 0 0 1px rgba(0, 0, 0, 0.15); /* лёгкая обводка */
}

::v-deep(.q-message-avatar img) {
  object-fit: contain !important;
  width: 15px !important;     /* ⬅ стало меньше */
  height: 15px !important;
  margin: 10px;
  display: block;
  background: white;
  border-radius: 0 !important;
}
</style>
