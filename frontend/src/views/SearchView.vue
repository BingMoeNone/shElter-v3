<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { searchApi } from '@/services/api'
import type { Article, Pagination } from '@/types'
import ArticleCard from '@/components/articles/ArticleCard.vue'

const route = useRoute()
const router = useRouter()

const articles = ref<Article[]>([])
const pagination = ref<Pagination | null>(null)
const loading = ref(false)
const searchQuery = ref('')

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
  
  try {
    const response = await searchApi.search(searchQuery.value)
    articles.value = response.data.articles
    pagination.value = response.data.pagination
    
    router.push({ query: { q: searchQuery.value } })
  } catch (error) {
    console.error('Search failed:', error)
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="search-page">
    <h1>Search Articles</h1>
    
    <div class="search-form">
      <input
        v-model="searchQuery"
        type="search"
        placeholder="Enter search terms..."
        @keyup.enter="performSearch"
      />
      <button @click="performSearch" :disabled="loading">
        {{ loading ? 'Searching...' : 'Search' }}
      </button>
    </div>
    
    <div v-if="articles.length > 0" class="results-info">
      Found {{ pagination?.totalItems || 0 }} results for "{{ route.query.q }}"
    </div>
    
    <div v-if="loading" class="loading">
      Searching...
    </div>
    
    <div v-else-if="articles.length === 0 && route.query.q" class="no-results">
      No articles found for "{{ route.query.q }}".
    </div>
    
    <div v-else class="results-list">
      <ArticleCard
        v-for="article in articles"
        :key="article.id"
        :article="article"
      />
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
}

.search-form {
  display: flex;
  gap: 12px;
  margin-bottom: 24px;
}

.search-form input {
  flex: 1;
  padding: 12px;
}

.results-info {
  color: #666;
  margin-bottom: 20px;
}

.loading,
.no-results {
  text-align: center;
  padding: 40px;
  color: #666;
}

.results-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}
</style>
