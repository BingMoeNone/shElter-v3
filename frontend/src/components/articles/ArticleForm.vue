<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import type { Article } from '@/types'
import { useArticlesStore } from '@/stores/articles'
import { useRouter } from 'vue-router'
import { mediaApi } from '@/services/api'
import type Quill from 'quill'

const props = defineProps<{
  article?: Article
  mode: 'create' | 'edit'
}>()

const emit = defineEmits<{
  saved: [article: Article]
}>()

const articlesStore = useArticlesStore()
const router = useRouter()

const title = ref(props.article?.title || '')
const content = ref(props.article?.content || '')
const summary = ref(props.article?.summary || '')
const tagNames = ref(props.article?.tags.map(t => t.name).join(', ') || '')
const saving = ref(false)
const error = ref<string | null>(null)
const quillEditor = ref<InstanceType<typeof Quill> | null>(null)

// 澶勭悊鍥剧墖涓婁紶
const handleImageUpload = async (file: File) => {
  try {
    const response = await mediaApi.uploadFile(file)
    return response.data.url
  } catch (err) {
    console.error('Image upload failed:', err)
    throw new Error('鍥剧墖涓婁紶澶辫触')
  }
}

const editorOptions = {
  theme: 'snow',
  modules: {
    toolbar: {
      container: [
        [{ header: [1, 2, 3, false] }],
        ['bold', 'italic', 'underline', 'strike'],
        [{ list: 'ordered' }, { list: 'bullet' }],
        [{ indent: '-1' }, { indent: '+1' }],
        [{ align: [] }],
        ['link', 'image'],
        ['clean']
      ],
      handlers: {
        image: function() {
          const input = document.createElement('input')
          input.setAttribute('type', 'file')
          input.setAttribute('accept', 'image/*')
          input.click()
          
          input.onchange = async (e: Event) => {
            const target = e.target as HTMLInputElement
            if (target.files && target.files[0]) {
              const file = target.files[0]
              try {
                const url = await handleImageUpload(file)
                const range = this.quill.getSelection(true)
                this.quill.insertEmbed(range.index, 'image', url)
              } catch (err) {
                console.error('Image insertion failed:', err)
              }
            }
          }
        }
      }
    }
  },
  placeholder: 'Write your article content here...',
  readOnly: false
}

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
      <QuillEditor
        id="content"
        v-model="content"
        placeholder="Write your article content here..."
        :options="editorOptions"
        class="rich-text-editor"
        @editor-ready="(editor) => quillEditor = editor"
      />
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
  background: var(--color-surface);
  padding: 30px;
  border-radius: 8px;
  border: 1px solid var(--color-primary);
  box-shadow: 0 0 15px rgba(0, 255, 157, 0.1);
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  color: var(--color-text);
}

.form-group input,
.form-group textarea {
  width: 100%;
  padding: 12px;
  background: rgba(0, 0, 0, 0.5);
  border: 1px solid var(--color-border);
  border-radius: 4px;
  font-size: 14px;
  color: var(--color-text);
  font-family: var(--font-family-base);
  transition: all 0.3s;
}

.form-group input:focus,
.form-group textarea:focus {
  border-color: var(--color-primary);
  box-shadow: 0 0 10px rgba(0, 255, 157, 0.2);
}

.rich-text-editor {
      min-height: 400px;
      border: 1px solid var(--color-border);
      border-radius: 4px;
    }

    .rich-text-editor :deep(.ql-container) {
      font-family: var(--font-family-base);
      color: var(--color-text);
      min-height: 300px;
    }

    .rich-text-editor :deep(.ql-editor) {
      font-size: 14px;
      line-height: 1.6;
    }

    .rich-text-editor :deep(.ql-toolbar) {
      background: rgba(0, 0, 0, 0.3);
      border-bottom: 1px solid var(--color-border);
    }

    .rich-text-editor :deep(.ql-toolbar button:hover),
    .rich-text-editor :deep(.ql-toolbar .ql-picker-label:hover) {
      color: var(--color-primary);
    }

    .error-message {
      color: #ff4444;
      margin-bottom: 16px;
      padding: 12px;
      background: rgba(255, 68, 68, 0.1);
      border-radius: 4px;
      border-left: 3px solid #ff4444;
    }

.form-actions {
  display: flex;
  gap: 12px;
}

.btn-save {
  background: rgba(255, 255, 255, 0.1);
  color: var(--color-text);
  border: 1px solid var(--color-border);
  padding: 10px 20px;
  border-radius: 4px;
  transition: all 0.3s;
}

.btn-publish {
  background: rgba(0, 255, 157, 0.1);
  color: var(--color-primary);
  border: 1px solid var(--color-primary);
  padding: 10px 20px;
  border-radius: 4px;
  transition: all 0.3s;
}

.btn-save:hover:not(:disabled) {
  background: var(--color-surface-hover);
  border-color: var(--color-text);
}

.btn-publish:hover:not(:disabled) {
  background: var(--color-primary);
  color: #000;
  box-shadow: 0 0 15px var(--color-primary);
}

button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
</style>
