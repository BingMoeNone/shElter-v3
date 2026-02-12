<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { categoriesApi } from '@/services/api'
import type { Category } from '@/types'

const categories = ref<Category[]>([])
const loading = ref(true)

onMounted(async () => {
  await fetchCategories()
})

async function fetchCategories() {
  loading.value = true
  
  try {
    const response = await categoriesApi.list()
    categories.value = response.data.categories
  } catch (error) {
    console.error('Failed to fetch categories:', error)
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="categories-page">
    <h1>Categories</h1>
    
    <div v-if="loading" class="loading">
      Loading categories...
    </div>
    
    <div v-else-if="categories.length === 0" class="no-categories">
      No categories found.
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
        <span class="article-count">{{ category.articleCount }} articles</span>
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
}

.loading,
.no-categories {
  text-align: center;
  padding: 40px;
  color: #666;
}

.categories-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
}

.category-card {
  text-decoration: none;
  color: inherit;
  transition: transform 0.2s, box-shadow 0.2s;
}

.category-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.category-card h2 {
  font-size: 1.25rem;
  margin-bottom: 8px;
  color: #42b883;
}

.category-card p {
  color: #666;
  margin-bottom: 12px;
  line-height: 1.5;
}

.article-count {
  font-size: 0.85rem;
  color: #888;
}
</style>
