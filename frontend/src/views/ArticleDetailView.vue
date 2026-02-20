<script setup lang="ts">
import { onMounted, ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useArticlesStore } from '@/stores/articles'
import { useAuthStore } from '@/stores/auth'
import { commentsApi } from '@/services/api'
import type { Comment } from '@/types'
import CommentSection from '@/components/comments/CommentSection.vue'
import { useToastStore } from '@/stores/toast'

const articlesStore = useArticlesStore()
const authStore = useAuthStore()
const route = useRoute()
const router = useRouter()
const toast = useToastStore()

const articleId = computed(() => route.params.id as string)
const comments = ref<Comment[]>([])
const deleting = ref(false)

onMounted(async () => {
  await articlesStore.fetchArticle(articleId.value)
  await fetchComments()
})

const article = computed(() => articlesStore.currentArticle)

async function fetchComments() {
  try {
    const response = await commentsApi.getByArticle?.(articleId.value)
    if (response) {
      comments.value = response.data || []
    }
  } catch (err: any) {
    console.error('Failed to fetch comments:', err)
    toast.error('鍔犺浇璇勮澶辫触')
  }
}

function handleCommentAdded(comment: Comment) {
  comments.value.unshift(comment)
}

function handleCommentDeleted(commentId: string) {
  comments.value = comments.value.filter(c => c.id !== commentId)
}

function formatDate(date: string) {
  return new Date(date).toLocaleDateString('zh-CN', {
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
  if (!confirm('纭畾瑕佸垹闄よ繖绡囨枃绔犲悧锛熸鎿嶄綔涓嶅彲鎾ら攢銆?)) return
  
  deleting.value = true
  
  try {
    await articlesStore.deleteArticle(articleId.value)
    toast.success('鏂囩珷宸插垹闄?)
    router.push('/articles')
  } catch (err: any) {
    console.error('Failed to delete article:', err)
    toast.error(err.response?.data?.message || '鍒犻櫎鏂囩珷澶辫触')
  } finally {
    deleting.value = false
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
              缂栬緫
            </RouterLink>
            <button @click="handleDelete" class="btn-delete" :disabled="deleting">
              {{ deleting ? '鍒犻櫎涓?..' : '鍒犻櫎' }}
            </button>
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
  color: var(--color-text);
}

.article-header {
  margin-bottom: 32px;
  border-bottom: 1px solid var(--color-primary);
  padding-bottom: 20px;
}

.article-header h1 {
  font-size: 2rem;
  margin-bottom: 16px;
  color: var(--color-primary);
  text-shadow: 0 0 10px var(--color-primary);
  font-family: var(--font-family-heading);
}

.article-meta {
  display: flex;
  gap: 16px;
  color: var(--color-text-muted);
  margin-bottom: 16px;
}

.author {
  color: var(--color-accent);
  text-decoration: none;
  font-weight: 500;
}

.author:hover {
  text-shadow: 0 0 5px var(--color-accent);
}

.article-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 12px;
}

.tag {
  color: var(--color-primary);
  text-decoration: none;
  transition: all 0.2s;
}

.tag:hover {
  text-shadow: 0 0 5px var(--color-primary);
}

.article-categories {
  display: flex;
  gap: 8px;
  margin-bottom: 16px;
}

.category {
  background: rgba(255, 255, 255, 0.05);
  padding: 4px 12px;
  border: 1px solid var(--color-border);
  border-radius: 4px;
  font-size: 0.9rem;
  color: var(--color-text-muted);
  text-decoration: none;
  transition: all 0.2s;
}

.category:hover {
  border-color: var(--color-secondary);
  color: var(--color-secondary);
  box-shadow: 0 0 5px var(--color-secondary);
}

.article-actions {
  display: flex;
  gap: 12px;
}

.btn-edit {
  padding: 8px 16px;
  background: rgba(255, 255, 255, 0.1);
  color: var(--color-text);
  text-decoration: none;
  border-radius: 4px;
  border: 1px solid var(--color-border);
  transition: all 0.3s;
}

.btn-edit:hover {
  background: var(--color-surface-hover);
  border-color: var(--color-text);
}

.btn-delete {
  padding: 8px 16px;
  background: rgba(255, 68, 68, 0.1);
  color: #ff4444;
  border: 1px solid #ff4444;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-delete:hover {
  background: #ff4444;
  color: #fff;
  box-shadow: 0 0 10px #ff4444;
}

.article-content {
  line-height: 1.8;
  font-size: 1.1rem;
}

.summary {
  font-size: 1.2rem;
  color: var(--color-text-muted);
  margin-bottom: 24px;
  padding: 20px;
  border: 1px solid var(--color-primary);
  border-radius: 4px;
  background: rgba(0, 255, 157, 0.05);
  font-style: italic;
}

.content {
  white-space: pre-wrap;
}

.content :deep(h2),
.content :deep(h3) {
  color: var(--color-secondary);
  margin-top: 1.5em;
  margin-bottom: 0.5em;
}

.content :deep(a) {
  color: var(--color-accent);
}

.content :deep(code) {
  background: rgba(255, 255, 255, 0.1);
  padding: 2px 6px;
  border-radius: 4px;
  font-family: monospace;
  color: var(--color-primary);
}

.content :deep(pre) {
  background: #111;
  padding: 16px;
  border-radius: 8px;
  overflow-x: auto;
  border: 1px solid var(--color-border);
}

.loading,
.not-found {
  text-align: center;
  padding: 40px;
  color: var(--color-text-muted);
  border: 1px dashed var(--color-text-muted);
  border-radius: 8px;
}
</style>
