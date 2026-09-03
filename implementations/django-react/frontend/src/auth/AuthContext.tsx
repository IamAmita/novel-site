import { createContext, useContext, useEffect, useState } from 'react'
import type { ReactNode } from 'react'
import { api, ensureCsrf } from '../api/client'
import type { User } from '../api/types'

interface AuthState {
  user: User | null
  loading: boolean
  setUser: (u: User | null) => void
  logout: () => Promise<void>
}

const AuthContext = createContext<AuthState>({
  user: null,
  loading: true,
  setUser: () => {},
  logout: async () => {},
})

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    ensureCsrf()
      .then(() => api.get<User>('/api/auth/me/'))
      .then(setUser)
      .catch(() => setUser(null))
      .finally(() => setLoading(false))
  }, [])

  const logout = async () => {
    await api.post('/api/auth/logout/')
    setUser(null)
  }

  return (
    <AuthContext.Provider value={{ user, loading, setUser, logout }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  return useContext(AuthContext)
}
