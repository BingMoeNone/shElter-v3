<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { adminApi } from '@/services/api'

const router = useRouter()
const activeTab = ref('articles') // 'articles' or 'comments'
const pendingArticles = ref([])
const pendingComments = ref([])
const loading = ref({
  articles: true,
  comments: true
})
const currentPage = ref({
  articles: 1,
  comments: 1
})
const limit = ref(20)
const totalItems = ref({
  articles: 0,
  comments: 0
})
const totalPages = ref({
  articles: 0,
  comments: 0
})

const fetchPendingArticles = async () => {
  loading.value.articles = true
  try {
    const response = await adminApi.getPendingArticles({
      page: currentPage.value.articles,
      limit: limit.value
    })
    pendingArticles.value = response.data.articles
    totalItems.value.articles = response.data.pagination.total_items
    totalPages.value.articles = response.data.pagination.total_pages
  } catch (error) {
    console.error('Failed to fetch pending articles:', error)
  } finally {
    loading.value.articles = false
  }
}

const fetchPendingComments = async () => {
  loading.value.comments = true
  try {
    const response = await adminApi.getPendingComments({
      page: currentPage.value.comments,
      limit: limit.value
    })
    pendingComments.value = response.data.comments
    totalItems.value.comments = response.data.pagination.total_items
    totalPages.value.comments = response.data.pagination.total_pages
  } catch (error) {
    console.error('Failed to fetch pending comments:', error)
  } finally {
    loading.value.comments = false
  }
}

const handleApproveArticle = async (articleId: string) => {
  try {
    await adminApi.approveArticle(articleId)
    fetchPendingArticles()
  } catch (error) {
    console.error('Failed to approve article:', error)
  }
}

const handleRejectArticle = async (articleId: string) => {
  try {
    await adminApi.rejectArticle(articleId)
    fetchPendingArticles()
  } catch (error) {
    console.error('Failed to reject article:', error)
  }
}

const handleApproveComment = async (commentId: string) => {
  try {
    await adminApi.approveComment(commentId)
    fetchPendingComments()
  } catch (error) {
    console.error('Failed to approve comment:', error)
  }
}

const handleRejectComment = async (commentId: string) => {
  try {
    await adminApi.rejectComment(commentId)
    fetchPendingComments()
  } catch (error) {
    console.error('Failed to reject comment:', error)
  }
}

const handlePageChange = (page: number, type: 'articles' | 'comments') => {
  currentPage.value[type] = page
  if (type === 'articles') {
    fetchPendingArticles()
  } else {
    fetchPendingComments()
  }
}

const handleViewArticle = (articleId: string) => {
  router.push(`/articles/${articleId}`)
}

const switchTab = (tab: 'articles' | 'comments') => {
  activeTab.value = tab
  if (tab === 'comments' && pendingComments.value.length === 0) {
    fetchPendingComments()
  }
}

onMounted(() => {
  fetchPendingArticles()
})
</script>

