<script setup lang="ts">
import { RouterLink } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { ref } from 'vue'

const authStore = useAuthStore()
const searchQuery = ref('')
const showMobileMenu = ref(false)

const emit = defineEmits<{
  search: [query: string]
}>()

function handleSearch() {
  if (searchQuery.value.trim()) {
    emit('search', searchQuery.value)
  }
}

async function handleLogout() {
  await authStore.logout()
}
</script>

<template>
  <header class="header">
    <div class="header-content">
      <RouterLink to="/" class="logo">
        <h1>Wiki Platform</h1>
      </RouterLink>
      
      <nav class="nav" :class="{ 'nav-open': showMobileMenu }">
        <RouterLink to="/" class="nav-link">Home</RouterLink>
        <RouterLink to="/articles" class="nav-link">Articles</RouterLink>
        <RouterLink to="/categories" class="nav-link">Categories</RouterLink>
        
        <form class="search-form" @submit.prevent="handleSearch">
          <input
            v-model="searchQuery"
            type="search"
            placeholder="Search articles..."
            class="search-input"
          />
          <button type="submit" class="search-btn">Search</button>
        </form>
        
        <div class="auth-section">
          <template v-if="authStore.isAuthenticated">
            <RouterLink to="/articles/create" class="nav-link">Create Article</RouterLink>
            <RouterLink to="/profile" class="nav-link">Profile</RouterLink>
            <button @click="handleLogout" class="logout-btn">Logout</button>
          </template>
          <template v-else>
            <RouterLink to="/login" class="nav-link">Login</RouterLink>
            <RouterLink to="/register" class="nav-link register-link">Register</RouterLink>
          </template>
        </div>
      </nav>
      
      <button class="mobile-menu-btn" @click="showMobileMenu = !showMobileMenu">
        <span></span>
        <span></span>
        <span></span>
      </button>
    </div>
  </header>
</template>

<style scoped>
.header {
  background: white;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  position: sticky;
  top: 0;
  z-index: 100;
}

.header-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 60px;
}

.logo {
  text-decoration: none;
}

.logo h1 {
  font-size: 1.5rem;
  color: #42b883;
  margin: 0;
}

.nav {
  display: flex;
  align-items: center;
  gap: 20px;
}

.nav-link {
  color: #333;
  text-decoration: none;
  font-weight: 500;
  transition: color 0.2s;
}

.nav-link:hover {
  color: #42b883;
}

.search-form {
  display: flex;
  gap: 8px;
}

.search-input {
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  width: 200px;
}

.search-btn {
  padding: 8px 16px;
  background: #42b883;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.auth-section {
  display: flex;
  align-items: center;
  gap: 12px;
}

.register-link {
  background: #42b883;
  color: white !important;
  padding: 8px 16px;
  border-radius: 4px;
}

.logout-btn {
  background: transparent;
  color: #666;
  border: 1px solid #ddd;
  padding: 8px 16px;
}

.mobile-menu-btn {
  display: none;
  flex-direction: column;
  gap: 4px;
  background: transparent;
  border: none;
  padding: 8px;
}

.mobile-menu-btn span {
  width: 24px;
  height: 2px;
  background: #333;
}

@media (max-width: 768px) {
  .nav {
    display: none;
    position: absolute;
    top: 60px;
    left: 0;
    right: 0;
    background: white;
    flex-direction: column;
    padding: 20px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  }

  .nav-open {
    display: flex;
  }

  .search-form {
    width: 100%;
  }

  .search-input {
    flex: 1;
  }

  .mobile-menu-btn {
    display: flex;
  }
}
</style>
