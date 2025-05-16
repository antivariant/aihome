import { defineStore } from 'pinia'

interface User {
  id: string
  name: string
  avatar: string
}

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null as User | null,
    token: null as string | null
  }),

  actions: {
    async login(username: string) {
      const lower = username.toLowerCase()

      if (lower === 'igor') {
        this.token = 'mocktoken-igor'
        this.user = {
          id: 'user123',
          name: 'Igor',
          avatar: '/avatars/igor.png'
        }
      } else if (lower === 'galina') {
        this.token = 'mocktoken-galina'
        this.user = {
          id: 'user124',
          name: 'Galina',
          avatar: '/avatars/galina.png'
        }
      } else {
        throw new Error('Unknown user')
      }
    },

    logout() {
      this.token = null
      this.user = null
    }
  }
})