<template>
  <div class="admin-moderation">
    <h1 class="page-title">鍐呭瀹℃牳</h1>
    
    <div class="moderation-tabs">
      <button 
        class="tab-btn" 
        :class="{ active: activeTab === 'articles' }"
        @click="switchTab('articles')"
      >
        寰呭鏍告枃绔?        <span class="tab-count">{{ totalItems.articles }}</span>
      </button>
      <button 
        class="tab-btn" 
        :class="{ active: activeTab === 'comments' }"
        @click="switchTab('comments')"
      >
        寰呭鏍歌瘎璁?        <span class="tab-count">{{ totalItems.comments }}</span>
      </button>
    </div>
    
    <!-- Articles Tab -->
    <div v-if="activeTab === 'articles'" class="tab-content">
      <div v-if="loading.articles" class="loading">鍔犺浇涓?..</div>
      
      <div v-else class="articles-table-container">
        <table v-if="pendingArticles.length > 0" class="moderation-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>鏍囬</th>
              <th>浣滆€?/th>
              <th>鍒涘缓鏃堕棿</th>
              <th>鎿嶄綔</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="article in pendingArticles" :key="article.id">
              <td>{{ article.id }}</td>
              <td class="article-title">{{ article.title }}</td>
              <td>{{ article.author.username }}</td>
              <td>{{ new Date(article.created_at).toLocaleString() }}</td>
              <td>
                <div class="action-buttons">
                  <button class="btn btn-view" @click="handleViewArticle(article.id)">鏌ョ湅</button>
                  <button class="btn btn-approve" @click="handleApproveArticle(article.id)">鎵瑰噯</button>
                  <button class="btn btn-reject" @click="handleRejectArticle(article.id)">鎷掔粷</button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
        
        <div v-else class="empty-state">
          娌℃湁寰呭鏍哥殑鏂囩珷
        </div>
        
        <div v-if="totalPages.articles > 1" class="pagination">
          <button 
            class="page-btn" 
            @click="handlePageChange(currentPage.articles - 1, 'articles')"
            :disabled="currentPage.articles === 1"
          >
            涓婁竴椤?          </button>
          
          <span class="page-info">
            绗?{{ currentPage.articles }} / {{ totalPages.articles }} 椤?          </span>
          
          <button 
            class="page-btn" 
            @click="handlePageChange(currentPage.articles + 1, 'articles')"
            :disabled="currentPage.articles === totalPages.articles"
          >
            涓嬩竴椤?          </button>
        </div>
      </div>
    </div>
    
    <!-- Comments Tab -->
    <div v-else class="tab-content">
      <div v-if="loading.comments" class="loading">鍔犺浇涓?..</div>
      
      <div v-else class="comments-table-container">
        <table v-if="pendingComments.length > 0" class="moderation-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>鍐呭</th>
              <th>浣滆€?/th>
              <th>鏂囩珷</th>
              <th>鍒涘缓鏃堕棿</th>
              <th>鎿嶄綔</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="comment in pendingComments" :key="comment.id">
              <td>{{ comment.id }}</td>
              <td class="comment-content">{{ comment.content }}</td>
              <td>{{ comment.author.username }}</td>
              <td>
                <button class="article-link" @click="handleViewArticle(comment.article_id)">
                  鏌ョ湅鏂囩珷
                </button>
              </td>
              <td>{{ new Date(comment.created_at).toLocaleString() }}</td>
              <td>
                <div class="action-buttons">
                  <button class="btn btn-approve" @click="handleApproveComment(comment.id)">鎵瑰噯</button>
                  <button class="btn btn-reject" @click="handleRejectComment(comment.id)">鎷掔粷</button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
        
        <div v-else class="empty-state">
          娌℃湁寰呭鏍哥殑璇勮
        </div>
        
        <div v-if="totalPages.comments > 1" class="pagination">
          <button 
            class="page-btn" 
            @click="handlePageChange(currentPage.comments - 1, 'comments')"
            :disabled="currentPage.comments === 1"
          >
            涓婁竴椤?          </button>
          
          <span class="page-info">
            绗?{{ currentPage.comments }} / {{ totalPages.comments }} 椤?          </span>
          
          <button 
            class="page-btn" 
            @click="handlePageChange(currentPage.comments + 1, 'comments')"
            :disabled="currentPage.comments === totalPages.comments"
          >
            涓嬩竴椤?          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.admin-moderation {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.page-title {
  font-size: 2rem;
  color: var(--color-primary);
  margin-bottom: 20px;
  text-align: center;
}

.moderation-tabs {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
  border-bottom: 2px solid var(--color-border);
}

.tab-btn {
  padding: 10px 20px;
  background: var(--color-surface);
  color: var(--color-text);
  border: none;
  border-radius: 4px 4px 0 0;
  cursor: pointer;
  font-size: 1rem;
  font-weight: bold;
  transition: all 0.3s ease;
  position: relative;
  top: 2px;
}

.tab-btn:hover {
  background: rgba(0, 255, 157, 0.1);
  color: var(--color-primary);
}

.tab-btn.active {
  background: var(--color-primary);
  color: #000;
  box-shadow: 0 0 10px rgba(0, 255, 157, 0.3);
}

.tab-count {
  background: rgba(255, 255, 255, 0.2);
  color: var(--color-text);
  border-radius: 10px;
  padding: 2px 8px;
  font-size: 0.8rem;
  margin-left: 8px;
}

.tab-btn.active .tab-count {
  background: rgba(0, 0, 0, 0.3);
  color: #fff;
}

.tab-content {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: 0 4px 4px 4px;
  padding: 20px;
  box-shadow: 0 0 15px rgba(0, 255, 157, 0.1);
}

.loading {
  text-align: center;
  font-size: 1.2rem;
  color: var(--color-text-muted);
  padding: 40px;
}

.moderation-table-container {
  overflow-x: auto;
}

.moderation-table {
  width: 100%;
  border-collapse: collapse;
  background: var(--color-surface);
  border-radius: 8px;
  overflow: hidden;
}

.moderation-table th,
.moderation-table td {
  padding: 12px;
  text-align: left;
  border-bottom: 1px solid var(--color-border);
}

.moderation-table th {
  background: rgba(0, 255, 157, 0.1);
  color: var(--color-primary);
  font-weight: bold;
  font-size: 0.9rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.moderation-table tr:last-child td {
  border-bottom: none;
}

.moderation-table tr:hover {
  background: rgba(0, 255, 157, 0.05);
}

.article-title {
  max-width: 300px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.comment-content {
  max-width: 400px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.article-link {
  background: none;
  border: none;
  color: var(--color-primary);
  text-decoration: underline;
  cursor: pointer;
  font-size: 0.9rem;
  padding: 0;
}

.article-link:hover {
  color: #00c853;
}

.action-buttons {
  display: flex;
  gap: 8px;
}

.btn {
  padding: 6px 12px;
  border: 1px solid var(--color-border);
  border-radius: 4px;
  font-size: 0.8rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-view {
  background: rgba(79, 172, 254, 0.1);
  color: #4facfe;
}

.btn-approve {
  background: rgba(67, 233, 123, 0.1);
  color: #43e97b;
}

.btn-reject {
  background: rgba(255, 107, 107, 0.1);
  color: #ff6b6b;
}

.btn-view:hover {
  background: #4facfe;
  color: #fff;
}

.btn-approve:hover {
  background: #43e97b;
  color: #000;
}

.btn-reject:hover {
  background: #ff6b6b;
  color: #fff;
}

.empty-state {
  text-align: center;
  font-size: 1.2rem;
  color: var(--color-text-muted);
  padding: 40px;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 20px;
  gap: 10px;
}

.page-btn {
  padding: 8px 16px;
  background: rgba(0, 255, 157, 0.1);
  color: var(--color-primary);
  border: 1px solid var(--color-primary);
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.page-btn:hover:not(:disabled) {
  background: var(--color-primary);
  color: #000;
}

.page-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.page-info {
  font-size: 0.9rem;
  color: var(--color-text-muted);
}
</style>
