<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { adminApi } from '@/services/api'

const router = useRouter()
const comments = ref([])
const loading = ref(true)
const searchQuery = ref('')
const currentPage = ref(1)
const limit = ref(20)
const totalItems = ref(0)
const totalPages = ref(0)
const articleIdFilter = ref('')

const fetchComments = async () => {
  loading.value = true
  try {
    const response = await adminApi.getComments({
      page: currentPage.value,
      limit: limit.value,
      article_id: articleIdFilter.value || undefined
    })
    comments.value = response.data.comments
    totalItems.value = response.data.pagination.total_items
    totalPages.value = response.data.pagination.total_pages
  } catch (error) {
    console.error('Failed to fetch comments:', error)
  } finally {
    loading.value = false
  }
}

const handleSearch = () => {
  currentPage.value = 1
  fetchComments()
}

const handleArticleFilterChange = () => {
  currentPage.value = 1
  fetchComments()
}

const handlePageChange = (page: number) => {
  currentPage.value = page
  fetchComments()
}

const handleViewArticle = (articleId: string) => {
  router.push(`/articles/${articleId}`)
}

const handleDeleteComment = async (commentId: string) => {
  if (confirm('纭畾瑕佸垹闄よ繖涓瘎璁哄悧锛?)) {
    try {
      await adminApi.deleteComment(commentId)
      fetchComments()
    } catch (error) {
      console.error('Failed to delete comment:', error)
    }
  }
}

onMounted(() => {
  fetchComments()
})
</script>

<template>
  <div class="admin-comments">
    <h1 class="page-title">璇勮绠＄悊</h1>
    
    <div class="comments-header">
      <div class="search-bar">
        <input
          type="text"
          v-model="searchQuery"
          placeholder="鎼滅储璇勮鍐呭..."
          @input="handleSearch"
        />
      </div>
      <div class="filter-bar">
        <input
          type="text"
          v-model="articleIdFilter"
          placeholder="鎸夋枃绔營D杩囨护..."
          @input="handleArticleFilterChange"
        />
      </div>
    </div>
    
    <div v-if="loading" class="loading">鍔犺浇涓?..</div>
    
    <div v-else class="comments-table-container">
      <table class="comments-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>鍐呭</th>
            <th>浣滆€?/th>
            <th>鏂囩珷</th>
            <th>鐘舵€?/th>
            <th>鍒涘缓鏃堕棿</th>
            <th>鎿嶄綔</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="comment in comments" :key="comment.id">
            <td>{{ comment.id }}</td>
            <td class="comment-content">{{ comment.content }}</td>
            <td>{{ comment.author.username }}</td>
            <td>
              <button class="article-link" @click="handleViewArticle(comment.article_id)">
                鏌ョ湅鏂囩珷
              </button>
            </td>
            <td>
              <span :class="`status-badge status-${comment.is_approved ? 'approved' : 'pending'}`">
                {{ comment.is_approved ? '宸叉壒鍑? : '寰呮壒鍑? }}
              </span>
            </td>
            <td>{{ new Date(comment.created_at).toLocaleString() }}</td>
            <td>
              <div class="action-buttons">
                <button class="btn btn-delete" @click="handleDeleteComment(comment.id)">鍒犻櫎</button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
      
      <div v-if="totalPages > 1" class="pagination">
        <button 
          class="page-btn" 
          @click="handlePageChange(currentPage - 1)"
          :disabled="currentPage === 1"
        >
          涓婁竴椤?        </button>
        
        <span class="page-info">
          绗?{{ currentPage }} / {{ totalPages }} 椤?        </span>
        
        <button 
          class="page-btn" 
          @click="handlePageChange(currentPage + 1)"
          :disabled="currentPage === totalPages"
        >
          涓嬩竴椤?        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.admin-comments {
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

.comments-header {
  display: flex;
  gap: 20px;
  margin-bottom: 20px;
  flex-wrap: wrap;
}

.search-bar {
  flex: 1;
  min-width: 250px;
}

.search-bar input {
  width: 100%;
  padding: 10px;
  background: rgba(0, 0, 0, 0.5);
  border: 1px solid var(--color-border);
  border-radius: 4px;
  color: var(--color-text);
  font-size: 1rem;
}

.search-bar input:focus {
  outline: none;
  border-color: var(--color-primary);
  box-shadow: 0 0 10px rgba(0, 255, 157, 0.2);
}

.filter-bar {
  min-width: 200px;
}

.filter-bar input {
  width: 100%;
  padding: 10px;
  background: rgba(0, 0, 0, 0.5);
  border: 1px solid var(--color-border);
  border-radius: 4px;
  color: var(--color-text);
  font-size: 1rem;
}

.filter-bar input:focus {
  outline: none;
  border-color: var(--color-primary);
  box-shadow: 0 0 10px rgba(0, 255, 157, 0.2);
}

.loading {
  text-align: center;
  font-size: 1.2rem;
  color: var(--color-text-muted);
  padding: 40px;
}

.comments-table-container {
  overflow-x: auto;
}

.comments-table {
  width: 100%;
  border-collapse: collapse;
  background: var(--color-surface);
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 0 15px rgba(0, 255, 157, 0.1);
}

.comments-table th,
.comments-table td {
  padding: 12px;
  text-align: left;
  border-bottom: 1px solid var(--color-border);
}

.comments-table th {
  background: rgba(0, 255, 157, 0.1);
  color: var(--color-primary);
  font-weight: bold;
  font-size: 0.9rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.comments-table tr:last-child td {
  border-bottom: none;
}

.comments-table tr:hover {
  background: rgba(0, 255, 157, 0.05);
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

.status-badge {
  display: inline-block;
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 0.8rem;
  font-weight: bold;
  text-transform: capitalize;
}

.status-approved {
  background: rgba(67, 233, 123, 0.2);
  color: #43e97b;
}

.status-pending {
  background: rgba(255, 204, 0, 0.2);
  color: #ffcc00;
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

.btn-delete {
  background: rgba(255, 107, 107, 0.1);
  color: #ff6b6b;
}

.btn-delete:hover {
  background: #ff6b6b;
  color: #fff;
  box-shadow: 0 2px 8px rgba(255, 107, 107, 0.3);
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
