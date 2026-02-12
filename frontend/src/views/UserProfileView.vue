<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import { usersApi, articlesApi } from '@/services/api'
import type { User, Article, UserProfile } from '@/types'
import UserCard from '@/components/users/UserCard.vue'
import ArticleCard from '@/components/articles/ArticleCard.vue'

const route = useRoute()

const user = ref<UserProfile | null>(null)
const articles = ref<Article[]>([])
const loading = ref(true)
const error = ref<string | null>(null)

onMounted(async () => {
  await fetchUser()
})

async function fetchUser() {
  loading.value = true
  error.value = null
  
  try {
    const userId = route.params.id as string
    const response = await usersApi.getProfile(userId)
    user.value = response.data
    
    const articlesResponse = await articlesApi.list({ limit: 10 })
    articles.value = articlesResponse.data.articles.filter(
      (a: Article) => a.author.id === userId
    )
  } catch (err) {
    error.value = 'Failed to load user profile'
    console.error(err)
  } finally {
    loading.value = false
  }
}

function handleConnectionChanged() {
  fetchUser()
}
</script>

<template>
  <div class="user-profile-page">
    <div v-if="loading" class="loading">
      Loading profile...
    </div>
    
    <div v-else-if="error" class="error">
      {{ error }}
    </div>
    
    <template v-else-if="user">
      <UserCard
        :user="user"
        :is-following="user.isFollowing"
        @connection-changed="handleConnectionChanged"
      />
      
      <section class="user-articles">
        <h2>Articles by {{ user.displayName || user.username }}</h2>
        
        <div v-if="articles.length === 0" class="no-articles">
          No articles yet.
        </div>
        
        <div v-else class="articles-list">
          <ArticleCard
            v-for="article in articles"
            :key="article.id"
            :article="article"
          />
        </div>
      </section>
    </template>
  </div>
</template>

<style scoped>
.user-profile-page {
  max-width: 800px;
  margin: 0 auto;
}

.loading,
.error,
.no-articles {
  text-align: center;
  padding: 40px;
  color: #666;
}

.error {
  color: #e74c3c;
}

.user-articles {
  margin-top: 32px;
}

.user-articles h2 {
  margin-bottom: 24px;
}

.articles-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}
</style>
