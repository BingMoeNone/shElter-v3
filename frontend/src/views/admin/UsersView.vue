<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { adminApi } from '@/services/api'

const users = ref([])
const loading = ref(true)
const searchQuery = ref('')
const currentPage = ref(1)
const limit = ref(20)
const totalItems = ref(0)
const totalPages = ref(0)

const fetchUsers = async () => {
  loading.value = true
  try {
    const response = await adminApi.getUsers({
      page: currentPage.value,
      limit: limit.value,
      search: searchQuery.value
    })
    users.value = response.data.users
    totalItems.value = response.data.pagination.total_items
    totalPages.value = response.data.pagination.total_pages
  } catch (error) {
    console.error('Failed to fetch users:', error)
  } finally {
    loading.value = false
  }
}

const handleSearch = () => {
  currentPage.value = 1
  fetchUsers()
}

const handlePageChange = (page: number) => {
  currentPage.value = page
  fetchUsers()
}

const handleDeleteUser = async (userId: string) => {
  if (confirm('纭畾瑕佸垹闄よ繖涓敤鎴峰悧锛?')) {
    try {
      await adminApi.deleteUser(userId)
      fetchUsers()
    } catch (error) {
      console.error('Failed to delete user:', error)
    }
  }
}

onMounted(() => {
  fetchUsers()
})
</script>

<template>
  <div class="admin-users">
    <h1 class="page-title">鐢ㄦ埛绠＄悊</h1>
    
    <div class="users-header">
      <div class="search-bar">
        <input
          type="text"
          v-model="searchQuery"
          placeholder="鎼滅储鐢ㄦ埛鍚嶃€侀偖绠辨垨鏄剧ず鍚?.."
          @input="handleSearch"
        />
      </div>
    </div>
    
    <div v-if="loading" class="loading">鍔犺浇涓?..</div>
    
    <div v-else class="users-table-container">
      <table class="users-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>鐢ㄦ埛鍚?/th>
            <th>閭</th>
            <th>鏄剧ず鍚?/th>
            <th>瑙掕壊</th>
            <th>鐘舵€?/th>
            <th>娉ㄥ唽鏃堕棿</th>
            <th>鎿嶄綔</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="user in users" :key="user.id">
            <td>{{ user.id }}</td>
            <td>{{ user.username }}</td>
            <td>{{ user.email }}</td>
            <td>{{ user.display_name || '-' }}</td>
            <td>
              <span :class="`role-badge role-${user.role}`">
                {{ user.role }}
              </span>
            </td>
            <td>
              <span :class="`status-badge status-${user.is_active ? 'active' : 'inactive'}`">
                {{ user.is_active ? '娲昏穬' : '绂佺敤' }}
              </span>
            </td>
            <td>{{ new Date(user.created_at).toLocaleString() }}</td>
            <td>
              <div class="action-buttons">
                <button class="btn btn-view">鏌ョ湅</button>
                <button class="btn btn-edit">缂栬緫</button>
                <button class="btn btn-delete" @click="handleDeleteUser(user.id)">鍒犻櫎</button>
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
.admin-users {
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

.users-header {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 20px;
}

.search-bar {
  width: 300px;
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

.loading {
  text-align: center;
  font-size: 1.2rem;
  color: var(--color-text-muted);
  padding: 40px;
}

.users-table-container {
  overflow-x: auto;
}

.users-table {
  width: 100%;
  border-collapse: collapse;
  background: var(--color-surface);
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 0 15px rgba(0, 255, 157, 0.1);
}

.users-table th,
.users-table td {
  padding: 12px;
  text-align: left;
  border-bottom: 1px solid var(--color-border);
}

.users-table th {
  background: rgba(0, 255, 157, 0.1);
  color: var(--color-primary);
  font-weight: bold;
  font-size: 0.9rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.users-table tr:last-child td {
  border-bottom: none;
}

.users-table tr:hover {
  background: rgba(0, 255, 157, 0.05);
}

.role-badge {
  display: inline-block;
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 0.8rem;
  font-weight: bold;
  text-transform: capitalize;
}

.role-user {
  background: rgba(79, 172, 254, 0.2);
  color: #4facfe;
}

.role-moderator {
  background: rgba(67, 233, 123, 0.2);
  color: #43e97b;
}

.role-admin {
  background: rgba(255, 107, 107, 0.2);
  color: #ff6b6b;
}

.status-badge {
  display: inline-block;
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 0.8rem;
  font-weight: bold;
}

.status-active {
  background: rgba(67, 233, 123, 0.2);
  color: #43e97b;
}

.status-inactive {
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
