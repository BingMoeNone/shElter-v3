<script setup lang="ts">
import { onMounted, ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import { articlesApi, tagsApi } from '@/services/api'
import type { Article, Tag } from '@/types'
import ArticleCard from '@/components/articles/ArticleCard.vue'

const route = useRoute()

const tag = ref<Tag | null>(null)
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
    
    const tagsResponse = await tagsApi.list()
    tag.value = tagsResponse.data.tags.find(
      (t: Tag) => t.slug === slug
    ) || null
    
    const articlesResponse = await articlesApi.list({ tag: slug })
    articles.value = articlesResponse.data.articles
  } catch (error) {
    console.error('Failed to fetch data:', error)
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="tag-articles-page">
    <div v-if="loading" class="loading">
      Loading...
    </div>
    
    <template v-else>
      <header class="page-header">
        <h1>#{{ tag?.name || 'Tag' }}</h1>
        <p>{{ tag?.usageCount || 0 }} articles with this tag</p>
      </header>
      
      <div v-if="articles.length === 0" class="no-articles">
        No articles with this tag.
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
  color: #42b883;
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
