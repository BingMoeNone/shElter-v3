<script setup lang="ts">
import { ref, computed } from 'vue'
import type { Article } from '@/types'
import { useArticlesStore } from '@/stores/articles'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'

const props = defineProps<{
  article?: Article
  mode: 'create' | 'edit'
}>()

const emit = defineEmits<{
  saved: [article: Article]
}>()

const articlesStore = useArticlesStore()
const authStore = useAuthStore()
const router = useRouter()

const title = ref(props.article?.title || '')
const content = ref(props.article?.content || '')
const summary = ref(props.article?.summary || '')
const tagNames = ref(props.article?.tags.map(t => t.name).join(', ') || '')
const saving = ref(false)
const error = ref<string | null>(null)

const canSubmit = computed(() => {
  return title.value.trim() && content.value.trim().length >= 10
})

async function handleSubmit(publish: boolean = false) {
  if (!canSubmit.value || saving.value) return
  
  saving.value = true
  error.value = null
  
  try {
    const data = {
      title: title.value,
      content: content.value,
      summary: summary.value || undefined,
      tagNames: tagNames.value.split(',').map(t => t.trim()).filter(Boolean),
      status: publish ? 'published' : 'draft',
    }
    
    let article: Article
    
    if (props.mode === 'create') {
      article = await articlesStore.createArticle(data)
    } else if (props.article) {
      article = await articlesStore.updateArticle(props.article.id, data)
      if (publish && props.article.status !== 'published') {
        article = await articlesStore.publishArticle(props.article.id)
      }
    } else {
      throw new Error('No article to edit')
    }
    
    emit('saved', article)
    router.push(`/articles/${article.id}`)
  } catch (err) {
    error.value = 'Failed to save article. Please try again.'
    console.error(err)
  } finally {
    saving.value = false
  }
}
</script>

<template>
  <form class="article-form" @submit.prevent="handleSubmit(false)">
    <div class="form-group">
      <label for="title">Title</label>
      <input
        id="title"
        v-model="title"
        type="text"
        placeholder="Enter article title"
        required
        maxlength="200"
      />
    </div>
    
    <div class="form-group">
      <label for="summary">Summary (optional)</label>
      <input
        id="summary"
        v-model="summary"
        type="text"
        placeholder="Brief summary of the article"
        maxlength="500"
      />
    </div>
    
    <div class="form-group">
      <label for="content">Content</label>
      <textarea
        id="content"
        v-model="content"
        placeholder="Write your article content here..."
        rows="15"
        required
        minlength="10"
      ></textarea>
    </div>
    
    <div class="form-group">
      <label for="tags">Tags (comma-separated)</label>
      <input
        id="tags"
        v-model="tagNames"
        type="text"
        placeholder="tag1, tag2, tag3"
      />
    </div>
    
    <div v-if="error" class="error-message">{{ error }}</div>
    
    <div class="form-actions">
      <button type="submit" :disabled="!canSubmit || saving" class="btn-save">
        {{ saving ? 'Saving...' : 'Save Draft' }}
      </button>
      <button
        type="button"
        :disabled="!canSubmit || saving"
        class="btn-publish"
        @click="handleSubmit(true)"
      >
        {{ saving ? 'Publishing...' : 'Publish' }}
      </button>
    </div>
  </form>
</template>

<style scoped>
.article-form {
  max-width: 800px;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  color: #333;
}

.form-group input,
.form-group textarea {
  width: 100%;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
}

.form-group textarea {
  resize: vertical;
  min-height: 300px;
  font-family: inherit;
}

.error-message {
  color: #e74c3c;
  margin-bottom: 16px;
  padding: 12px;
  background: #fdf2f2;
  border-radius: 4px;
}

.form-actions {
  display: flex;
  gap: 12px;
}

.btn-save {
  background: #666;
}

.btn-publish {
  background: #42b883;
}

.btn-save:hover:not(:disabled) {
  background: #555;
}

.btn-publish:hover:not(:disabled) {
  background: #3aa876;
}
</style>
