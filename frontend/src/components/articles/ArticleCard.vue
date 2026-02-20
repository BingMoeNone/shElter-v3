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
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-left: 3px solid var(--color-primary);
  transition: all 0.3s ease;
}

.article-card:hover {
  transform: translateX(5px);
  box-shadow: 0 0 15px rgba(0, 255, 157, 0.2);
  border-color: var(--color-primary);
}

.article-link {
  text-decoration: none;
}

.article-title {
  font-size: 1.5rem;
  color: var(--color-primary);
  margin-bottom: 8px;
  transition: all 0.2s;
  font-family: var(--font-family-heading);
}

.article-link:hover .article-title {
  text-shadow: 0 0 8px var(--color-primary);
}

.article-meta {
  display: flex;
  gap: 16px;
  color: var(--color-text-muted);
  font-size: 0.9rem;
  margin-bottom: 12px;
  font-family: var(--font-family-base);
}

.article-excerpt {
  color: var(--color-text);
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
  color: var(--color-accent);
  font-size: 0.85rem;
  text-decoration: none;
  transition: all 0.2s;
}

.tag:hover {
  color: var(--color-primary);
  text-shadow: 0 0 5px var(--color-primary);
}

.article-categories {
  display: flex;
  gap: 8px;
}

.category {
  background: rgba(255, 255, 255, 0.05);
  padding: 4px 12px;
  border: 1px solid var(--color-border);
  border-radius: 4px;
  font-size: 0.85rem;
  color: var(--color-text-muted);
  text-decoration: none;
  transition: all 0.2s;
}

.category:hover {
  border-color: var(--color-secondary);
  color: var(--color-secondary);
  box-shadow: 0 0 5px var(--color-secondary);
}
</style>
