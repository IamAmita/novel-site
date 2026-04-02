export interface UserProfile {
  display_name: string
  icon_url: string | null
  biography: string | null
  website_url: string | null
  created_at: string
  updated_at: string
}

export interface User {
  id: number
  username: string
  email?: string
  email_verified_at?: string | null
  profile: UserProfile
  created_at: string
  updated_at?: string
}

export interface Category {
  id: number
  name: string
  slug: string
}

export interface Tag {
  id: number
  name: string
}

export interface NovelInfo {
  title: string
  synopsis: string | null
  cover_image_url: string | null
  is_r18: boolean
  created_at: string
  updated_at: string
}

export interface AuthorInfo {
  id: number
  username: string
  profile: UserProfile
}

export interface Novel {
  id: number
  user: number
  author: AuthorInfo
  category: number | null
  category_detail: Category | null
  tags: Tag[]
  info: NovelInfo
  episode_count: number
  deleted_at: string | null
  created_at: string
  updated_at: string
}

export interface EpisodeListItem {
  id: number
  novel: number
  section: number | null
  episode_number: number
  title: string
  sort_order: number
  deleted_at: string | null
  created_at: string
  updated_at: string
}

export interface Episode extends EpisodeListItem {
  body: string
}

export interface Comment {
  id: number
  user: number
  class_id: number
  target_id: number
  parent: number | null
  body: string
  is_deleted: boolean
  created_at: string
  updated_at: string
}

export interface Notification {
  id: number
  class_id: number
  target_id: number | null
  message: string
  created_at: string
  status?: {
    is_read: boolean
    read_at: string | null
  }
}

export interface PaginatedResponse<T> {
  count: number
  next: string | null
  previous: string | null
  results: T[]
}

export interface AuthTokens {
  access: string
  refresh: string
}

export interface LoginRequest {
  email: string
  password: string
}

export interface RegisterRequest {
  username: string
  email: string
  password: string
  password_confirm: string
  display_name: string
}

export interface NovelInfoFormData {
  title: string
  synopsis: string
  is_r18: boolean
  cover_image_url?: string | null
}

export interface NovelFormData {
  category: number | null
  info: NovelInfoFormData
}

export interface EpisodeFormData {
  novel: number
  title: string
  body: string
  episode_number: number
  sort_order?: number
}

export interface ProfileFormData {
  display_name: string
  biography: string
  website_url?: string
}

export type NovelStatusLabel = '下書き' | '連載中' | '完結' | '休止中'
