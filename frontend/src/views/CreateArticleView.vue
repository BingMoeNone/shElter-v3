<script setup lang="ts">
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import ArticleForm from '@/components/articles/ArticleForm.vue'

const authStore = useAuthStore()
const router = useRouter()

onMounted(() => {
  if (!authStore.isAuthenticated) {
    router.push('/login?redirect=/articles/create')
  }
})
</script>

<template>
  <div class="create-article-page">
    <h1>Create New Article</h1>
    
    <ArticleForm mode="create" />
  </div>
</template>

<style scoped>
.create-article-page {
  max-width: 800px;
  margin: 0 auto;
}

.create-article-page h1 {
  margin-bottom: 24px;
}
</style>
