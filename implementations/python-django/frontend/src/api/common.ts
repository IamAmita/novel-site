import apiClient from './client'
import type { Category, Tag, PaginatedResponse } from '../types'

export const commonApi = {
  async getCategories(): Promise<PaginatedResponse<Category>> {
    const response = await apiClient.get('/categories/', { params: { limit: 100 } })
    return response.data
  },

  async getTags(): Promise<PaginatedResponse<Tag>> {
    const response = await apiClient.get('/tags/', { params: { limit: 100 } })
    return response.data
  },
}
