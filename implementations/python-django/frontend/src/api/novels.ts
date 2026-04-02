import apiClient from './client'
import type {
  Novel,
  Episode,
  EpisodeListItem,
  PaginatedResponse,
  NovelFormData,
  EpisodeFormData,
} from '../types'

export interface NovelListParams {
  q?: string
  category?: number
  sort?: string
  limit?: number
  offset?: number
}

export const novelsApi = {
  async getList(params?: NovelListParams): Promise<PaginatedResponse<Novel>> {
    const response = await apiClient.get('/novels/', { params })
    return response.data
  },

  async getDetail(id: number): Promise<Novel> {
    const response = await apiClient.get(`/novels/${id}/`)
    return response.data
  },

  async create(data: NovelFormData): Promise<Novel> {
    const response = await apiClient.post('/novels/', data)
    return response.data
  },

  async update(id: number, data: Partial<NovelFormData>): Promise<Novel> {
    const response = await apiClient.patch(`/novels/${id}/`, data)
    return response.data
  },

  async delete(id: number): Promise<void> {
    await apiClient.delete(`/novels/${id}/`)
  },

  async getEpisodes(novelId: number): Promise<EpisodeListItem[]> {
    const response = await apiClient.get(`/novels/${novelId}/episodes/`)
    return response.data
  },

  async createEpisode(data: EpisodeFormData): Promise<Episode> {
    const response = await apiClient.post('/episodes/', data)
    return response.data
  },

  async getEpisode(episodeId: number): Promise<Episode> {
    const response = await apiClient.get(`/episodes/${episodeId}/`)
    return response.data
  },

  async updateEpisode(episodeId: number, data: Partial<Omit<EpisodeFormData, 'novel'>>): Promise<Episode> {
    const response = await apiClient.patch(`/episodes/${episodeId}/`, data)
    return response.data
  },

  async deleteEpisode(episodeId: number): Promise<void> {
    await apiClient.delete(`/episodes/${episodeId}/`)
  },
}
