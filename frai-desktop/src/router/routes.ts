import { RouteRecordRaw } from 'vue-router'
import MainLayout from 'layouts/MainLayout.vue'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    component: MainLayout,
    children: [
      { path: '', redirect: '/frai' },
      { path: 'frai', component: () => import('pages/FraiPage.vue') },
      { path: 'chat', component: () => import('pages/ChatPage.vue') },
      { path: 'logs', component: () => import('pages/LogsPage.vue') },
      { path: 'test', component: () => import('pages/TestPage.vue') },
      { path: 'devices', component: () => import('pages/DevicesPage.vue') },
    ]
  },

  // Always leave this as last one,
  // but you can also remove it
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/ErrorNotFound.vue')
  }
]

export default routes
