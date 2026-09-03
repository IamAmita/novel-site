export interface User {
  id: number
  user_id: string
  email: string
  username: string
  icon: string | null
  bio: string
}

export interface PenName {
  id: number
  display_name: string
  icon: string | null
  bio: string
  world_count: number
}

export interface World {
  id: number
  name: string
  description: string
  cover_image: string | null
  owner_pen_name: number
  owner_pen_name_display: string
  is_deleted: boolean
  updated_at: string
}
