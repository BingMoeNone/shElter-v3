<script setup lang="ts">
import { onMounted, ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import { articlesApi, tagsApi } from '@/services/api'
import type { Article, Tag } from '@/types'
import ArticleCard from '@/components/articles/ArticleCard.vue'
import { useToastStore } from '@/stores/toast'

const route = useRoute()
const toast = useToastStore()

const tag = ref<Tag | null>(null)
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
    
    const tagsResponse = await tagsApi.list()
    tag.value = tagsResponse.data.tags?.find(
      (t: Tag) => t.slug === slug
    ) || tagsResponse.data?.find(
      (t: Tag) => t.slug === slug
    ) || null
    
    const articlesResponse = await articlesApi.list({ tag: slug })
    articles.value = articlesResponse.data.articles || []
  } catch (err: any) {
    console.error('Failed to fetch data:', err)
    error.value = err.response?.data?.message || '加载失败'
    toast.error('无法加载标签文章')
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="tag-articles-page">
    <div v-if="loading" class="loading">
      <div class="loading-spinner"></div>
      <p>加载中...</p>
    </div>
    
    <div v-else-if="error" class="error-state">
      <span class="error-icon">⚠️</span>
      <p>{{ error }}</p>
      <button @click="fetchData" class="retry-btn">重试</button>
    </div>
    
    <template v-else>
      <header class="page-header">
        <h1>#{{ tag?.name || '标签' }}</h1>
        <p>{{ tag?.usageCount || articles.length }} 篇相关文章</p>
      </header>
      
      <div v-if="articles.length === 0" class="empty-state">
        <span class="empty-icon">🏷️</span>
        <p>该标签下暂无文章</p>
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
.tag-articles-page {
  max-width: 800px;
  margin: 0 auto;
}

.page-header {
  margin-bottom: 32px;
}

.page-header h1 {
  color: var(--color-primary);
  text-shadow: 0 0 10px var(--color-primary);
  margin-bottom: 8px;
}

.page-header p {
  color: var(--color-text-muted);
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

.articles-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}
</style>
