<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
const router = useRouter()

const username = ref('')
const email = ref('')
const password = ref('')
const confirmPassword = ref('')
const displayName = ref('')
const error = ref<string | null>(null)
const loading = ref(false)

async function handleRegister() {
  if (!username.value || !email.value || !password.value) return
  
  if (password.value !== confirmPassword.value) {
    error.value = 'Passwords do not match'
    return
  }
  
  if (password.value.length < 8) {
    error.value = 'Password must be at least 8 characters'
    return
  }
  
  error.value = null
  loading.value = true
  
  try {
    await authStore.register({
      username: username.value,
      email: email.value,
      password: password.value,
      displayName: displayName.value || undefined,
    })
    router.push('/')
  } catch (err) {
    error.value = 'Registration failed. Username or email may already be taken.'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="register-page">
    <div class="register-card card">
      <h1>Register</h1>
      
      <form @submit.prevent="handleRegister">
        <div class="form-group">
          <label for="username">Username *</label>
          <input
            id="username"
            v-model="username"
            type="text"
            required
            pattern="[a-zA-Z0-9_]+"
            title="Username can only contain letters, numbers, and underscores"
          />
        </div>
        
        <div class="form-group">
          <label for="email">Email *</label>
          <input
            id="email"
            v-model="email"
            type="email"
            required
          />
        </div>
        
        <div class="form-group">
          <label for="displayName">Display Name</label>
          <input
            id="displayName"
            v-model="displayName"
            type="text"
          />
        </div>
        
        <div class="form-group">
          <label for="password">Password *</label>
          <input
            id="password"
            v-model="password"
            type="password"
            required
            minlength="8"
          />
        </div>
        
        <div class="form-group">
          <label for="confirmPassword">Confirm Password *</label>
          <input
            id="confirmPassword"
            v-model="confirmPassword"
            type="password"
            required
          />
        </div>
        
        <div v-if="error" class="error-message">{{ error }}</div>
        
        <button type="submit" :disabled="loading" class="btn-register">
          {{ loading ? 'Creating Account...' : 'Register' }}
        </button>
      </form>
      
      <p class="login-link">
        Already have an account? <RouterLink to="/login">Login</RouterLink>
      </p>
    </div>
  </div>
</template>

<style scoped>
.register-page {
  display: flex;
  justify-content: center;
  padding: 40px 20px;
}

.register-card {
  width: 100%;
  max-width: 450px;
}

.register-card h1 {
  text-align: center;
  margin-bottom: 24px;
}

.form-group {
  margin-bottom: 16px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
}

.error-message {
  color: #e74c3c;
  margin-bottom: 16px;
  padding: 12px;
  background: #fdf2f2;
  border-radius: 4px;
  text-align: center;
}

.btn-register {
  width: 100%;
  padding: 12px;
  font-size: 16px;
}

.login-link {
  text-align: center;
  margin-top: 20px;
  color: #666;
}
</style>
