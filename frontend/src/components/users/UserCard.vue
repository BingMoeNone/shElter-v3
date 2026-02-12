<script setup lang="ts">
import type { User } from '@/types'
import { useAuthStore } from '@/stores/auth'
import { connectionsApi } from '@/services/api'
import { ref, computed } from 'vue'

const props = defineProps<{
  user: User
  isFollowing: boolean
}>()

const emit = defineEmits<{
  connectionChanged: []
}>()

const authStore = useAuthStore()
const loading = ref(false)

const isOwnProfile = computed(() => {
  return authStore.user?.id === props.user.id
})

async function handleConnect(type: 'friend' | 'follow') {
  if (loading.value) return
  loading.value = true
  
  try {
    await connectionsApi.create({
      userId: props.user.id,
      connectionType: type,
    })
    emit('connectionChanged')
  } catch (error) {
    console.error('Failed to create connection:', error)
  } finally {
    loading.value = false
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
          <strong>{{ user.contributionCount }}</strong> contributions
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
        Follow
      </button>
      <button
        v-else
        disabled
        class="btn-following"
      >
        Following
      </button>
      <button
        @click="handleConnect('friend')"
        :disabled="loading"
        class="btn-friend"
      >
        Add Friend
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
}

.user-avatar {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  overflow: hidden;
  margin-bottom: 20px;
}

.user-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.avatar-placeholder {
  width: 100%;
  height: 100%;
  background: #42b883;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 48px;
  font-weight: bold;
}

.user-info h2 {
  margin: 0 0 4px;
  font-size: 1.5rem;
}

.username {
  color: #666;
  margin: 0 0 12px;
}

.bio {
  color: #444;
  line-height: 1.6;
  margin-bottom: 16px;
}

.stats {
  display: flex;
  gap: 24px;
  margin-bottom: 20px;
}

.stat {
  color: #666;
}

.stat strong {
  color: #333;
}

.user-actions {
  display: flex;
  gap: 12px;
}

.btn-follow,
.btn-friend {
  padding: 10px 24px;
}

.btn-following {
  background: #ccc;
  padding: 10px 24px;
}

.btn-friend {
  background: #666;
}

.btn-friend:hover:not(:disabled) {
  background: #555;
}
</style>
