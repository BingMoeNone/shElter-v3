import axios, { type AxiosInstance, type AxiosResponse } from 'axios'
import { useAuthStore } from '@/stores/auth'

const api: AxiosInstance = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1',
  headers: {
    'Content-Type': 'application/json',
  },
})

api.interceptors.request.use(
  (config) => {
    const authStore = useAuthStore()
    if (authStore.token) {
      config.headers.Authorization = `Bearer ${authStore.token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      const authStore = useAuthStore()
      authStore.logout()
    }
    return Promise.reject(error)
  }
)

export default api

export const authApi = {
  login: (username: string, password: string) =>
    api.post('/auth/login', { username, password }),
  logout: () => api.post('/auth/logout'),
}

export const usersApi = {
  register: (data: { username: string; email: string; password: string; displayName?: string }) =>
    api.post('/users/', data),
  getProfile: (userId: string) => api.get(`/users/${userId}`),
  updateProfile: (userId: string, data: { displayName?: string; bio?: string; avatarUrl?: string }) =>
    api.put(`/users/${userId}`, data),
  list: (params?: { page?: number; limit?: number; search?: string }) =>
    api.get('/users/', { params }),
}

export const articlesApi = {
  create: (data: { title: string; content: string; summary?: string; status?: string; categoryIds?: string[]; tagNames?: string[] }) =>
    api.post('/articles/', data),
  get: (articleId: string) => api.get(`/articles/${articleId}`),
  update: (articleId: string, data: { title?: string; content?: string; summary?: string; status?: string; categoryIds?: string[]; tagNames?: string[] }) =>
    api.put(`/articles/${articleId}`, data),
  delete: (articleId: string) => api.delete(`/articles/${articleId}`),
  publish: (articleId: string) => api.post(`/articles/${articleId}/publish`),
  list: (params?: { page?: number; limit?: number; status?: string; category?: string; tag?: string; search?: string }) =>
    api.get('/articles/', { params }),
  getRevisions: (articleId: string) => api.get(`/articles/${articleId}/revisions`),
}

export const categoriesApi = {
  list: (params?: { page?: number; limit?: number }) => api.get('/categories/', { params }),
  get: (categoryId: string) => api.get(`/categories/${categoryId}`),
  create: (data: { name: string; description?: string; parentId?: string }) =>
    api.post('/categories/', data),
}

export const tagsApi = {
  list: (params?: { page?: number; limit?: number }) => api.get('/tags/', { params }),
  get: (tagId: string) => api.get(`/tags/${tagId}`),
  create: (data: { name: string }) => api.post('/tags/', data),
}

export const commentsApi = {
  create: (data: { articleId: string; content: string; parentId?: string }) =>
    api.post('/comments/', data),
  update: (commentId: string, data: { content: string }) =>
    api.put(`/comments/${commentId}`, data),
  delete: (commentId: string) => api.delete(`/comments/${commentId}`),
}

export const connectionsApi = {
  create: (data: { userId: string; connectionType: 'friend' | 'follow' }) =>
    api.post('/connections/', data),
  accept: (connectionId: string) => api.post(`/connections/${connectionId}/accept`),
  delete: (connectionId: string) => api.delete(`/connections/${connectionId}`),
}

export const searchApi = {
  search: (query: string, params?: { page?: number; limit?: number }) =>
    api.get('/search/', { params: { q: query, ...params } }),
}
