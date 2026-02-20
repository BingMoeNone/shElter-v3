<script setup lang="ts">
import { onMounted, ref, computed, watch } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { usersApi } from '@/services/api'
import { useToastStore } from '@/stores/toast'

const authStore = useAuthStore()
const toast = useToastStore()

const user = computed(() => authStore.user)
const saving = ref(false)
const error = ref<string | null>(null)

const displayName = ref('')
const bio = ref('')
const hasChanges = computed(() => {
  if (!user.value) return false
  return displayName.value !== (user.value.displayName || '') ||
         bio.value !== (user.value.bio || '')
})

onMounted(() => {
  if (user.value) {
    displayName.value = user.value.displayName || ''
    bio.value = user.value.bio || ''
  }
})

// Watch for user changes
watch(user, (newUser) => {
  if (newUser) {
    displayName.value = newUser.displayName || ''
    bio.value = newUser.bio || ''
  }
})

async function handleSave() {
  if (!user.value || !hasChanges.value || saving.value) return
  
  saving.value = true
  error.value = null
  
  try {
    const response = await usersApi.updateProfile(user.value.id, {
      displayName: displayName.value || undefined,
      bio: bio.value || undefined,
    })
    
    authStore.user = response.data
    toast.success('涓汉璧勬枡宸叉洿鏂帮紒')
  } catch (err: any) {
    error.value = err.response?.data?.message || '鏇存柊澶辫触'
    toast.error('淇濆瓨澶辫触锛岃閲嶈瘯')
    console.error(err)
  } finally {
    saving.value = false
  }
}

function formatDate(date: string) {
  return new Date(date).toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}
</script>

<template>
  <div class="profile-page">
    <h1>涓汉璧勬枡</h1>
    
    <div v-if="user" class="profile-content">
      <div class="profile-card card">
        <div class="form-group">
          <label for="username">鐢ㄦ埛鍚?/label>
          <input
            id="username"
            :value="user.username"
            disabled
          />
        </div>
        
        <div class="form-group">
          <label for="email">閭</label>
          <input
            id="email"
            :value="user.email"
            disabled
          />
        </div>
        
        <div class="form-group">
          <label for="displayName">鏄剧ず鍚嶇О</label>
          <input
            id="displayName"
            v-model="displayName"
            type="text"
            maxlength="50"
            placeholder="璁剧疆涓€涓樉绀哄悕绉?
          />
          <span class="char-count">{{ displayName.length }}/50</span>
        </div>
        
        <div class="form-group">
          <label for="bio">涓汉绠€浠?/label>
          <textarea
            id="bio"
            v-model="bio"
            rows="4"
            maxlength="500"
            placeholder="浠嬬粛涓€涓嬭嚜宸?.."
          ></textarea>
          <span class="char-count">{{ bio.length }}/500</span>
        </div>
        
        <div v-if="error" class="error-message">{{ error }}</div>
        
        <div class="form-actions">
          <button 
            @click="handleSave" 
            :disabled="!hasChanges || saving"
            class="btn-save"
          >
            <span v-if="saving" class="btn-spinner"></span>
            <span v-else>{{ saving ? '淇濆瓨涓?..' : '淇濆瓨鏇存敼' }}</span>
          </button>
        </div>
      </div>
      
      <div class="stats-card card">
        <h2>璐︽埛缁熻</h2>
        <div class="stat">
          <span class="label">璐＄尞鏁?/span>
          <span class="value">{{ user.contributionCount }}</span>
        </div>
        <div class="stat">
          <span class="label">瑙掕壊</span>
          <span class="value role-badge" :class="user.role">{{ user.role }}</span>
        </div>
        <div class="stat">
          <span class="label">娉ㄥ唽鏃堕棿</span>
          <span class="value">{{ formatDate(user.createdAt) }}</span>
        </div>
      </div>
    </div>
    
    <div v-else class="not-authenticated">
      <span class="lock-icon">馃敀</span>
      <p>璇?RouterLink to="/login">鐧诲綍</RouterLink>鏌ョ湅涓汉璧勬枡</p>
    </div>
  </div>
</template>

<style scoped>
.profile-page {
  max-width: 600px;
  margin: 0 auto;
}

.profile-page h1 {
  margin-bottom: 24px;
  color: var(--color-primary);
  text-shadow: 0 0 10px var(--color-primary);
}

.profile-content {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.profile-card,
.stats-card {
  background: var(--color-surface);
  border: 1px solid var(--color-primary);
  box-shadow: 0 0 15px rgba(0, 255, 157, 0.1);
}

.profile-card .form-group {
  margin-bottom: 20px;
  position: relative;
}

.profile-card label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  color: var(--color-text);
}

.profile-card input,
.profile-card textarea {
  background: rgba(0, 0, 0, 0.5);
  border: 1px solid var(--color-border);
  color: var(--color-text);
  padding: 12px;
  width: 100%;
  border-radius: 4px;
  transition: all 0.3s;
}

.profile-card input:focus,
.profile-card textarea:focus {
  border-color: var(--color-primary);
  box-shadow: 0 0 10px rgba(0, 255, 157, 0.2);
  outline: none;
}

.profile-card input:disabled {
  background: rgba(255, 255, 255, 0.05);
  cursor: not-allowed;
  color: var(--color-text-muted);
  border-color: var(--color-border);
}

.profile-card textarea {
  resize: vertical;
  min-height: 100px;
}

.char-count {
  position: absolute;
  right: 8px;
  bottom: 8px;
  font-size: 0.75rem;
  color: var(--color-text-muted);
}

.error-message {
  color: #ff4444;
  padding: 12px;
  background: rgba(255, 68, 68, 0.1);
  border-radius: 4px;
  margin-bottom: 16px;
  border-left: 3px solid #ff4444;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
}

.btn-save {
  padding: 12px 32px;
  background: rgba(0, 255, 157, 0.1);
  border: 1px solid var(--color-primary);
  color: var(--color-primary);
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  gap: 8px;
}

.btn-save:hover:not(:disabled) {
  background: var(--color-primary);
  color: #000;
  box-shadow: 0 0 15px var(--color-primary);
}

.btn-save:disabled {
  opacity: 0.5;
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

.stats-card h2 {
  font-size: 1.25rem;
  margin-bottom: 16px;
  color: var(--color-secondary);
  text-shadow: 0 0 5px var(--color-secondary);
}

.stat {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 0;
  border-bottom: 1px solid var(--color-border);
}

.stat:last-child {
  border-bottom: none;
}

.stat .label {
  color: var(--color-text-muted);
}

.stat .value {
  font-weight: 500;
  color: var(--color-accent);
}

.role-badge {
  padding: 4px 12px;
  border-radius: 4px;
  font-size: 0.85rem;
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

.not-authenticated {
  text-align: center;
  padding: 60px;
  color: var(--color-text-muted);
}

.lock-icon {
  font-size: 3rem;
  display: block;
  margin-bottom: 16px;
}

.not-authenticated a {
  color: var(--color-primary);
  font-weight: bold;
}
</style>
