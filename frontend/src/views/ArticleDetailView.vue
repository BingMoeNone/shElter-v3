<script setup lang="ts">
import { onMounted, ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useArticlesStore } from '@/stores/articles'
import { useAuthStore } from '@/stores/auth'
import { commentsApi } from '@/services/api'
import type { Comment } from '@/types'
import CommentSection from '@/components/comments/CommentSection.vue'

const articlesStore = useArticlesStore()
const authStore = useAuthStore()
const route = useRoute()
const router = useRouter()

const articleId = computed(() => route.params.id as string)
const comments = ref<Comment[]>([])

onMounted(async () => {
  await articlesStore.fetchArticle(articleId.value)
  await fetchComments()
})

const article = computed(() => articlesStore.currentArticle)

async function fetchComments() {
  try {
    const response = await commentsApi.getByArticle?.(articleId.value)
    if (response) {
      comments.value = response.data
    }
  } catch (error) {
    console.error('Failed to fetch comments:', error)
  }
}

function handleCommentAdded(comment: Comment) {
  comments.value.unshift(comment)
}

function handleCommentDeleted(commentId: string) {
  comments.value = comments.value.filter(c => c.id !== commentId)
}

function formatDate(date: string) {
  return new Date(date).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

function canEdit() {
  return article.value && (
    article.value.author.id === authStore.user?.id ||
    authStore.isAdmin
  )
}

async function handleDelete() {
  if (!confirm('Are you sure you want to delete this article?')) return
  
  try {
    await articlesStore.deleteArticle(articleId.value)
    router.push('/articles')
  } catch (error) {
    console.error('Failed to delete article:', error)
  }
}
</script>

<template>
  <div class="article-detail-page">
    <template v-if="article">
      <article class="article">
        <header class="article-header">
          <h1>{{ article.title }}</h1>
          
          <div class="article-meta">
            <RouterLink :to="`/users/${article.author.id}`" class="author">
              By {{ article.author.displayName || article.author.username }}
            </RouterLink>
            <span class="date">{{ formatDate(article.createdAt) }}</span>
            <span class="views">{{ article.viewCount }} views</span>
          </div>
          
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
          
          <div v-if="canEdit()" class="article-actions">
            <RouterLink :to="`/articles/${article.id}/edit`" class="btn-edit">
              Edit
            </RouterLink>
            <button @click="handleDelete" class="btn-delete">Delete</button>
          </div>
        </header>
        
        <div class="article-content">
          <p v-if="article.summary" class="summary">{{ article.summary }}</p>
          <div class="content" v-html="article.content"></div>
        </div>
      </article>
      
      <CommentSection
        :comments="comments"
        :article-id="articleId"
        @comment-added="handleCommentAdded"
        @comment-deleted="handleCommentDeleted"
      />
    </template>
    
    <div v-else-if="articlesStore.loading" class="loading">
      Loading article...
    </div>
    
    <div v-else class="not-found">
      Article not found.
    </div>
  </div>
</template>

<style scoped>
.article-detail-page {
  max-width: 800px;
  margin: 0 auto;
}

.article-header {
  margin-bottom: 32px;
}

.article-header h1 {
  font-size: 2rem;
  margin-bottom: 16px;
}

.article-meta {
  display: flex;
  gap: 16px;
  color: #666;
  margin-bottom: 16px;
}

.author {
  color: #42b883;
  text-decoration: none;
  font-weight: 500;
}

.article-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 12px;
}

.tag {
  color: #42b883;
  text-decoration: none;
}

.tag:hover {
  text-decoration: underline;
}

.article-categories {
  display: flex;
  gap: 8px;
  margin-bottom: 16px;
}

.category {
  background: #f0f0f0;
  padding: 4px 12px;
  border-radius: 4px;
  font-size: 0.9rem;
  color: #666;
  text-decoration: none;
}

.article-actions {
  display: flex;
  gap: 12px;
}

.btn-edit {
  padding: 8px 16px;
  background: #666;
  color: white;
  text-decoration: none;
  border-radius: 4px;
}

.btn-delete {
  padding: 8px 16px;
  background: #e74c3c;
  color: white;
}

.article-content {
  line-height: 1.8;
}

.summary {
  font-size: 1.1rem;
  color: #666;
  margin-bottom: 24px;
  padding-bottom: 24px;
  border-bottom: 1px solid #eee;
}

.content {
  white-space: pre-wrap;
}

.loading,
.not-found {
  text-align: center;
  padding: 40px;
  color: #666;
}
</style>
