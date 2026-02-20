export interface User {
  id: string
  username: string
  email: string
  displayName: string | null
  bio: string | null
  avatarUrl: string | null
  isActive: boolean
  role: 'user' | 'moderator' | 'admin'
  createdAt: string
  updatedAt: string
  contributionCount: number
}

export interface UserProfile {
  id: string
  username: string
  displayName: string | null
  bio: string | null
  avatarUrl: string | null
  createdAt: string
  contributionCount: number
  isFollowing: boolean
}

export interface Article {
  id: string
  title: string
  slug: string
  content: string
  summary: string | null
  status: 'draft' | 'published' | 'archived'
  author: User
  publishedAt: string | null
  createdAt: string
  updatedAt: string
  viewCount: number
  isFeatured: boolean
  categories: Category[]
  tags: Tag[]
}

export interface Category {
  id: string
  name: string
  slug: string
  description: string | null
  parentId: string | null
  articleCount: number
}

export interface Tag {
  id: string
  name: string
  slug: string
  usageCount: number
}

export interface Comment {
  id: string
  content: string
  author: User
  articleId: string
  parentId: string | null
  createdAt: string
  updatedAt: string
  isApproved: boolean
}

export interface Connection {
  id: string
  follower: User
  followed: User
  status: 'pending' | 'accepted' | 'blocked'
  connectionType: 'friend' | 'follow'
  createdAt: string
  acceptedAt: string | null
}

export interface Pagination {
  page: number
  limit: number
  totalPages: number
  totalItems: number
}

export interface LoginResponse {
  accessToken: string
  refreshToken: string
  tokenType: string
  user: User
}

export interface ApiError {
  code: string
  message: string
  details: Record<string, unknown>
}
