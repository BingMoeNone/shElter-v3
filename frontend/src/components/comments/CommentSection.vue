<script setup lang="ts">
import type { Comment, User } from '@/types'
import { ref, computed } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { commentsApi } from '@/services/api'

const props = defineProps<{
  comments: Comment[]
  articleId: string
}>()

const emit = defineEmits<{
  commentAdded: [comment: Comment]
  commentDeleted: [commentId: string]
}>()

const authStore = useAuthStore()

const newComment = ref('')
const replyingTo = ref<string | null>(null)
const replyContent = ref('')
const submitting = ref(false)

const sortedComments = computed(() => {
  return [...props.comments].sort((a, b) => 
    new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime()
  )
})

function formatDate(date: string) {
  return new Date(date).toLocaleDateString('en-US', {
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
  } catch (error) {
    console.error('Failed to post comment:', error)
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
  } catch (error) {
    console.error('Failed to post reply:', error)
  } finally {
    submitting.value = false
  }
}

async function deleteComment(commentId: string) {
  if (!confirm('Are you sure you want to delete this comment?')) return
  
  try {
    await commentsApi.delete(commentId)
    emit('commentDeleted', commentId)
  } catch (error) {
    console.error('Failed to delete comment:', error)
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
          >
            Delete
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
}

.comment-form {
  margin-bottom: 24px;
}

.comment-form textarea {
  width: 100%;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  margin-bottom: 12px;
  font-family: inherit;
}

.login-prompt {
  padding: 16px;
  background: #f5f5f5;
  border-radius: 4px;
  margin-bottom: 24px;
}

.comments-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.comment {
  padding: 16px;
  background: #f9f9f9;
  border-radius: 8px;
  border-left: 3px solid #42b883;
}

.comment-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.author {
  font-weight: 600;
  color: #42b883;
  text-decoration: none;
}

.date {
  color: #888;
  font-size: 0.85rem;
}

.comment-content {
  margin: 0;
  line-height: 1.6;
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
  color: #666;
  padding: 4px 12px;
  font-size: 0.85rem;
}

.btn-delete {
  color: #e74c3c;
}

.reply-form {
  margin-top: 12px;
  padding-top: 12px;
  border-top: 1px solid #eee;
}

.reply-form textarea {
  width: 100%;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
  margin-bottom: 8px;
}

.reply-actions {
  display: flex;
  gap: 8px;
}

.no-comments {
  text-align: center;
  color: #888;
  padding: 40px;
}
</style>
