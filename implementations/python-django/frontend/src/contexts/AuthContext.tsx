import { createContext, useState, useEffect, useCallback, type ReactNode } from 'react'
import { authApi } from '../api/auth'
import type { User, LoginRequest, RegisterRequest } from '../types'

interface AuthContextValue {
  user: User | null
  isAuthenticated: boolean
  isLoading: boolean
  login: (data: LoginRequest) => Promise<void>
  register: (data: RegisterRequest) => Promise<void>
  logout: () => void
  updateUser: (user: User) => void
}

export const AuthContext = createContext<AuthContextValue | null>(null)

interface Props {
  children: ReactNode
}

export function AuthProvider({ children }: Props) {
  const [user, setUser] = useState<User | null>(null)
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    const storedUser = localStorage.getItem('user')
    const accessToken = localStorage.getItem('access_token')
    if (storedUser && accessToken) {
      try {
        setUser(JSON.parse(storedUser))
      } catch {
        localStorage.removeItem('user')
      }
    }
    setIsLoading(false)
  }, [])

  const login = useCallback(async (data: LoginRequest) => {
    const result = await authApi.login(data)
    localStorage.setItem('access_token', result.access)
    localStorage.setItem('refresh_token', result.refresh)
    localStorage.setItem('user', JSON.stringify(result.user))
    setUser(result.user)
  }, [])

  const register = useCallback(async (data: RegisterRequest) => {
    const result = await authApi.register(data)
    localStorage.setItem('access_token', result.access)
    localStorage.setItem('refresh_token', result.refresh)
    localStorage.setItem('user', JSON.stringify(result.user))
    setUser(result.user)
  }, [])

  const logout = useCallback(() => {
    authApi.logout()
    localStorage.removeItem('user')
    setUser(null)
  }, [])

  const updateUser = useCallback((updatedUser: User) => {
    localStorage.setItem('user', JSON.stringify(updatedUser))
    setUser(updatedUser)
  }, [])

  return (
    <AuthContext.Provider
      value={{
        user,
        isAuthenticated: !!user,
        isLoading,
        login,
        register,
        logout,
        updateUser,
      }}
    >
      {children}
    </AuthContext.Provider>
  )
}
