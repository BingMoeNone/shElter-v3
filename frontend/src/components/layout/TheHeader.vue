<script setup lang="ts">
import { RouterLink, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { ref, computed } from 'vue'

const authStore = useAuthStore()
const router = useRouter()
const searchQuery = ref('')
const showMobileMenu = ref(false)

const displayName = computed(() => {
  if (authStore.user) {
    return authStore.user.displayName || authStore.user.username
  }
  return '涓汉璧勬枡'
})

function handleSearch() {
  if (searchQuery.value.trim()) {
    router.push({ path: '/search', query: { q: searchQuery.value.trim() } })
    searchQuery.value = ''
    showMobileMenu.value = false
  }
}

async function handleLogout() {
  await authStore.logout()
  showMobileMenu.value = false
  router.push('/')
}

function closeMobileMenu() {
  showMobileMenu.value = false
}
</script>

<template>
  <header class="header">
    <div class="header-content">
      <RouterLink to="/" class="logo" @click="closeMobileMenu">
        <h1>Wiki Platform</h1>
      </RouterLink>
      
      <nav class="nav" :class="{ 'nav-open': showMobileMenu }">
        <RouterLink to="/" class="nav-link" @click="closeMobileMenu">棣栭〉</RouterLink>
        <RouterLink to="/articles" class="nav-link" @click="closeMobileMenu">鏂囩珷</RouterLink>
        <RouterLink to="/categories" class="nav-link" @click="closeMobileMenu">鍒嗙被</RouterLink>
        <RouterLink to="/metro" class="nav-link special-link" @click="closeMobileMenu">鍦伴搧</RouterLink>
        <RouterLink to="/music" class="nav-link special-link" @click="closeMobileMenu">闊充箰</RouterLink>
        
        <form class="search-form" @submit.prevent="handleSearch">
          <input
            v-model="searchQuery"
            type="search"
            placeholder="鎼滅储鏂囩珷..."
            class="search-input"
          />
          <button type="submit" class="search-btn">鎼滅储</button>
        </form>
        
        <div class="auth-section">
          <template v-if="authStore.isAuthenticated">
            <RouterLink to="/articles/create" class="nav-link" @click="closeMobileMenu">鍐欐枃绔?/RouterLink>
            <RouterLink to="/profile" class="nav-link profile-link" @click="closeMobileMenu">
              <span class="user-name">{{ displayName }}</span>
            </RouterLink>
            <button @click="handleLogout" class="logout-btn">閫€鍑?/button>
          </template>
          <template v-else>
            <RouterLink to="/login" class="nav-link" @click="closeMobileMenu">鐧诲綍</RouterLink>
            <RouterLink to="/register" class="nav-link register-link" @click="closeMobileMenu">娉ㄥ唽</RouterLink>
          </template>
        </div>
      </nav>
      
      <button class="mobile-menu-btn" @click="showMobileMenu = !showMobileMenu" :class="{ active: showMobileMenu }">
        <span></span>
        <span></span>
        <span></span>
      </button>
    </div>
  </header>
</template>

<style scoped>
.header {
  background: var(--color-surface);
  border-bottom: 1px solid var(--color-primary);
  box-shadow: 0 0 10px rgba(0, 255, 157, 0.2);
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
  color: var(--color-primary);
  text-shadow: 0 0 5px var(--color-primary);
  margin: 0;
}

.nav {
  display: flex;
  align-items: center;
  gap: 20px;
}

.nav-link {
  color: var(--color-text);
  font-weight: 500;
  transition: all 0.2s;
  padding: 6px 10px;
  border-radius: 4px;
}

.nav-link:hover,
.nav-link.router-link-active {
  color: var(--color-primary);
  text-shadow: 0 0 5px var(--color-primary);
  background: rgba(0, 255, 157, 0.05);
}

.special-link {
  color: var(--color-secondary);
}

.special-link:hover {
  color: var(--color-secondary);
  text-shadow: 0 0 5px var(--color-secondary);
  background: rgba(0, 210, 255, 0.05);
}

.search-form {
  display: flex;
  gap: 8px;
}

.search-input {
  padding: 6px 12px;
  border: 1px solid var(--color-border);
  background: rgba(0, 0, 0, 0.5);
  color: var(--color-text);
  border-radius: 4px;
  font-size: 0.9rem;
  width: 180px;
  transition: all 0.3s;
}

.search-input:focus {
  border-color: var(--color-primary);
  box-shadow: 0 0 10px rgba(0, 255, 157, 0.2);
  width: 220px;
}

.search-btn {
  padding: 6px 12px;
  background: rgba(0, 255, 157, 0.1);
  border: 1px solid var(--color-primary);
  color: var(--color-primary);
  border-radius: 4px;
  font-size: 0.9rem;
  transition: all 0.3s;
}

.search-btn:hover {
  background: var(--color-primary);
  color: #000;
  box-shadow: 0 0 10px var(--color-primary);
}

.auth-section {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-left: 12px;
  padding-left: 12px;
  border-left: 1px solid var(--color-border);
}

.profile-link {
  display: flex;
  align-items: center;
  gap: 8px;
  color: var(--color-accent);
}

.user-name {
  font-weight: bold;
  max-width: 120px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.logout-btn {
  padding: 6px 12px;
  background: transparent;
  border: 1px solid var(--color-text-muted);
  color: var(--color-text-muted);
  border-radius: 4px;
  font-size: 0.9rem;
  transition: all 0.3s;
}

.logout-btn:hover {
  border-color: #ff4444;
  color: #ff4444;
  background: rgba(255, 68, 68, 0.05);
  box-shadow: 0 0 10px rgba(255, 68, 68, 0.2);
}

.register-link {
  color: var(--color-primary);
  border: 1px solid var(--color-primary);
}

.register-link:hover {
  background: rgba(0, 255, 157, 0.1);
  box-shadow: 0 0 10px rgba(0, 255, 157, 0.2);
}

.mobile-menu-btn {
  display: none;
  background: transparent;
  border: none;
  flex-direction: column;
  gap: 5px;
  cursor: pointer;
  padding: 5px;
}

.mobile-menu-btn span {
  display: block;
  width: 25px;
  height: 2px;
  background-color: var(--color-primary);
  transition: all 0.3s;
}

@media (max-width: 768px) {
  .nav {
    position: fixed;
    top: 60px;
    left: 0;
    width: 100%;
    background: var(--color-surface);
    flex-direction: column;
    padding: 20px;
    border-bottom: 1px solid var(--color-primary);
    transform: translateY(-150%);
    transition: transform 0.3s ease;
    z-index: 99;
  }

  .nav.nav-open {
    transform: translateY(0);
    box-shadow: 0 10px 20px rgba(0, 0, 0, 0.5);
  }

  .mobile-menu-btn {
    display: flex;
  }

  .auth-section {
    flex-direction: column;
    border-left: none;
    padding-left: 0;
    margin-left: 0;
    width: 100%;
    border-top: 1px solid var(--color-border);
    padding-top: 16px;
    margin-top: 8px;
  }
  
  .search-input {
    width: 100%;
  }
  
  .search-input:focus {
    width: 100%;
  }
}
</style>
