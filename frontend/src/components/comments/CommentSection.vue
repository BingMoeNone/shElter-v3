<script setup lang="ts">
import type { Comment } from '@/types'
import { ref, computed } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { commentsApi } from '@/services/api'
import { useToastStore } from '@/stores/toast'

const props = defineProps<{
  comments: Comment[]
  articleId: string
}>()

const emit = defineEmits<{
  commentAdded: [comment: Comment]
  commentDeleted: [commentId: string]
}>()

const authStore = useAuthStore()
const toast = useToastStore()

const newComment = ref('')
const replyingTo = ref<string | null>(null)
const replyContent = ref('')
const submitting = ref(false)
const deletingId = ref<string | null>(null)

const sortedComments = computed(() => {
  return [...props.comments].sort((a, b) => 
    new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime()
  )
})

function formatDate(date: string) {
  return new Date(date).toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

async function submitComment() {
  if (!newComment.value.trim() || submitting.value) return
  
  submitting.value = true
  
  try {
    const response = await commentsApi.create({
      articleId: props.articleId,
      content: newComment.value,
    })
    emit('commentAdded', response.data)
    newComment.value = ''
    toast.success('评论发表成功！')
  } catch (err: any) {
    console.error('Failed to post comment:', err)
    toast.error(err.response?.data?.message || '评论发表失败，请重试')
  } finally {
    submitting.value = false
  }
}

async function submitReply(commentId: string) {
  if (!replyContent.value.trim() || submitting.value) return
  
  submitting.value = true
  
  try {
    const response = await commentsApi.create({
      articleId: props.articleId,
      content: replyContent.value,
      parentId: commentId,
    })
    emit('commentAdded', response.data)
    replyContent.value = ''
    replyingTo.value = null
    toast.success('回复发表成功！')
  } catch (err: any) {
    console.error('Failed to post reply:', err)
    toast.error(err.response?.data?.message || '回复发表失败，请重试')
  } finally {
    submitting.value = false
  }
}

async function deleteComment(commentId: string) {
  if (!confirm('确定要删除这条评论吗？')) return
  
  deletingId.value = commentId
  
  try {
    await commentsApi.delete(commentId)
    emit('commentDeleted', commentId)
    toast.success('评论已删除')
  } catch (err: any) {
    console.error('Failed to delete comment:', err)
    toast.error(err.response?.data?.message || '删除评论失败')
  } finally {
    deletingId.value = null
  }
}

function canDelete(comment: Comment): boolean {
  if (!authStore.user) return false
  return authStore.user.id === comment.author.id || 
         authStore.isAdmin || 
         authStore.isModerator
}
</script>

<template>
  <div class="comment-section">
    <h3>Comments ({{ comments.length }})</h3>
    
    <div v-if="authStore.isAuthenticated" class="comment-form">
      <textarea
        v-model="newComment"
        placeholder="Write a comment..."
        rows="3"
      ></textarea>
      <button
        @click="submitComment"
        :disabled="!newComment.trim() || submitting"
      >
        {{ submitting ? 'Posting...' : 'Post Comment' }}
      </button>
    </div>
    
    <div v-else class="login-prompt">
      <RouterLink to="/login">Login</RouterLink> to leave a comment.
    </div>
    
    <div class="comments-list">
      <div v-for="comment in sortedComments" :key="comment.id" class="comment">
        <div class="comment-header">
          <RouterLink :to="`/users/${comment.author.id}`" class="author">
            {{ comment.author.displayName || comment.author.username }}
          </RouterLink>
          <span class="date">{{ formatDate(comment.createdAt) }}</span>
        </div>
        
        <p class="comment-content">{{ comment.content }}</p>
        
        <div class="comment-actions">
          <button
            v-if="authStore.isAuthenticated"
            @click="replyingTo = replyingTo === comment.id ? null : comment.id"
            class="btn-reply"
          >
            Reply
          </button>
          <button
            v-if="canDelete(comment)"
            @click="deleteComment(comment.id)"
            class="btn-delete"
            :disabled="deletingId === comment.id"
          >
            {{ deletingId === comment.id ? '删除中...' : 'Delete' }}
          </button>
        </div>
        
        <div v-if="replyingTo === comment.id" class="reply-form">
          <textarea
            v-model="replyContent"
            placeholder="Write a reply..."
            rows="2"
          ></textarea>
          <div class="reply-actions">
            <button @click="submitReply(comment.id)" :disabled="!replyContent.trim() || submitting">
              Reply
            </button>
            <button @click="replyingTo = null" class="btn-cancel">Cancel</button>
          </div>
        </div>
      </div>
    </div>
    
    <div v-if="comments.length === 0" class="no-comments">
      No comments yet. Be the first to comment!
    </div>
  </div>
</template>

<style scoped>
.comment-section {
  margin-top: 40px;
}

.comment-section h3 {
  margin-bottom: 20px;
  color: var(--color-primary);
  text-shadow: 0 0 5px var(--color-primary);
}

.comment-form {
  margin-bottom: 24px;
}

.comment-form textarea {
  width: 100%;
  padding: 12px;
  background: rgba(0, 0, 0, 0.5);
  border: 1px solid var(--color-border);
  border-radius: 4px;
  margin-bottom: 12px;
  font-family: inherit;
  color: var(--color-text);
  transition: all 0.3s;
}

.comment-form textarea:focus {
  border-color: var(--color-primary);
  box-shadow: 0 0 10px rgba(0, 255, 157, 0.2);
}

.comment-form button {
  padding: 8px 16px;
  background: rgba(0, 255, 157, 0.1);
  border: 1px solid var(--color-primary);
  color: var(--color-primary);
  cursor: pointer;
  transition: all 0.3s;
  border-radius: 4px;
}

.comment-form button:hover:not(:disabled) {
  background: var(--color-primary);
  color: #000;
  box-shadow: 0 0 15px var(--color-primary);
}

.login-prompt {
  padding: 16px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid var(--color-border);
  border-radius: 4px;
  margin-bottom: 24px;
  color: var(--color-text-muted);
}

.login-prompt a {
  color: var(--color-primary);
  font-weight: bold;
}

.comments-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.comment {
  padding: 16px;
  background: var(--color-surface);
  border-radius: 8px;
  border-left: 3px solid var(--color-primary);
  border: 1px solid var(--color-border);
  border-left-width: 3px;
}

.comment-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.author {
  font-weight: 600;
  color: var(--color-accent);
  text-decoration: none;
}

.author:hover {
  text-shadow: 0 0 5px var(--color-accent);
}

.date {
  color: var(--color-text-muted);
  font-size: 0.85rem;
}

.comment-content {
  margin: 0;
  line-height: 1.6;
  color: var(--color-text);
}

.comment-actions {
  margin-top: 8px;
  display: flex;
  gap: 8px;
}

.btn-reply,
.btn-delete,
.btn-cancel {
  background: transparent;
  color: var(--color-text-muted);
  padding: 4px 12px;
  font-size: 0.85rem;
  border: 1px solid transparent;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-reply:hover {
  color: var(--color-primary);
  border-color: var(--color-primary);
}

.btn-delete {
  color: #ff4444;
}

.btn-delete:hover {
  border-color: #ff4444;
  background: rgba(255, 68, 68, 0.1);
}

.btn-cancel:hover {
  color: var(--color-text);
  border-color: var(--color-text);
}

.reply-form {
  margin-top: 12px;
  padding-top: 12px;
  border-top: 1px solid var(--color-border);
}

.reply-form textarea {
  width: 100%;
  padding: 8px;
  background: rgba(0, 0, 0, 0.5);
  border: 1px solid var(--color-border);
  border-radius: 4px;
  margin-bottom: 8px;
  color: var(--color-text);
}

.reply-form textarea:focus {
  border-color: var(--color-primary);
}

.reply-actions {
  display: flex;
  gap: 8px;
}

.reply-actions button {
  padding: 6px 12px;
  background: rgba(0, 255, 157, 0.1);
  border: 1px solid var(--color-primary);
  color: var(--color-primary);
  cursor: pointer;
  border-radius: 4px;
}

.reply-actions button:hover:not(:disabled) {
  background: var(--color-primary);
  color: #000;
}

.no-comments {
  text-align: center;
  color: var(--color-text-muted);
  padding: 40px;
  border: 1px dashed var(--color-text-muted);
  border-radius: 8px;
}
</style>
