import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('@/views/HomeView.vue'),
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('@/views/LoginView.vue'),
      meta: { guest: true },
    },
    {
      path: '/register',
      name: 'register',
      component: () => import('@/views/RegisterView.vue'),
      meta: { guest: true },
    },
    {
      path: '/articles',
      name: 'articles',
      component: () => import('@/views/ArticlesView.vue'),
    },
    {
      path: '/articles/create',
      name: 'article-create',
      component: () => import('@/views/CreateArticleView.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/articles/:id/edit',
      name: 'article-edit',
      component: () => import('@/views/EditArticleView.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/articles/:id',
      name: 'article-detail',
      component: () => import('@/views/ArticleDetailView.vue'),
    },
    {
      path: '/users/:id',
      name: 'user-profile',
      component: () => import('@/views/UserProfileView.vue'),
    },
    {
      path: '/search',
      name: 'search',
      component: () => import('@/views/SearchView.vue'),
    },
    {
      path: '/categories',
      name: 'categories',
      component: () => import('@/views/CategoriesView.vue'),
    },
    {
      path: '/categories/:slug',
      name: 'category-articles',
      component: () => import('@/views/CategoryArticlesView.vue'),
    },
    {
      path: '/tags/:slug',
      name: 'tag-articles',
      component: () => import('@/views/TagArticlesView.vue'),
    },
    {
      path: '/profile',
      name: 'profile',
      component: () => import('@/views/ProfileView.vue'),
      meta: { requiresAuth: true },
    },
  ],
})

router.beforeEach((to, _from, next) => {
  const authStore = useAuthStore()
  
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next({ name: 'login', query: { redirect: to.fullPath } })
  } else if (to.meta.guest && authStore.isAuthenticated) {
    next({ name: 'home' })
  } else {
    next()
  }
})

export default router
