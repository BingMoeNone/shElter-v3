import axios, { type AxiosInstance } from 'axios'
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
  login: (username: string, email: string, password: string) =>
    api.post('/auth/login', { username, email, password }),
  logout: () => api.post('/auth/logout'),
}

export const usersApi = {
  register: (data: { username: string; email: string; password: string; displayName?: string }) =>
    api.post('/users/', data),
  getMe: () => api.get('/users/me'),
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
  getByArticle: (articleId: string) => api.get(`/comments/article/${articleId}`),
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

export const metroApi = {
  getLines: () => api.get('/metro/lines'),
  getStations: () => api.get('/metro/stations'),
  getStationByKey: (pathKey: string) => api.get(`/metro/station/${pathKey}`),
}

export const musicApi = {
  getTracks: () => api.get('/music/tracks'),
  getAlbums: () => api.get('/music/albums'),
  getArtists: () => api.get('/music/artists'),
}

export const mediaApi = {
  uploadFile: (file: File) => {
    const formData = new FormData()
    formData.append('file', file)
    return api.post('/media/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
  },
  uploadMultipleFiles: (files: File[]) => {
    const formData = new FormData()
    files.forEach(file => {
      formData.append('files', file)
    })
    return api.post('/media/upload-multiple', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
  },
}

export const adminApi = {
  // Dashboard and Stats
  getModerationStats: () => api.get('/moderation/stats'),
  
  // Users Management
  getUsers: (params?: { page?: number; limit?: number; search?: string }) =>
    api.get('/admin/users', { params }),
  getUser: (userId: string) => api.get(`/admin/users/${userId}`),
  updateUser: (userId: string, data: any) => api.put(`/admin/users/${userId}`, data),
  resetPassword: (userId: string, data: { new_password: string }) =>
    api.post(`/admin/users/${userId}/reset-password`, data),
  deleteUser: (userId: string) => api.delete(`/admin/users/${userId}`),
  
  // Articles Management
  getArticles: (params?: { page?: number; limit?: number; search?: string; status?: string }) =>
    api.get('/articles', { params }),
  
  // Comments Management
  getComments: (params?: { page?: number; limit?: number; article_id?: string }) =>
    api.get('/comments/article/:article_id', { params }),
  
  // Moderation
  getPendingArticles: (params?: { page?: number; limit?: number }) =>
    api.get('/moderation/articles/pending', { params }),
  approveArticle: (articleId: string) => api.put(`/moderation/articles/${articleId}/approve`),
  rejectArticle: (articleId: string) => api.put(`/moderation/articles/${articleId}/reject`),
  
  getPendingComments: (params?: { page?: number; limit?: number; article_id?: string }) =>
    api.get('/moderation/comments/pending', { params }),
  approveComment: (commentId: string) => api.put(`/moderation/comments/${commentId}/approve`),
  rejectComment: (commentId: string) => api.put(`/moderation/comments/${commentId}/reject`),
  deleteComment: (commentId: string) => api.put(`/moderation/comments/${commentId}/delete`),
  
  // Audit Logs
  getLogs: (params?: { page?: number; limit?: number; user_id?: string; action?: string }) =>
    api.get('/admin/logs', { params }),
}
