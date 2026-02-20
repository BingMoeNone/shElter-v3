import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { Article, Pagination } from '@/types'
import { articlesApi } from '@/services/api'
import { useToastStore } from './toast'

export const useArticlesStore = defineStore('articles', () => {
  const articles = ref<Article[]>([])
  const currentArticle = ref<Article | null>(null)
  const pagination = ref<Pagination | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)

  async function fetchArticles(params?: { page?: number; limit?: number; status?: string; category?: string; tag?: string; search?: string }): Promise<void> {
    loading.value = true
    error.value = null

    try {
      const response = await articlesApi.list(params)
      articles.value = response.data.articles || response.data || []
      pagination.value = response.data.pagination
    } catch (err: any) {
      error.value = 'Failed to fetch articles'
      console.error(err)
      useToastStore().error(err.response?.data?.message || '鑾峰彇鏂囩珷鍒楄〃澶辫触')
    } finally {
      loading.value = false
    }
  }

  async function fetchArticle(articleId: string): Promise<void> {
    loading.value = true
    error.value = null

    try {
      const response = await articlesApi.get(articleId)
      currentArticle.value = response.data
    } catch (err: any) {
      error.value = 'Failed to fetch article'
      console.error(err)
      useToastStore().error(err.response?.data?.message || '鑾峰彇鏂囩珷澶辫触')
    } finally {
      loading.value = false
    }
  }

  async function createArticle(data: { title: string; content: string; summary?: string; status?: string; categoryIds?: string[]; tagNames?: string[] }): Promise<Article> {
    loading.value = true
    error.value = null

    try {
      const response = await articlesApi.create(data)
      const article = response.data
      articles.value.unshift(article)
      useToastStore().success('鏂囩珷鍒涘缓鎴愬姛锛?)
      return article
    } catch (err: any) {
      error.value = 'Failed to create article'
      useToastStore().error(err.response?.data?.message || '鍒涘缓鏂囩珷澶辫触')
      throw err
    } finally {
      loading.value = false
    }
  }

  async function updateArticle(articleId: string, data: { title?: string; content?: string; summary?: string; status?: string; categoryIds?: string[]; tagNames?: string[] }): Promise<Article> {
    loading.value = true
    error.value = null

    try {
      const response = await articlesApi.update(articleId, data)
      const article = response.data

      const index = articles.value.findIndex(a => a.id === articleId)
      if (index !== -1) {
        articles.value[index] = article
      }

      if (currentArticle.value?.id === articleId) {
        currentArticle.value = article
      }

      useToastStore().success('鏂囩珷鏇存柊鎴愬姛锛?)
      return article
    } catch (err: any) {
      error.value = 'Failed to update article'
      useToastStore().error(err.response?.data?.message || '鏇存柊鏂囩珷澶辫触')
      throw err
    } finally {
      loading.value = false
    }
  }

  async function publishArticle(articleId: string): Promise<Article> {
    loading.value = true
    error.value = null

    try {
      const response = await articlesApi.publish(articleId)
      const article = response.data

      const index = articles.value.findIndex(a => a.id === articleId)
      if (index !== -1) {
        articles.value[index] = article
      }

      if (currentArticle.value?.id === articleId) {
        currentArticle.value = article
      }

      useToastStore().success('鏂囩珷鍙戝竷鎴愬姛锛?)
      return article
    } catch (err: any) {
      error.value = 'Failed to publish article'
      useToastStore().error(err.response?.data?.message || '鍙戝竷鏂囩珷澶辫触')
      throw err
    } finally {
      loading.value = false
    }
  }

  async function deleteArticle(articleId: string): Promise<void> {
    loading.value = true
    error.value = null

    try {
      await articlesApi.delete(articleId)
      articles.value = articles.value.filter(a => a.id !== articleId)

      if (currentArticle.value?.id === articleId) {
        currentArticle.value = null
      }

      useToastStore().success('鏂囩珷鍒犻櫎鎴愬姛锛?)
    } catch (err: any) {
      error.value = 'Failed to delete article'
      useToastStore().error(err.response?.data?.message || '鍒犻櫎鏂囩珷澶辫触')
      throw err
    } finally {
      loading.value = false
    }
  }

  function clearCurrentArticle(): void {
    currentArticle.value = null
  }

  return {
    articles,
    currentArticle,
    pagination,
    loading,
    error,
    fetchArticles,
    fetchArticle,
    createArticle,
    updateArticle,
    publishArticle,
    deleteArticle,
    clearCurrentArticle,
  }
})
