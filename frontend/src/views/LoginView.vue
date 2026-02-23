<script setup lang="ts">
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
const router = useRouter()
const route = useRoute()

const username = ref('')
const email = ref('')
const password = ref('')
const error = ref<string | null>(null)
const errorDetails = ref<any>(null)
const success = ref<string | null>(null)
const loading = ref(false)

async function handleLogin() {
  if (!username.value || !email.value || !password.value) return
  
  error.value = null
  errorDetails.value = null
  success.value = null
  loading.value = true
  
  try {
    await authStore.login(username.value, email.value, password.value)
    success.value = '登录成功，欢迎回来！'
    
    // Short delay to show success message
    setTimeout(() => {
      const redirect = route.query.redirect as string
      if (redirect && redirect !== '/login') {
        router.push(redirect)
      } else {
        router.push('/')
      }
    }, 1000)
  } catch (err: any) {
    password.value = ''
    const response = err.response?.data
    if (response?.detail) {
      if (typeof response.detail === 'string') {
        error.value = response.detail
      } else {
        error.value = response.detail.message || '登录失败'
        errorDetails.value = response.detail
      }
    } else if (response?.message) {
      error.value = response.message
    } else {
      error.value = '鐧诲綍澶辫触锛岃绋嶅悗閲嶈瘯'
    }
    loading.value = false
  }
}
</script>

<template>
  <div class="login-page">
    <div class="login-card card">
      <h1>鐧诲綍</h1>
      
      <form @submit.prevent="handleLogin">
        <div class="form-group">
          <label for="username">鐢ㄦ埛鍚?/label>
          <input
            id="username"
            v-model="username"
            type="text"
            required
            autofocus
            placeholder="璇疯緭鍏ョ敤鎴峰悕"
          />
        </div>
        
        <div class="form-group">
          <label for="email">閭</label>
          <input
            id="email"
            v-model="email"
            type="email"
            required
            placeholder="璇疯緭鍏ユ敞鍐屾椂浣跨敤鐨勯偖绠?
          />
        </div>
        
        <div class="form-group">
          <label for="password">瀵嗙爜</label>
          <input
            id="password"
            v-model="password"
            type="password"
            required
            placeholder="璇疯緭鍏ュ瘑鐮?
          />
        </div>
        
        <div v-if="success" class="success-message">
          <p>{{ success }}</p>
        </div>

        <div v-if="error" class="error-message">
          <p class="error-title">{{ error }}</p>
          <p v-if="errorDetails?.suggestion" class="error-suggestion">
            {{ errorDetails.suggestion }}
          </p>
        </div>
        
        <button type="submit" :disabled="loading" class="btn-login">
          {{ success ? '鐧诲綍鎴愬姛' : (loading ? '鐧诲綍涓?..' : '鐧诲綍') }}
        </button>
      </form>
      
      <p class="register-link">
        杩樻病鏈夎处鎴凤紵 <RouterLink to="/register">绔嬪嵆娉ㄥ唽</RouterLink>
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
  max-width: 420px;
  background: var(--color-surface);
  border: 1px solid var(--color-primary);
  box-shadow: 0 0 20px rgba(0, 255, 157, 0.1);
}

.login-card h1 {
  text-align: center;
  margin-bottom: 24px;
  color: var(--color-primary);
  text-shadow: 0 0 10px var(--color-primary);
}

.form-group {
  margin-bottom: 16px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  color: var(--color-text);
}

.form-group input {
  background: rgba(0, 0, 0, 0.5);
  border: 1px solid var(--color-border);
  color: var(--color-text);
  transition: all 0.3s;
}

.form-group input:focus {
  border-color: var(--color-primary);
  box-shadow: 0 0 10px rgba(0, 255, 157, 0.2);
}

.error-message {
  color: #ff4444;
  margin-bottom: 16px;
  padding: 12px;
  background: rgba(255, 68, 68, 0.1);
  border-radius: 4px;
  border-left: 3px solid #ff4444;
}

.error-title {
  margin: 0 0 8px 0;
  font-weight: 500;
}

.error-suggestion {
  margin: 0;
  font-size: 0.9rem;
  color: var(--color-text-muted);
}

.success-message {
  color: var(--color-primary);
  margin-bottom: 16px;
  padding: 12px;
  background: rgba(0, 255, 157, 0.1);
  border-radius: 4px;
  border-left: 3px solid var(--color-primary);
  text-align: center;
  font-weight: bold;
}

.btn-login {
  width: 100%;
  padding: 12px;
  font-size: 16px;
  margin-top: 10px;
  background: rgba(0, 255, 157, 0.1);
  border: 1px solid var(--color-primary);
  color: var(--color-primary);
  transition: all 0.3s;
}

.btn-login:hover {
  background: var(--color-primary);
  color: #000;
  box-shadow: 0 0 20px var(--color-primary);
}

.btn-login:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  box-shadow: none;
}

.register-link {
  text-align: center;
  margin-top: 20px;
  color: var(--color-text-muted);
}

.register-link a {
  color: var(--color-primary);
  font-weight: bold;
}

.register-link a:hover {
  text-shadow: 0 0 5px var(--color-primary);
}
</style>
