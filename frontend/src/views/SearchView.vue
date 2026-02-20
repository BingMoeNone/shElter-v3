<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { searchApi } from '@/services/api'
import type { Article, Pagination } from '@/types'
import ArticleCard from '@/components/articles/ArticleCard.vue'
import { useToastStore } from '@/stores/toast'

const route = useRoute()
const router = useRouter()
const toast = useToastStore()

const articles = ref<Article[]>([])
const pagination = ref<Pagination | null>(null)
const loading = ref(false)
const searchQuery = ref('')
const error = ref<string | null>(null)
const hasSearched = ref(false)

onMounted(() => {
  const q = route.query.q as string
  if (q) {
    searchQuery.value = q
    performSearch()
  }
})

async function performSearch() {
  if (!searchQuery.value.trim()) return
  
  loading.value = true
  error.value = null
  hasSearched.value = true
  
  try {
    const response = await searchApi.search(searchQuery.value)
    articles.value = response.data.articles || []
    pagination.value = response.data.pagination
    
    router.push({ query: { q: searchQuery.value } })
  } catch (err: any) {
    console.error('Search failed:', err)
    error.value = err.response?.data?.message || '鎼滅储澶辫触'
    toast.error('鎼滅储澶辫触锛岃绋嶅悗閲嶈瘯')
  } finally {
    loading.value = false
  }
}

function clearSearch() {
  searchQuery.value = ''
  articles.value = []
  pagination.value = null
  error.value = null
  hasSearched.value = false
  router.push({ query: {} })
}
</script>

<template>
  <div class="search-page">
    <h1>鎼滅储鏂囩珷</h1>
    
    <div class="search-form">
      <input
        v-model="searchQuery"
        type="search"
        placeholder="杈撳叆鍏抽敭璇嶆悳绱?.."
        @keyup.enter="performSearch"
      />
      <button @click="performSearch" :disabled="loading || !searchQuery.trim()">
        {{ loading ? '鎼滅储涓?..' : '鎼滅储' }}
      </button>
      <button v-if="hasSearched" @click="clearSearch" class="btn-clear">
        娓呴櫎
      </button>
    </div>
    
    <div v-if="loading" class="loading">
      <div class="loading-spinner"></div>
      <p>姝ｅ湪鎼滅储...</p>
    </div>
    
    <div v-else-if="error" class="error-state">
      <span class="error-icon">鈿狅笍</span>
      <p>{{ error }}</p>
      <button @click="performSearch" class="retry-btn">閲嶈瘯</button>
    </div>
    
    <template v-else-if="hasSearched">
      <div v-if="articles.length > 0" class="results-info">
        鎵惧埌 {{ pagination?.totalItems || articles.length }} 鏉′笌 "{{ route.query.q }}" 鐩稿叧鐨勭粨鏋?      </div>
      
      <div v-else class="no-results">
        <span class="empty-icon">馃攳</span>
        <p>鏈壘鍒颁笌 "{{ route.query.q }}" 鐩稿叧鐨勬枃绔?/p>
        <p class="suggestion">灏濊瘯浣跨敤涓嶅悓鐨勫叧閿瘝</p>
      </div>
      
      <div v-if="articles.length > 0" class="results-list">
        <ArticleCard
          v-for="article in articles"
          :key="article.id"
          :article="article"
        />
      </div>
    </template>
    
    <div v-else class="search-placeholder">
      <span class="placeholder-icon">馃攳</span>
      <p>杈撳叆鍏抽敭璇嶅紑濮嬫悳绱?/p>
    </div>
  </div>
</template>

<style scoped>
.search-page {
  max-width: 800px;
  margin: 0 auto;
}

.search-page h1 {
  margin-bottom: 24px;
  color: var(--color-primary);
  text-shadow: 0 0 10px var(--color-primary);
}

.search-form {
  display: flex;
  gap: 12px;
  margin-bottom: 24px;
}

.search-form input {
  flex: 1;
  padding: 12px;
  background: rgba(0, 0, 0, 0.5);
  border: 1px solid var(--color-primary);
  color: var(--color-text);
  border-radius: 4px;
  transition: all 0.3s;
}

.search-form input:focus {
  box-shadow: 0 0 10px var(--color-primary);
  outline: none;
}

.search-form button {
  padding: 12px 24px;
  background: rgba(0, 255, 157, 0.1);
  border: 1px solid var(--color-primary);
  color: var(--color-primary);
  cursor: pointer;
  transition: all 0.3s;
}

.search-form button:hover:not(:disabled) {
  background: var(--color-primary);
  color: #000;
  box-shadow: 0 0 15px var(--color-primary);
}

.search-form button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-clear {
  background: rgba(255, 255, 255, 0.05) !important;
  border-color: var(--color-text-muted) !important;
  color: var(--color-text-muted) !important;
}

.btn-clear:hover:not(:disabled) {
  background: rgba(255, 255, 255, 0.1) !important;
}

.results-info {
  color: var(--color-text-muted);
  margin-bottom: 20px;
  padding: 12px;
  background: rgba(0, 255, 157, 0.05);
  border-radius: 4px;
  border-left: 3px solid var(--color-primary);
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

.no-results,
.search-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 60px;
  color: var(--color-text-muted);
  text-align: center;
  border: 1px dashed var(--color-border);
  border-radius: 8px;
}

.empty-icon,
.placeholder-icon {
  font-size: 3rem;
  margin-bottom: 16px;
}

.suggestion {
  font-size: 0.9rem;
  margin-top: 8px;
  color: var(--color-text-muted);
}

.results-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}
</style>
