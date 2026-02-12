import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { Article, Pagination } from '@/types'
import { articlesApi } from '@/services/api'

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
      articles.value = response.data.articles
      pagination.value = response.data.pagination
    } catch (err) {
      error.value = 'Failed to fetch articles'
      console.error(err)
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
    } catch (err) {
      error.value = 'Failed to fetch article'
      console.error(err)
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
      return article
    } catch (err) {
      error.value = 'Failed to create article'
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
      
      return article
    } catch (err) {
      error.value = 'Failed to update article'
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
      
      return article
    } catch (err) {
      error.value = 'Failed to publish article'
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
    } catch (err) {
      error.value = 'Failed to delete article'
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
