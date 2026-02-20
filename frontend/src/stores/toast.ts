import { defineStore } from 'pinia'
import { ref } from 'vue'

export interface Toast {
  id: string
  type: 'success' | 'error' | 'warning' | 'info'
  message: string
  duration?: number
}

export const useToastStore = defineStore('toast', () => {
  const toasts = ref<Toast[]>([])

  function addToast(type: Toast['type'], message: string, duration = 3000) {
    const id = Math.random().toString(36).substring(2, 9)
    const toast: Toast = { id, type, message, duration }
    toasts.value.push(toast)

    if (duration > 0) {
      setTimeout(() => {
        removeToast(id)
      }, duration)
    }

    return id
  }

  function removeToast(id: string) {
    const index = toasts.value.findIndex(t => t.id === id)
    if (index > -1) {
      toasts.value.splice(index, 1)
    }
  }

  function success(message: string, duration?: number) {
    return addToast('success', message, duration)
  }

  function error(message: string, duration?: number) {
    return addToast('error', message, duration)
  }

  function warning(message: string, duration?: number) {
    return addToast('warning', message, duration)
  }

  function info(message: string, duration?: number) {
    return addToast('info', message, duration)
  }

  return {
    toasts,
    addToast,
    removeToast,
    success,
    error,
    warning,
    info,
  }
})
