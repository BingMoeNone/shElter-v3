<script setup lang="ts">
import { useToastStore } from '@/stores/toast'

const toastStore = useToastStore()

function getIcon(type: string) {
  switch (type) {
    case 'success': return '鉁?
    case 'error': return '鉁?
    case 'warning': return '鈿?
    case 'info': return '鈩?
    default: return '鈥?
  }
}
</script>

<template>
  <Teleport to="body">
    <div class="toast-container">
      <TransitionGroup name="toast">
        <div
          v-for="toast in toastStore.toasts"
          :key="toast.id"
          class="toast"
          :class="`toast-${toast.type}`"
        >
          <span class="toast-icon">{{ getIcon(toast.type) }}</span>
          <span class="toast-message">{{ toast.message }}</span>
          <button
            class="toast-close"
            @click="toastStore.removeToast(toast.id)"
          >
            鉁?          </button>
        </div>
      </TransitionGroup>
    </div>
  </Teleport>
</template>

<style scoped>
.toast-container {
  position: fixed;
  top: 20px;
  right: 20px;
  z-index: 9999;
  display: flex;
  flex-direction: column;
  gap: 10px;
  pointer-events: none;
}

.toast {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 16px;
  border-radius: 8px;
  background: #1a1a1a;
  border: 1px solid;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
  pointer-events: auto;
  min-width: 280px;
  max-width: 400px;
}

.toast-success {
  border-color: #00ff88;
  background: rgba(0, 255, 136, 0.1);
}

.toast-error {
  border-color: #ff4444;
  background: rgba(255, 68, 68, 0.1);
}

.toast-warning {
  border-color: #ffaa00;
  background: rgba(255, 170, 0, 0.1);
}

.toast-info {
  border-color: #4488ff;
  background: rgba(68, 136, 255, 0.1);
}

.toast-icon {
  font-size: 1.2rem;
  font-weight: bold;
}

.toast-success .toast-icon { color: #00ff88; }
.toast-error .toast-icon { color: #ff4444; }
.toast-warning .toast-icon { color: #ffaa00; }
.toast-info .toast-icon { color: #4488ff; }

.toast-message {
  flex: 1;
  color: #fff;
  font-size: 0.95rem;
}

.toast-close {
  background: none;
  border: none;
  color: #888;
  cursor: pointer;
  font-size: 1rem;
  padding: 0;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 4px;
  transition: all 0.2s;
}

.toast-close:hover {
  background: rgba(255, 255, 255, 0.1);
  color: #fff;
}

/* Transitions */
.toast-enter-active,
.toast-leave-active {
  transition: all 0.3s ease;
}

.toast-enter-from {
  opacity: 0;
  transform: translateX(100%);
}

.toast-leave-to {
  opacity: 0;
  transform: translateX(100%);
}

@media (max-width: 600px) {
  .toast-container {
    left: 20px;
    right: 20px;
  }
  
  .toast {
    max-width: 100%;
    min-width: auto;
  }
}
</style>
