<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { adminApi } from '@/services/api'

const router = useRouter()
const articles = ref([])
const loading = ref(true)
const searchQuery = ref('')
const currentPage = ref(1)
const limit = ref(20)
const totalItems = ref(0)
const totalPages = ref(0)
const statusFilter = ref('')

const fetchArticles = async () => {
  loading.value = true
  try {
    const response = await adminApi.getArticles({
      page: currentPage.value,
      limit: limit.value,
      search: searchQuery.value,
      status: statusFilter.value || undefined
    })
    articles.value = response.data.articles
    totalItems.value = response.data.pagination.total_items
    totalPages.value = response.data.pagination.total_pages
  } catch (error) {
    console.error('Failed to fetch articles:', error)
  } finally {
    loading.value = false
  }
}

const handleSearch = () => {
  currentPage.value = 1
  fetchArticles()
}

const handleStatusFilterChange = () => {
  currentPage.value = 1
  fetchArticles()
}

const handlePageChange = (page: number) => {
  currentPage.value = page
  fetchArticles()
}

const handleViewArticle = (articleId: string) => {
  router.push(`/articles/${articleId}`)
}

const handleEditArticle = (articleId: string) => {
  router.push(`/articles/${articleId}/edit`)
}

onMounted(() => {
  fetchArticles()
})
</script>

<template>
  <div class="admin-articles">
    <h1 class="page-title">鏂囩珷绠＄悊</h1>
    
    <div class="articles-header">
      <div class="search-bar">
        <input
          type="text"
          v-model="searchQuery"
          placeholder="鎼滅储鏂囩珷鏍囬鎴栧唴瀹?.."
          @input="handleSearch"
        />
      </div>
      <div class="filter-bar">
        <select v-model="statusFilter" @change="handleStatusFilterChange">
          <option value="">鎵€鏈夌姸鎬?/option>
          <option value="draft">鑽夌</option>
          <option value="published">宸插彂甯?/option>
          <option value="archived">宸插綊妗?/option>
        </select>
      </div>
    </div>
    
    <div v-if="loading" class="loading">鍔犺浇涓?..</div>
    
    <div v-else class="articles-table-container">
      <table class="articles-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>鏍囬</th>
            <th>浣滆€?/th>
            <th>鐘舵€?/th>
            <th>鍙戝竷鏃堕棿</th>
            <th>鏌ョ湅娆℃暟</th>
            <th>鎿嶄綔</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="article in articles" :key="article.id">
            <td>{{ article.id }}</td>
            <td class="article-title">
              {{ article.title }}
            </td>
            <td>{{ article.author.username }}</td>
            <td>
              <span :class="`status-badge status-${article.status}`">
                {{ article.status }}
              </span>
            </td>
            <td>{{ article.published_at ? new Date(article.published_at).toLocaleString() : '-' }}</td>
            <td>{{ article.view_count }}</td>
            <td>
              <div class="action-buttons">
                <button class="btn btn-view" @click="handleViewArticle(article.id)">鏌ョ湅</button>
                <button class="btn btn-edit" @click="handleEditArticle(article.id)">缂栬緫</button>
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
.admin-articles {
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

.articles-header {
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
  min-width: 150px;
}

.filter-bar select {
  width: 100%;
  padding: 10px;
  background: rgba(0, 0, 0, 0.5);
  border: 1px solid var(--color-border);
  border-radius: 4px;
  color: var(--color-text);
  font-size: 1rem;
}

.filter-bar select:focus {
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

.articles-table-container {
  overflow-x: auto;
}

.articles-table {
  width: 100%;
  border-collapse: collapse;
  background: var(--color-surface);
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 0 15px rgba(0, 255, 157, 0.1);
}

.articles-table th,
.articles-table td {
  padding: 12px;
  text-align: left;
  border-bottom: 1px solid var(--color-border);
}

.articles-table th {
  background: rgba(0, 255, 157, 0.1);
  color: var(--color-primary);
  font-weight: bold;
  font-size: 0.9rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.articles-table tr:last-child td {
  border-bottom: none;
}

.articles-table tr:hover {
  background: rgba(0, 255, 157, 0.05);
}

.article-title {
  max-width: 300px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.status-badge {
  display: inline-block;
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 0.8rem;
  font-weight: bold;
  text-transform: capitalize;
}

.status-draft {
  background: rgba(255, 204, 0, 0.2);
  color: #ffcc00;
}

.status-published {
  background: rgba(67, 233, 123, 0.2);
  color: #43e97b;
}

.status-archived {
  background: rgba(255, 107, 107, 0.2);
  color: #ff6b6b;
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

.btn-edit {
  background: rgba(0, 242, 254, 0.1);
  color: #00f2fe;
}

.btn-delete {
  background: rgba(255, 107, 107, 0.1);
  color: #ff6b6b;
}

.btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 2px 8px rgba(0, 255, 157, 0.2);
}

.btn-view:hover {
  background: #4facfe;
  color: #fff;
}

.btn-edit:hover {
  background: #00f2fe;
  color: #000;
}

.btn-delete:hover {
  background: #ff6b6b;
  color: #fff;
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
