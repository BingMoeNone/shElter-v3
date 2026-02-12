<script setup lang="ts">
import { onMounted, ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import { articlesApi } from '@/services/api'
import type { Article, Category } from '@/types'
import { categoriesApi } from '@/services/api'
import ArticleCard from '@/components/articles/ArticleCard.vue'

const route = useRoute()

const category = ref<Category | null>(null)
const articles = ref<Article[]>([])
const loading = ref(true)

onMounted(async () => {
  await fetchData()
})

watch(() => route.params.slug, () => {
  fetchData()
})

async function fetchData() {
  loading.value = true
  
  try {
    const slug = route.params.slug as string
    
    const categoriesResponse = await categoriesApi.list()
    category.value = categoriesResponse.data.categories.find(
      (c: Category) => c.slug === slug
    ) || null
    
    const articlesResponse = await articlesApi.list({ category: slug })
    articles.value = articlesResponse.data.articles
  } catch (error) {
    console.error('Failed to fetch data:', error)
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="category-articles-page">
    <div v-if="loading" class="loading">
      Loading...
    </div>
    
    <template v-else>
      <header class="page-header">
        <h1>{{ category?.name || 'Category' }}</h1>
        <p v-if="category?.description">{{ category.description }}</p>
      </header>
      
      <div v-if="articles.length === 0" class="no-articles">
        No articles in this category.
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
}

.page-header p {
  color: #666;
}

.loading,
.no-articles {
  text-align: center;
  padding: 40px;
  color: #666;
}

.articles-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}
</style>
