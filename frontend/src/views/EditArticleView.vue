<script setup lang="ts">
import { onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useArticlesStore } from '@/stores/articles'
import { useAuthStore } from '@/stores/auth'
import ArticleForm from '@/components/articles/ArticleForm.vue'

const articlesStore = useArticlesStore()
const authStore = useAuthStore()
const route = useRoute()
const router = useRouter()

const articleId = computed(() => route.params.id as string)

onMounted(async () => {
  await articlesStore.fetchArticle(articleId.value)
  
  if (articlesStore.currentArticle && 
      articlesStore.currentArticle.author.id !== authStore.user?.id &&
      !authStore.isAdmin) {
    router.push(`/articles/${articleId.value}`)
  }
})

const article = computed(() => articlesStore.currentArticle)
</script>

<template>
  <div class="edit-article-page">
    <template v-if="article">
      <h1>Edit Article: {{ article.title }}</h1>
      <ArticleForm mode="edit" :article="article" />
    </template>
    
    <div v-else-if="articlesStore.loading" class="loading">
      Loading article...
    </div>
  </div>
</template>

<style scoped>
.edit-article-page {
  max-width: 800px;
  margin: 0 auto;
}

.edit-article-page h1 {
  margin-bottom: 24px;
}

.loading {
  text-align: center;
  padding: 40px;
  color: #666;
}
</style>
