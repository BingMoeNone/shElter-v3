<script setup lang="ts">
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
const router = useRouter()
const route = useRoute()

const username = ref('')
const password = ref('')
const error = ref<string | null>(null)
const loading = ref(false)

async function handleLogin() {
  if (!username.value || !password.value) return
  
  error.value = null
  loading.value = true
  
  try {
    await authStore.login(username.value, password.value)
    const redirect = route.query.redirect as string
    router.push(redirect || '/')
  } catch (err) {
    error.value = 'Invalid username or password'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="login-page">
    <div class="login-card card">
      <h1>Login</h1>
      
      <form @submit.prevent="handleLogin">
        <div class="form-group">
          <label for="username">Username</label>
          <input
            id="username"
            v-model="username"
            type="text"
            required
            autofocus
          />
        </div>
        
        <div class="form-group">
          <label for="password">Password</label>
          <input
            id="password"
            v-model="password"
            type="password"
            required
          />
        </div>
        
        <div v-if="error" class="error-message">{{ error }}</div>
        
        <button type="submit" :disabled="loading" class="btn-login">
          {{ loading ? 'Logging in...' : 'Login' }}
        </button>
      </form>
      
      <p class="register-link">
        Don't have an account? <RouterLink to="/register">Register</RouterLink>
      </p>
    </div>
  </div>
</template>

<style scoped>
.login-page {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 60vh;
}

.login-card {
  width: 100%;
  max-width: 400px;
}

.login-card h1 {
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

.btn-login {
  width: 100%;
  padding: 12px;
  font-size: 16px;
}

.register-link {
  text-align: center;
  margin-top: 20px;
  color: #666;
}
</style>
