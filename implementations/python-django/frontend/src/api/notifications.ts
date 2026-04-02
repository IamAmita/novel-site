import apiClient from './client'
import type { Notification, PaginatedResponse } from '../types'

export const notificationsApi = {
  async getList(): Promise<PaginatedResponse<Notification>> {
    const response = await apiClient.get('/notifications/')
    return response.data
  },

  async markAsRead(id: number): Promise<void> {
    await apiClient.put(`/notifications/${id}/read/`)
  },
}
