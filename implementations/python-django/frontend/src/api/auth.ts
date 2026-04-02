import apiClient from './client'
import type { User, LoginRequest, RegisterRequest } from '../types'

interface AuthResponse {
  user: User
  access: string
  refresh: string
}

export const authApi = {
  async register(data: RegisterRequest): Promise<AuthResponse> {
    const response = await apiClient.post('/auth/register/', data)
    return response.data
  },

  async login(data: LoginRequest): Promise<AuthResponse> {
    const response = await apiClient.post('/auth/login/', data)
    return response.data
  },

  async refresh(refreshToken: string): Promise<{ access: string }> {
    const response = await apiClient.post('/auth/token/refresh/', {
      refresh: refreshToken,
    })
    return response.data
  },

  logout() {
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
  },
}
