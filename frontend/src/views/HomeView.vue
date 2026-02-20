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
        View All Articles 鈫?      </RouterLink>
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
  background: linear-gradient(135deg, rgba(0, 255, 157, 0.1) 0%, rgba(0, 0, 0, 0.8) 100%);
  border: 1px solid var(--color-primary);
  box-shadow: 0 0 20px rgba(0, 255, 157, 0.1);
  color: var(--color-text);
  border-radius: 8px;
  margin-bottom: 40px;
  position: relative;
  overflow: hidden;
}

.hero::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 2px;
  background: var(--color-primary);
  box-shadow: 0 0 10px var(--color-primary);
}

.hero h1 {
  font-size: 2.5rem;
  margin-bottom: 16px;
  color: var(--color-primary);
  text-shadow: 0 0 10px var(--color-primary);
  font-family: var(--font-family-heading);
}

.hero p {
  font-size: 1.2rem;
  opacity: 0.9;
  margin-bottom: 32px;
  color: var(--color-text-muted);
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
  border: 1px solid var(--color-primary);
  background: rgba(0, 0, 0, 0.5);
  color: var(--color-text);
  border-radius: 4px;
  font-size: 16px;
  font-family: var(--font-family-base);
}

.search-section input:focus {
  box-shadow: 0 0 10px var(--color-primary);
}

.search-section button {
  padding: 12px 24px;
  background: rgba(0, 255, 157, 0.1);
  border: 1px solid var(--color-primary);
  color: var(--color-primary);
  font-weight: 600;
  transition: all 0.3s;
}

.search-section button:hover {
  background: var(--color-primary);
  color: #000;
  box-shadow: 0 0 15px var(--color-primary);
}

.featured-articles h2 {
  margin-bottom: 24px;
  color: var(--color-secondary);
  text-shadow: 0 0 5px var(--color-secondary);
}

.loading,
.no-articles {
  text-align: center;
  padding: 40px;
  color: var(--color-text-muted);
  border: 1px dashed var(--color-text-muted);
  border-radius: 8px;
}

.articles-grid {
  display: grid;
  gap: 20px;
}

.view-all {
  display: inline-block;
  margin-top: 24px;
  font-weight: 500;
  color: var(--color-accent);
}

.view-all:hover {
  color: var(--color-primary);
  text-shadow: 0 0 5px var(--color-primary);
}
</style>
