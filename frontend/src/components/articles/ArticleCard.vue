<script setup lang="ts">
import type { Article } from '@/types'
import { computed } from 'vue'

const props = defineProps<{
  article: Article
}>()

const formattedDate = computed(() => {
  return new Date(props.article.createdAt).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
})

const excerpt = computed(() => {
  const text = props.article.content.replace(/<[^>]*>/g, '')
  return text.length > 150 ? text.slice(0, 150) + '...' : text
})
</script>

<template>
  <article class="article-card card">
    <RouterLink :to="`/articles/${article.id}`" class="article-link">
      <h2 class="article-title">{{ article.title }}</h2>
    </RouterLink>
    
    <div class="article-meta">
      <span class="author">By {{ article.author.displayName || article.author.username }}</span>
      <span class="date">{{ formattedDate }}</span>
      <span class="views">{{ article.viewCount }} views</span>
    </div>
    
    <p class="article-excerpt">{{ article.summary || excerpt }}</p>
    
    <div class="article-tags" v-if="article.tags.length > 0">
      <RouterLink
        v-for="tag in article.tags"
        :key="tag.id"
        :to="`/tags/${tag.slug}`"
        class="tag"
      >
        #{{ tag.name }}
      </RouterLink>
    </div>
    
    <div class="article-categories" v-if="article.categories.length > 0">
      <RouterLink
        v-for="category in article.categories"
        :key="category.id"
        :to="`/categories/${category.slug}`"
        class="category"
      >
        {{ category.name }}
      </RouterLink>
    </div>
  </article>
</template>

<style scoped>
.article-card {
  margin-bottom: 20px;
}

.article-link {
  text-decoration: none;
}

.article-title {
  font-size: 1.5rem;
  color: #333;
  margin-bottom: 8px;
  transition: color 0.2s;
}

.article-link:hover .article-title {
  color: #42b883;
}

.article-meta {
  display: flex;
  gap: 16px;
  color: #666;
  font-size: 0.9rem;
  margin-bottom: 12px;
}

.article-excerpt {
  color: #444;
  line-height: 1.6;
  margin-bottom: 12px;
}

.article-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 12px;
}

.tag {
  color: #42b883;
  font-size: 0.85rem;
  text-decoration: none;
}

.tag:hover {
  text-decoration: underline;
}

.article-categories {
  display: flex;
  gap: 8px;
}

.category {
  background: #f0f0f0;
  padding: 4px 12px;
  border-radius: 4px;
  font-size: 0.85rem;
  color: #666;
  text-decoration: none;
}

.category:hover {
  background: #e0e0e0;
}
</style>
