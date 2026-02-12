import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { User, LoginResponse } from '@/types'
import { authApi, usersApi } from '@/services/api'

export const useAuthStore = defineStore('auth', () => {
  const token = ref<string | null>(localStorage.getItem('token'))
  const refreshToken = ref<string | null>(localStorage.getItem('refreshToken'))
  const user = ref<User | null>(null)

  const isAuthenticated = computed(() => !!token.value && !!user.value)
  const isAdmin = computed(() => user.value?.role === 'admin')
  const isModerator = computed(() => user.value?.role === 'moderator' || user.value?.role === 'admin')

  async function login(username: string, password: string): Promise<void> {
    try {
      const response = await authApi.login(username, password)
      const data: LoginResponse = response.data
      
      token.value = data.accessToken
      refreshToken.value = data.refreshToken
      user.value = data.user
      
      localStorage.setItem('token', data.accessToken)
      localStorage.setItem('refreshToken', data.refreshToken)
    } catch (error) {
      throw error
    }
  }

  async function register(userData: { username: string; email: string; password: string; displayName?: string }): Promise<void> {
    try {
      await usersApi.register(userData)
      await login(userData.username, userData.password)
    } catch (error) {
      throw error
    }
  }

  async function logout(): Promise<void> {
    try {
      await authApi.logout()
    } catch (error) {
      console.error('Logout error:', error)
    } finally {
      token.value = null
      refreshToken.value = null
      user.value = null
      localStorage.removeItem('token')
      localStorage.removeItem('refreshToken')
    }
  }

  async function fetchCurrentUser(): Promise<void> {
    if (!token.value) return
    
    try {
      const response = await usersApi.getProfile(user.value?.id || '')
      user.value = response.data
    } catch (error) {
      logout()
    }
  }

  function initAuth(): void {
    const storedToken = localStorage.getItem('token')
    if (storedToken) {
      token.value = storedToken
      fetchCurrentUser()
    }
  }

  return {
    token,
    refreshToken,
    user,
    isAuthenticated,
    isAdmin,
    isModerator,
    login,
    register,
    logout,
    fetchCurrentUser,
    initAuth,
  }
})
