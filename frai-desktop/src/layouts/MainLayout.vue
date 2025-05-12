<template>
  <q-layout view="lHh Lpr lFf">
    <q-header elevated>
      <q-toolbar>
        <q-btn
          flat
          dense
          round
          icon="menu"
          aria-label="Меню"
          @click="leftDrawerOpen = !leftDrawerOpen"
        />
        <q-toolbar-title>
          F.R.A.I Desktop
        </q-toolbar-title>
        <div>Quasar v{{ $q.version }}</div>
      </q-toolbar>
    </q-header>

    <q-drawer v-model="leftDrawerOpen"
              bordered
              behavior="default"
              :width="200">
      <q-list>
        <q-item-label header>Навигация</q-item-label>

        <q-item clickable v-ripple to="/frai" @click="leftDrawerOpen = false">
          <q-item-section avatar><q-icon name="smart_toy" /></q-item-section>
          <q-item-section>Frai</q-item-section>
        </q-item>

        <q-item clickable v-ripple to="/chat" @click="leftDrawerOpen = false">
          <q-item-section avatar><q-icon name="chat" /></q-item-section>
          <q-item-section>Chat</q-item-section>
        </q-item>

        <q-item clickable v-ripple to="/logs" @click="leftDrawerOpen = false">
          <q-item-section avatar><q-icon name="list_alt" /></q-item-section>
          <q-item-section>Logs</q-item-section>
        </q-item>

        <q-item clickable v-ripple to="/test" @click="leftDrawerOpen = false">
          <q-item-section avatar><q-icon name="developer_board" /></q-item-section>
          <q-item-section>Test</q-item-section>
        </q-item>

        <q-item clickable v-ripple to="/devices" @click="leftDrawerOpen = false">
          <q-item-section avatar><q-icon name="sensors" /></q-item-section>
          <q-item-section>Devices</q-item-section>
        </q-item>
      </q-list>
    </q-drawer>

    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useQuasar } from 'quasar'

const $q = useQuasar()
const leftDrawerOpen = ref(false)
</script>
