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
const errorDetails = ref<any>(null)
const success = ref<string | null>(null)
const loading = ref(false)

async function handleRegister() {
  if (!username.value || !email.value || !password.value) return
  
  if (password.value !== confirmPassword.value) {
    error.value = '两次输入的密码不一致'
    errorDetails.value = null
    return
  }
  
  if (password.value.length < 8) {
    error.value = '密码长度至少为 8 个字符'
    errorDetails.value = null
    return
  }
  
  error.value = null
  errorDetails.value = null
  success.value = null
  loading.value = true
  
  try {
    await authStore.register({
      username: username.value,
      email: email.value,
      password: password.value,
      displayName: displayName.value || undefined,
    })
    success.value = '注册成功，正在为您自动登录...'
    
    setTimeout(() => {
      router.push('/')
    }, 1500)
  } catch (err: any) {
    const response = err.response?.data
    if (response?.detail) {
      if (typeof response.detail === 'string') {
        error.value = response.detail
      } else {
        error.value = response.detail.message || '娉ㄥ唽澶辫触'
        errorDetails.value = response.detail
      }
    } else if (response?.message) {
      error.value = response.message
    } else {
      error.value = '娉ㄥ唽澶辫触锛岃绋嶅悗閲嶈瘯'
    }
    loading.value = false
  }
}
</script>

<template>
  <div class="register-page">
    <div class="register-card card">
      <h1>娉ㄥ唽</h1>
      
      <form @submit.prevent="handleRegister">
        <div class="form-group">
          <label for="username">鐢ㄦ埛鍚?*</label>
          <input
            id="username"
            v-model="username"
            type="text"
            required
            pattern="[a-zA-Z0-9_]+"
            title="鐢ㄦ埛鍚嶅彧鑳藉寘鍚瓧姣嶃€佹暟瀛楀拰涓嬪垝绾?
            placeholder="璇疯緭鍏ョ敤鎴峰悕"
          />
          <p class="hint">鐢ㄦ埛鍚嶅彲浠ヤ笌鍏朵粬鐢ㄦ埛鐩稿悓锛屼絾闇€涓庨偖绠遍厤濂椾娇鐢?/p>
        </div>
        
        <div class="form-group">
          <label for="email">閭 *</label>
          <input
            id="email"
            v-model="email"
            type="email"
            required
            placeholder="璇疯緭鍏ラ偖绠卞湴鍧€"
          />
          <p class="hint">閭鏄偍鐨勫敮涓€韬唤鏍囪瘑锛屼笉鍙噸澶?/p>
        </div>
        
        <div class="form-group">
          <label for="displayName">鏄剧ず鍚嶇О</label>
          <input
            id="displayName"
            v-model="displayName"
            type="text"
            placeholder="鍙€夛紝鐢ㄤ簬鏄剧ず鎮ㄧ殑鏄电О"
          />
        </div>
        
        <div class="form-group">
          <label for="password">瀵嗙爜 *</label>
          <input
            id="password"
            v-model="password"
            type="password"
            required
            minlength="8"
            placeholder="鑷冲皯 8 涓瓧绗?
          />
        </div>
        
        <div class="form-group">
          <label for="confirmPassword">纭瀵嗙爜 *</label>
          <input
            id="confirmPassword"
            v-model="confirmPassword"
            type="password"
            required
            placeholder="璇峰啀娆¤緭鍏ュ瘑鐮?
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
        
        <button type="submit" :disabled="loading" class="btn-register">
          {{ success ? '娉ㄥ唽鎴愬姛' : (loading ? '娉ㄥ唽涓?..' : '娉ㄥ唽') }}
        </button>
      </form>
      
      <p class="login-link">
        宸叉湁璐︽埛锛?<RouterLink to="/login">绔嬪嵆鐧诲綍</RouterLink>
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
  background: var(--color-surface);
  border: 1px solid var(--color-primary);
  box-shadow: 0 0 20px rgba(0, 255, 157, 0.1);
}

.register-card h1 {
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

.hint {
  font-size: 0.85rem;
  color: var(--color-text-muted);
  margin-top: 4px;
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

.btn-register {
  width: 100%;
  padding: 12px;
  font-size: 16px;
  margin-top: 10px;
  background: rgba(0, 255, 157, 0.1);
  border: 1px solid var(--color-primary);
  color: var(--color-primary);
  transition: all 0.3s;
}

.btn-register:hover {
  background: var(--color-primary);
  color: #000;
  box-shadow: 0 0 20px var(--color-primary);
}

.btn-register:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  box-shadow: none;
}

.login-link {
  text-align: center;
  margin-top: 20px;
  color: var(--color-text-muted);
}

.login-link a {
  color: var(--color-primary);
  font-weight: bold;
}

.login-link a:hover {
  text-shadow: 0 0 5px var(--color-primary);
}
</style>
