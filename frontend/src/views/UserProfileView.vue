<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import { usersApi } from '@/services/api'
import type { Article, UserProfile } from '@/types'
import UserCard from '@/components/users/UserCard.vue'
import ArticleCard from '@/components/articles/ArticleCard.vue'
import { useToastStore } from '@/stores/toast'

const route = useRoute()
const toast = useToastStore()

const user = ref<UserProfile | null>(null)
const articles = ref<Article[]>([])
const loading = ref(true)
const error = ref<string | null>(null)

onMounted(async () => {
  await fetchUser()
})

async function fetchUser() {
  loading.value = true
  error.value = null
  
  try {
    const userId = route.params.id as string
    const response = await usersApi.getProfile(userId)
    user.value = response.data
    
    // Note: In a real app, there should be an API to fetch articles by user ID
    // This is a workaround that may not be efficient
    if (user.value) {
      articles.value = []  // Will be populated when proper API is available
    }
  } catch (err: any) {
    error.value = err.response?.data?.message || '鍔犺浇鐢ㄦ埛璧勬枡澶辫触'
    toast.error('鏃犳硶鍔犺浇鐢ㄦ埛璧勬枡')
    console.error(err)
  } finally {
    loading.value = false
  }
}

function handleConnectionChanged() {
  fetchUser()
}
</script>

<template>
  <div class="user-profile-page">
    <div v-if="loading" class="loading">
      <div class="loading-spinner"></div>
      <p>鍔犺浇鐢ㄦ埛璧勬枡涓?..</p>
    </div>
    
    <div v-else-if="error" class="error-state">
      <span class="error-icon">鈿狅笍</span>
      <p>{{ error }}</p>
      <button @click="fetchUser" class="retry-btn">閲嶈瘯</button>
    </div>
    
    <template v-else-if="user">
      <UserCard
        :user="user"
        :is-following="user.isFollowing"
        @connection-changed="handleConnectionChanged"
      />
      
      <section class="user-articles">
        <h2>{{ user.displayName || user.username }} 鐨勬枃绔?/h2>
        
        <div v-if="articles.length === 0" class="empty-state">
          <span class="empty-icon">馃摑</span>
          <p>鏆傛棤鏂囩珷</p>
        </div>
        
        <div v-else class="articles-list">
          <ArticleCard
            v-for="article in articles"
            :key="article.id"
            :article="article"
          />
        </div>
      </section>
    </template>
  </div>
</template>

<style scoped>
.user-profile-page {
  max-width: 800px;
  margin: 0 auto;
}

.loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 60px;
  color: var(--color-text-muted);
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 3px solid var(--color-border);
  border-top-color: var(--color-primary);
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 16px;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.error-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 60px;
  color: #ff4444;
  text-align: center;
}

.error-icon {
  font-size: 3rem;
  margin-bottom: 16px;
}

.retry-btn {
  margin-top: 16px;
  padding: 8px 24px;
  background: rgba(255, 68, 68, 0.1);
  border: 1px solid #ff4444;
  color: #ff4444;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.2s;
}

.retry-btn:hover {
  background: #ff4444;
  color: white;
}

.user-articles {
  margin-top: 32px;
}

.user-articles h2 {
  margin-bottom: 24px;
  color: var(--color-secondary);
  text-shadow: 0 0 5px var(--color-secondary);
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 40px;
  color: var(--color-text-muted);
  text-align: center;
  border: 1px dashed var(--color-border);
  border-radius: 8px;
}

.empty-icon {
  font-size: 2rem;
  margin-bottom: 12px;
}

.articles-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}
</style>
