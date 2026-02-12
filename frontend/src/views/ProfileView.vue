<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { usersApi } from '@/services/api'
import type { User } from '@/types'

const authStore = useAuthStore()

const user = ref<User | null>(null)
const loading = ref(false)
const saving = ref(false)
const error = ref<string | null>(null)
const success = ref<string | null>(null)

const displayName = ref('')
const bio = ref('')

onMounted(async () => {
  if (authStore.user) {
    user.value = authStore.user
    displayName.value = user.value.displayName || ''
    bio.value = user.value.bio || ''
  }
})

async function handleSave() {
  if (!user.value) return
  
  saving.value = true
  error.value = null
  success.value = null
  
  try {
    const response = await usersApi.updateProfile(user.value.id, {
      displayName: displayName.value || undefined,
      bio: bio.value || undefined,
    })
    
    user.value = response.data
    authStore.user = response.data
    success.value = 'Profile updated successfully!'
  } catch (err) {
    error.value = 'Failed to update profile'
    console.error(err)
  } finally {
    saving.value = false
  }
}
</script>

<template>
  <div class="profile-page">
    <h1>My Profile</h1>
    
    <div v-if="user" class="profile-content">
      <div class="profile-card card">
        <div class="form-group">
          <label for="username">Username</label>
          <input
            id="username"
            :value="user.username"
            disabled
          />
        </div>
        
        <div class="form-group">
          <label for="email">Email</label>
          <input
            id="email"
            :value="user.email"
            disabled
          />
        </div>
        
        <div class="form-group">
          <label for="displayName">Display Name</label>
          <input
            id="displayName"
            v-model="displayName"
            type="text"
            maxlength="50"
          />
        </div>
        
        <div class="form-group">
          <label for="bio">Bio</label>
          <textarea
            id="bio"
            v-model="bio"
            rows="4"
            maxlength="500"
          ></textarea>
        </div>
        
        <div v-if="error" class="error-message">{{ error }}</div>
        <div v-if="success" class="success-message">{{ success }}</div>
        
        <button @click="handleSave" :disabled="saving">
          {{ saving ? 'Saving...' : 'Save Changes' }}
        </button>
      </div>
      
      <div class="stats-card card">
        <h2>Statistics</h2>
        <div class="stat">
          <span class="label">Contributions</span>
          <span class="value">{{ user.contributionCount }}</span>
        </div>
        <div class="stat">
          <span class="label">Role</span>
          <span class="value">{{ user.role }}</span>
        </div>
        <div class="stat">
          <span class="label">Member since</span>
          <span class="value">{{ new Date(user.createdAt).toLocaleDateString() }}</span>
        </div>
      </div>
    </div>
    
    <div v-else class="not-authenticated">
      Please <RouterLink to="/login">login</RouterLink> to view your profile.
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
}

.profile-content {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.profile-card .form-group {
  margin-bottom: 16px;
}

.profile-card label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
}

.profile-card input:disabled {
  background: #f5f5f5;
  cursor: not-allowed;
}

.profile-card textarea {
  width: 100%;
  resize: vertical;
}

.error-message {
  color: #e74c3c;
  padding: 12px;
  background: #fdf2f2;
  border-radius: 4px;
  margin-bottom: 16px;
}

.success-message {
  color: #27ae60;
  padding: 12px;
  background: #f0fff4;
  border-radius: 4px;
  margin-bottom: 16px;
}

.stats-card h2 {
  font-size: 1.25rem;
  margin-bottom: 16px;
}

.stat {
  display: flex;
  justify-content: space-between;
  padding: 12px 0;
  border-bottom: 1px solid #eee;
}

.stat:last-child {
  border-bottom: none;
}

.stat .label {
  color: #666;
}

.stat .value {
  font-weight: 500;
}

.not-authenticated {
  text-align: center;
  padding: 40px;
  color: #666;
}
</style>
