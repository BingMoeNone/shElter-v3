<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useArticlesStore } from '@/stores/articles'
import ArticleCard from '@/components/articles/ArticleCard.vue'

const articlesStore = useArticlesStore()
const searchQuery = ref('')

onMounted(() => {
  articlesStore.fetchArticles({ limit: 10 })
})

function handleSearch() {
  if (searchQuery.value.trim()) {
    articlesStore.fetchArticles({ search: searchQuery.value, limit: 10 })
  } else {
    articlesStore.fetchArticles({ limit: 10 })
  }
}
</script>

<template>
  <div class="home">
    <section class="hero">
      <h1>Welcome to Wiki Platform</h1>
      <p>A collaborative platform for sharing knowledge and building communities.</p>
      
      <div class="search-section">
        <input
          v-model="searchQuery"
          type="search"
          placeholder="Search articles..."
          @keyup.enter="handleSearch"
        />
        <button @click="handleSearch">Search</button>
      </div>
    </section>
    
    <section class="featured-articles">
      <h2>Latest Articles</h2>
      
      <div v-if="articlesStore.loading" class="loading">
        Loading articles...
      </div>
      
      <div v-else-if="articlesStore.articles.length === 0" class="no-articles">
        No articles found. Be the first to <RouterLink to="/articles/create">create one</RouterLink>!
      </div>
      
      <div v-else class="articles-grid">
        <ArticleCard
          v-for="article in articlesStore.articles"
          :key="article.id"
          :article="article"
        />
      </div>
      
      <RouterLink to="/articles" class="view-all">
        View All Articles →
      </RouterLink>
    </section>
  </div>
</template>

<style scoped>
.home {
  max-width: 1000px;
  margin: 0 auto;
}

.hero {
  text-align: center;
  padding: 60px 20px;
  background: linear-gradient(135deg, #42b883 0%, #35495e 100%);
  color: white;
  border-radius: 8px;
  margin-bottom: 40px;
}

.hero h1 {
  font-size: 2.5rem;
  margin-bottom: 16px;
}

.hero p {
  font-size: 1.2rem;
  opacity: 0.9;
  margin-bottom: 32px;
}

.search-section {
  display: flex;
  gap: 12px;
  max-width: 500px;
  margin: 0 auto;
}

.search-section input {
  flex: 1;
  padding: 12px 16px;
  border: none;
  border-radius: 4px;
  font-size: 16px;
}

.search-section button {
  padding: 12px 24px;
  background: white;
  color: #42b883;
  font-weight: 600;
}

.featured-articles h2 {
  margin-bottom: 24px;
}

.loading,
.no-articles {
  text-align: center;
  padding: 40px;
  color: #666;
}

.articles-grid {
  display: grid;
  gap: 20px;
}

.view-all {
  display: inline-block;
  margin-top: 24px;
  font-weight: 500;
}
</style>
