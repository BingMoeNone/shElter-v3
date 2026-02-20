<script setup lang="ts">
import { onMounted, ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import { articlesApi } from '@/services/api'
import type { Article, Category } from '@/types'
import { categoriesApi } from '@/services/api'
import ArticleCard from '@/components/articles/ArticleCard.vue'
import { useToastStore } from '@/stores/toast'

const route = useRoute()
const toast = useToastStore()

const category = ref<Category | null>(null)
const articles = ref<Article[]>([])
const loading = ref(true)
const error = ref<string | null>(null)

onMounted(async () => {
  await fetchData()
})

watch(() => route.params.slug, () => {
  fetchData()
})

async function fetchData() {
  loading.value = true
  error.value = null
  
  try {
    const slug = route.params.slug as string
    
    const categoriesResponse = await categoriesApi.list()
    category.value = categoriesResponse.data.categories?.find(
      (c: Category) => c.slug === slug
    ) || categoriesResponse.data?.find(
      (c: Category) => c.slug === slug
    ) || null
    
    const articlesResponse = await articlesApi.list({ category: slug })
    articles.value = articlesResponse.data.articles || []
  } catch (err: any) {
    console.error('Failed to fetch data:', err)
    error.value = err.response?.data?.message || '鍔犺浇澶辫触'
    toast.error('鏃犳硶鍔犺浇鍒嗙被鏂囩珷')
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="category-articles-page">
    <div v-if="loading" class="loading">
      <div class="loading-spinner"></div>
      <p>鍔犺浇涓?..</p>
    </div>
    
    <div v-else-if="error" class="error-state">
      <span class="error-icon">鈿狅笍</span>
      <p>{{ error }}</p>
      <button @click="fetchData" class="retry-btn">閲嶈瘯</button>
    </div>
    
    <template v-else>
      <header class="page-header">
        <h1>{{ category?.name || '鍒嗙被' }}</h1>
        <p v-if="category?.description">{{ category.description }}</p>
        <p v-else class="no-description">鏆傛棤鎻忚堪</p>
      </header>
      
      <div v-if="articles.length === 0" class="empty-state">
        <span class="empty-icon">馃摑</span>
        <p>璇ュ垎绫讳笅鏆傛棤鏂囩珷</p>
        <RouterLink to="/articles/create" class="create-link">鍒涘缓绗竴绡囨枃绔?/RouterLink>
      </div>
      
      <div v-else class="articles-list">
        <ArticleCard
          v-for="article in articles"
          :key="article.id"
          :article="article"
        />
      </div>
    </template>
  </div>
</template>

<style scoped>
.category-articles-page {
  max-width: 800px;
  margin: 0 auto;
}

.page-header {
  margin-bottom: 32px;
}

.page-header h1 {
  margin-bottom: 8px;
  color: var(--color-primary);
  text-shadow: 0 0 10px var(--color-primary);
}

.page-header p {
  color: var(--color-text-muted);
}

.no-description {
  font-style: italic;
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

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 60px;
  color: var(--color-text-muted);
  text-align: center;
  border: 1px dashed var(--color-border);
  border-radius: 8px;
}

.empty-icon {
  font-size: 3rem;
  margin-bottom: 16px;
}

.create-link {
  margin-top: 16px;
  color: var(--color-primary);
  padding: 8px 24px;
  border: 1px solid var(--color-primary);
  border-radius: 4px;
  text-decoration: none;
  transition: all 0.3s;
}

.create-link:hover {
  background: var(--color-primary);
  color: #000;
}

.articles-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}
</style>
