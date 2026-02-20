<script setup lang="ts">
import type { User, UserProfile } from '@/types'
import { useAuthStore } from '@/stores/auth'
import { connectionsApi } from '@/services/api'
import { ref, computed } from 'vue'
import { useToastStore } from '@/stores/toast'

const props = defineProps<{
  user: User | UserProfile
  isFollowing: boolean
}>()

const emit = defineEmits<{
  connectionChanged: []
}>()

const authStore = useAuthStore()
const toast = useToastStore()
const loading = ref(false)
const actionType = ref<'follow' | 'friend' | null>(null)

const isOwnProfile = computed(() => {
  return authStore.user?.id === props.user.id
})

async function handleConnect(type: 'friend' | 'follow') {
  if (loading.value) return
  loading.value = true
  actionType.value = type
  
  try {
    await connectionsApi.create({
      userId: props.user.id,
      connectionType: type,
    })
    emit('connectionChanged')
    
    if (type === 'follow') {
      toast.success(`宸插叧娉?${props.user.displayName || props.user.username}`)
    } else {
      toast.success(`宸插悜 ${props.user.displayName || props.user.username} 鍙戦€佸ソ鍙嬭姹俙)
    }
  } catch (err: any) {
    console.error('Failed to create connection:', err)
    toast.error(err.response?.data?.message || '鎿嶄綔澶辫触锛岃閲嶈瘯')
  } finally {
    loading.value = false
    actionType.value = null
  }
}
</script>

<template>
  <div class="user-card card">
    <div class="user-avatar">
      <img
        v-if="user.avatarUrl"
        :src="user.avatarUrl"
        :alt="user.displayName || user.username"
      />
      <div v-else class="avatar-placeholder">
        {{ (user.displayName || user.username).charAt(0).toUpperCase() }}
      </div>
    </div>
    
    <div class="user-info">
      <h2>{{ user.displayName || user.username }}</h2>
      <p class="username">@{{ user.username }}</p>
      <p v-if="user.bio" class="bio">{{ user.bio }}</p>
      
      <div class="stats">
        <span class="stat">
          <strong>{{ user.contributionCount }}</strong> 璐＄尞
        </span>
        <span v-if="'role' in user" class="stat role-badge" :class="user.role">
          {{ user.role }}
        </span>
      </div>
    </div>
    
    <div v-if="!isOwnProfile && authStore.isAuthenticated" class="user-actions">
      <button
        v-if="!isFollowing"
        @click="handleConnect('follow')"
        :disabled="loading"
        class="btn-follow"
      >
        <span v-if="loading && actionType === 'follow'" class="btn-spinner"></span>
        <span v-else>鍏虫敞</span>
      </button>
      <button
        v-else
        disabled
        class="btn-following"
      >
        宸插叧娉?      </button>
      <button
        @click="handleConnect('friend')"
        :disabled="loading"
        class="btn-friend"
      >
        <span v-if="loading && actionType === 'friend'" class="btn-spinner"></span>
        <span v-else>娣诲姞濂藉弸</span>
      </button>
    </div>
  </div>
</template>

<style scoped>
.user-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  padding: 32px;
  background: var(--color-surface);
  border: 1px solid var(--color-primary);
  box-shadow: 0 0 15px rgba(0, 255, 157, 0.1);
}

.user-avatar {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  overflow: hidden;
  margin-bottom: 20px;
  border: 3px solid var(--color-primary);
  box-shadow: 0 0 15px rgba(0, 255, 157, 0.3);
}

.user-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.avatar-placeholder {
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, var(--color-primary), var(--color-secondary));
  color: #000;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 48px;
  font-weight: bold;
}

.user-info h2 {
  margin: 0 0 4px;
  font-size: 1.5rem;
  color: var(--color-primary);
  text-shadow: 0 0 5px var(--color-primary);
}

.username {
  color: var(--color-text-muted);
  margin: 0 0 12px;
}

.bio {
  color: var(--color-text);
  line-height: 1.6;
  margin-bottom: 16px;
  max-width: 400px;
}

.stats {
  display: flex;
  gap: 16px;
  margin-bottom: 20px;
  flex-wrap: wrap;
  justify-content: center;
}

.stat {
  color: var(--color-text-muted);
  display: flex;
  align-items: center;
  gap: 4px;
}

.stat strong {
  color: var(--color-accent);
}

.role-badge {
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 0.8rem;
  text-transform: uppercase;
}

.role-badge.admin {
  background: rgba(255, 68, 68, 0.2);
  color: #ff4444;
}

.role-badge.moderator {
  background: rgba(255, 170, 0, 0.2);
  color: #ffaa00;
}

.role-badge.user {
  background: rgba(0, 255, 157, 0.2);
  color: var(--color-primary);
}

.user-actions {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
  justify-content: center;
}

.btn-follow,
.btn-friend {
  padding: 10px 24px;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  justify-content: center;
  min-width: 100px;
}

.btn-follow {
  background: rgba(0, 255, 157, 0.1);
  border: 1px solid var(--color-primary);
  color: var(--color-primary);
}

.btn-follow:hover:not(:disabled) {
  background: var(--color-primary);
  color: #000;
  box-shadow: 0 0 15px var(--color-primary);
}

.btn-following {
  padding: 10px 24px;
  border-radius: 4px;
  background: rgba(0, 255, 157, 0.2);
  border: 1px solid var(--color-primary);
  color: var(--color-primary);
  cursor: default;
}

.btn-friend {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid var(--color-text-muted);
  color: var(--color-text);
}

.btn-friend:hover:not(:disabled) {
  background: rgba(255, 255, 255, 0.1);
  border-color: var(--color-text);
}

button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-spinner {
  width: 16px;
  height: 16px;
  border: 2px solid transparent;
  border-top-color: currentColor;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>
