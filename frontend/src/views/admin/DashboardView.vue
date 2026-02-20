<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { adminApi } from '@/services/api'

const router = useRouter()
const loading = ref(true)
const stats = ref({
  totalUsers: 0,
  totalArticles: 0,
  totalComments: 0,
  pendingArticles: 0,
  pendingComments: 0,
})

onMounted(async () => {
  try {
    // Get dashboard statistics from API
    const [usersRes, articlesRes, commentsRes, moderationRes] = await Promise.all([
      adminApi.getUsers({ page: 1, limit: 1 }),
      adminApi.getArticles({ page: 1, limit: 1 }),
      adminApi.getComments({ page: 1, limit: 1 }),
      adminApi.getModerationStats()
    ])
    
    stats.value = {
      totalUsers: usersRes.data.pagination.total_items,
      totalArticles: articlesRes.data.pagination.total_items,
      totalComments: commentsRes.data.pagination.total_items,
      pendingArticles: moderationRes.data.pending_articles,
      pendingComments: moderationRes.data.pending_comments
    }
  } catch (error) {
    console.error('Failed to fetch dashboard stats:', error)
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <div class="admin-dashboard">
    <h1 class="dashboard-title">绠＄悊鍛樹华琛ㄧ洏</h1>
    
    <div class="dashboard-grid">
      <div class="stat-card">
        <div class="stat-icon users-icon">馃懃</div>
        <div class="stat-content">
          <div class="stat-value">{{ stats.totalUsers }}</div>
          <div class="stat-label">鎬荤敤鎴锋暟</div>
          <button class="stat-action" @click="router.push('/admin/users')">鏌ョ湅鐢ㄦ埛</button>
        </div>
      </div>
      
      <div class="stat-card">
        <div class="stat-icon articles-icon">馃摑</div>
        <div class="stat-content">
          <div class="stat-value">{{ stats.totalArticles }}</div>
          <div class="stat-label">鎬绘枃绔犳暟</div>
          <button class="stat-action" @click="router.push('/admin/articles')">鏌ョ湅鏂囩珷</button>
        </div>
      </div>
      
      <div class="stat-card">
        <div class="stat-icon comments-icon">馃挰</div>
        <div class="stat-content">
          <div class="stat-value">{{ stats.totalComments }}</div>
          <div class="stat-label">鎬昏瘎璁烘暟</div>
          <button class="stat-action" @click="router.push('/admin/comments')">鏌ョ湅璇勮</button>
        </div>
      </div>
      
      <div class="stat-card warning">
        <div class="stat-icon pending-icon">鈴?/div>
        <div class="stat-content">
          <div class="stat-value">{{ stats.pendingArticles }}</div>
          <div class="stat-label">寰呭鏍告枃绔?/div>
          <button class="stat-action" @click="router.push('/admin/moderation')">瀹℃牳鏂囩珷</button>
        </div>
      </div>
      
      <div class="stat-card warning">
        <div class="stat-icon pending-icon">鈴?/div>
        <div class="stat-content">
          <div class="stat-value">{{ stats.pendingComments }}</div>
          <div class="stat-label">寰呭鏍歌瘎璁?/div>
          <button class="stat-action" @click="router.push('/admin/moderation')">瀹℃牳璇勮</button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.admin-dashboard {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.dashboard-title {
  font-size: 2rem;
  color: var(--color-primary);
  margin-bottom: 30px;
  text-align: center;
}

.dashboard-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.stat-card {
  background: var(--color-surface);
  padding: 25px;
  border-radius: 8px;
  border: 1px solid var(--color-border);
  box-shadow: 0 0 15px rgba(0, 255, 157, 0.1);
  display: flex;
  align-items: center;
  transition: all 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 20px rgba(0, 255, 157, 0.2);
}

.stat-card.warning {
  border-color: #ffcc00;
  background: rgba(255, 204, 0, 0.05);
}

.stat-icon {
  font-size: 3rem;
  margin-right: 20px;
  flex-shrink: 0;
}

.users-icon {
  color: #4facfe;
}

.articles-icon {
  color: #00f2fe;
}

.comments-icon {
  color: #43e97b;
}

.pending-icon {
  color: #ffcc00;
}

.stat-content {
  flex: 1;
}

.stat-value {
  font-size: 2.5rem;
  font-weight: bold;
  color: var(--color-text);
  margin-bottom: 5px;
}

.stat-label {
  font-size: 1rem;
  color: var(--color-text-muted);
  margin-bottom: 15px;
}

.stat-action {
  background: rgba(0, 255, 157, 0.1);
  color: var(--color-primary);
  border: 1px solid var(--color-primary);
  padding: 8px 15px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: all 0.3s ease;
}

.stat-action:hover {
  background: var(--color-primary);
  color: #000;
  box-shadow: 0 0 10px var(--color-primary);
}
</style>
