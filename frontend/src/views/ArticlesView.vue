<script setup lang="ts">
import { onMounted, ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useArticlesStore } from '@/stores/articles'
import ArticleCard from '@/components/articles/ArticleCard.vue'

const articlesStore = useArticlesStore()
const route = useRoute()

const currentPage = ref(1)
const searchQuery = ref('')

onMounted(() => {
  fetchArticles()
})

watch(() => route.query, () => {
  fetchArticles()
}, { deep: true })

function fetchArticles() {
  const params: Record<string, unknown> = {
    page: currentPage.value,
    limit: 10,
  }
  
  if (route.query.category) {
    params.category = route.query.category as string
  }
  if (route.query.tag) {
    params.tag = route.query.tag as string
  }
  if (searchQuery.value) {
    params.search = searchQuery.value
  }
  
  articlesStore.fetchArticles(params)
}

function handleSearch() {
  currentPage.value = 1
  fetchArticles()
}

function changePage(page: number) {
  currentPage.value = page
  fetchArticles()
  window.scrollTo(0, 0)
}
</script>

<template>
  <div class="articles-page">
    <div class="page-header">
      <h1>Articles</h1>
      
      <div class="search-section">
        <input
          v-model="searchQuery"
          type="search"
          placeholder="Search articles..."
          @keyup.enter="handleSearch"
        />
        <button @click="handleSearch">Search</button>
      </div>
    </div>
    
    <div v-if="articlesStore.loading" class="loading">
      Loading articles...
    </div>
    
    <div v-else-if="articlesStore.articles.length === 0" class="no-articles">
      No articles found.
    </div>
    
    <template v-else>
      <div class="articles-list">
        <ArticleCard
          v-for="article in articlesStore.articles"
          :key="article.id"
          :article="article"
        />
      </div>
      
      <div v-if="articlesStore.pagination" class="pagination">
        <button
          :disabled="currentPage === 1"
          @click="changePage(currentPage - 1)"
        >
          Previous
        </button>
        <span>Page {{ currentPage }} of {{ articlesStore.pagination.totalPages }}</span>
        <button
          :disabled="currentPage === articlesStore.pagination.totalPages"
          @click="changePage(currentPage + 1)"
        >
          Next
        </button>
      </div>
    </template>
  </div>
</template>

<style scoped>
.articles-page {
  max-width: 800px;
  margin: 0 auto;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  flex-wrap: wrap;
  gap: 16px;
}

.page-header h1 {
  margin: 0;
  color: var(--color-primary);
  text-shadow: 0 0 10px var(--color-primary);
}

.search-section {
  display: flex;
  gap: 8px;
}

.search-section input {
  width: 250px;
  padding: 8px 12px;
  background: rgba(0, 0, 0, 0.5);
  border: 1px solid var(--color-primary);
  color: var(--color-text);
  border-radius: 4px;
}

.search-section input:focus {
  box-shadow: 0 0 10px var(--color-primary);
}

.search-section button {
  padding: 8px 16px;
  background: rgba(0, 255, 157, 0.1);
  border: 1px solid var(--color-primary);
  color: var(--color-primary);
  cursor: pointer;
  transition: all 0.3s;
}

.search-section button:hover {
  background: var(--color-primary);
  color: #000;
  box-shadow: 0 0 15px var(--color-primary);
}

.loading,
.no-articles {
  text-align: center;
  padding: 40px;
  color: var(--color-text-muted);
  border: 1px dashed var(--color-text-muted);
  border-radius: 8px;
}

.articles-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 16px;
  margin-top: 32px;
}

.pagination span {
  color: var(--color-text-muted);
}

.pagination button {
  padding: 8px 16px;
  background: rgba(0, 255, 157, 0.1);
  border: 1px solid var(--color-primary);
  color: var(--color-primary);
  cursor: pointer;
  transition: all 0.3s;
}

.pagination button:hover:not(:disabled) {
  background: var(--color-primary);
  color: #000;
  box-shadow: 0 0 15px var(--color-primary);
}

.pagination button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  border-color: var(--color-text-muted);
  color: var(--color-text-muted);
}
</style>
