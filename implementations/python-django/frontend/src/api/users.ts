import apiClient from './client'
import type { User, Novel, PaginatedResponse } from '../types'

export const usersApi = {
  async getUser(id: number): Promise<User> {
    const response = await apiClient.get(`/users/${id}/`)
    return response.data
  },

  async getMe(): Promise<User> {
    const response = await apiClient.get('/users/me/')
    return response.data
  },

  async updateProfile(profileId: number, data: { display_name?: string; biography?: string; website_url?: string }): Promise<User> {
    await apiClient.patch(`/profiles/${profileId}/`, data)
    const userRes = await apiClient.get('/users/me/')
    return userRes.data
  },

  async getUserNovels(userId: number): Promise<PaginatedResponse<Novel>> {
    const response = await apiClient.get('/novels/', { params: { user: userId } })
    return response.data
  },

  async follow(userId: number): Promise<void> {
    await apiClient.post('/follows/', { followee: userId })
  },

  async unfollow(userId: number): Promise<void> {
    // フォローレコードを検索して削除
    const res = await apiClient.get('/follows/', { params: { followee: userId } })
    if (res.data.results?.length > 0) {
      await apiClient.delete(`/follows/${res.data.results[0].id}/`)
    }
  },

  async getFollowCount(userId: number): Promise<{ followers: number; following: number }> {
    const [followers, following] = await Promise.all([
      apiClient.get('/follows/', { params: { followee: userId, limit: 1 } }),
      apiClient.get('/follows/', { params: { follower: userId, limit: 1 } }),
    ])
    return {
      followers: followers.data.count || 0,
      following: following.data.count || 0,
    }
  },

  async isFollowing(followerId: number, followeeId: number): Promise<boolean> {
    const res = await apiClient.get('/follows/', {
      params: { follower: followerId, followee: followeeId },
    })
    return (res.data.count || 0) > 0
  },
}
