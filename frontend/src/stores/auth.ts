import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { User } from '@/types'
import { authApi, usersApi } from '@/services/api'
import { useToastStore } from './toast'

export const useAuthStore = defineStore('auth', () => {
  const token = ref<string | null>(localStorage.getItem('token'))
  const refreshToken = ref<string | null>(localStorage.getItem('refreshToken'))
  const user = ref<User | null>(null)

  const isAuthenticated = computed(() => !!token.value && !!user.value)
  const isAdmin = computed(() => user.value?.role === 'admin')
  const isModerator = computed(() => user.value?.role === 'moderator' || user.value?.role === 'admin')

  function mapUser(data: any): User {
    return {
      id: data.id,
      username: data.username,
      email: data.email,
      displayName: data.display_name || data.displayName,
      bio: data.bio,
      avatarUrl: data.avatar_url || data.avatarUrl,
      isActive: data.is_active !== undefined ? data.is_active : data.isActive,
      role: data.role,
      createdAt: data.created_at || data.createdAt,
      updatedAt: data.updated_at || data.updatedAt,
      contributionCount: data.contribution_count || data.contributionCount || 0
    }
  }

  async function login(username: string, email: string, password: string): Promise<void> {
    try {
      const response = await authApi.login(username, email, password)
      // 适配 v3.1.0 统一响应格式: { data: {...}, message, status }
      const responseData = response.data.data || response.data

      const accessToken = responseData.access_token || responseData.accessToken
      const refreshTokenValue = responseData.refresh_token || responseData.refreshToken

      token.value = accessToken
      refreshToken.value = refreshTokenValue
      user.value = mapUser(responseData.user)

      localStorage.setItem('token', accessToken)
      localStorage.setItem('refreshToken', refreshTokenValue)

      useToastStore().success(`欢迎回来，${user.value?.displayName || user.value?.username}！`)
    } catch (error: any) {
      useToastStore().error(error.response?.data?.message || '登录失败，请检查用户名和密码')
      throw error
    }
  }

  async function register(userData: { username: string; email: string; password: string; displayName?: string }): Promise<void> {
    try {
      await usersApi.register(userData)
      await login(userData.username, userData.email, userData.password)
      useToastStore().success('注册成功！')
    } catch (error: any) {
      useToastStore().error(error.response?.data?.message || '注册失败')
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
      useToastStore().info('您已安全退出')
    }
  }

  async function fetchCurrentUser(): Promise<void> {
    if (!token.value) return
    
    try {
      const response = await usersApi.getMe()
      user.value = mapUser(response.data)
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
