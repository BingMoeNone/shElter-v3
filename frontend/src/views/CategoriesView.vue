<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { categoriesApi } from '@/services/api'
import type { Category } from '@/types'
import { useToastStore } from '@/stores/toast'

const toast = useToastStore()
const categories = ref<Category[]>([])
const loading = ref(true)
const error = ref<string | null>(null)

onMounted(async () => {
  await fetchCategories()
})

async function fetchCategories() {
  loading.value = true
  error.value = null
  
  try {
    const response = await categoriesApi.list()
    categories.value = response.data.categories || response.data || []
  } catch (err: any) {
    console.error('Failed to fetch categories:', err)
    error.value = err.response?.data?.message || '鍔犺浇鍒嗙被澶辫触'
    toast.error('鏃犳硶鍔犺浇鍒嗙被鍒楄〃')
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="categories-page">
    <h1>鍒嗙被</h1>
    
    <div v-if="loading" class="loading">
      <div class="loading-spinner"></div>
      <p>鍔犺浇鍒嗙被涓?..</p>
    </div>
    
    <div v-else-if="error" class="error-state">
      <span class="error-icon">鈿狅笍</span>
      <p>{{ error }}</p>
      <button @click="fetchCategories" class="retry-btn">閲嶈瘯</button>
    </div>
    
    <div v-else-if="categories.length === 0" class="empty-state">
      <span class="empty-icon">馃搨</span>
      <p>鏆傛棤鍒嗙被</p>
    </div>
    
    <div v-else class="categories-grid">
      <RouterLink
        v-for="category in categories"
        :key="category.id"
        :to="`/categories/${category.slug}`"
        class="category-card card"
      >
        <h2>{{ category.name }}</h2>
        <p v-if="category.description">{{ category.description }}</p>
        <span class="article-count">{{ category.articleCount || 0 }} 绡囨枃绔?/span>
      </RouterLink>
    </div>
  </div>
</template>

<style scoped>
.categories-page {
  max-width: 1000px;
  margin: 0 auto;
}

.categories-page h1 {
  margin-bottom: 24px;
  color: var(--color-primary);
  text-shadow: 0 0 10px var(--color-primary);
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

.categories-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
}

.category-card {
  text-decoration: none;
  color: inherit;
  background: var(--color-surface);
  border: 1px solid var(--color-primary);
  border-radius: 8px;
  padding: 20px;
  transition: all 0.3s;
  box-shadow: 0 0 10px rgba(0, 255, 157, 0.1);
}

.category-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 255, 157, 0.2);
  border-color: var(--color-secondary);
}

.category-card h2 {
  font-size: 1.25rem;
  margin-bottom: 8px;
  color: var(--color-primary);
  text-shadow: 0 0 5px var(--color-primary);
}

.category-card p {
  color: var(--color-text-muted);
  margin-bottom: 12px;
  line-height: 1.5;
}

.article-count {
  font-size: 0.85rem;
  color: var(--color-accent);
  background: rgba(0, 255, 157, 0.1);
  padding: 4px 12px;
  border-radius: 12px;
}
</style>
