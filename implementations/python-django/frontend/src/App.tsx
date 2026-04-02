import { type ReactNode } from 'react'
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { AuthProvider } from './contexts/AuthContext'
import { useAuth } from './hooks/useAuth'
import { Layout } from './components/Layout/Layout'
import { LoadingSpinner } from './components/Common/LoadingSpinner'

import { HomePage } from './pages/Home/HomePage'
import { LoginPage } from './pages/Auth/LoginPage'
import { RegisterPage } from './pages/Auth/RegisterPage'
import { NovelDetailPage } from './pages/Novel/NovelDetailPage'
import { EpisodeReadPage } from './pages/Novel/EpisodeReadPage'
import { NovelCreatePage } from './pages/Novel/NovelCreatePage'
import { NovelEditPage } from './pages/Novel/NovelEditPage'
import { EpisodeCreatePage } from './pages/Novel/EpisodeCreatePage'
import { EpisodeEditPage } from './pages/Novel/EpisodeEditPage'
import { ProfilePage } from './pages/User/ProfilePage'
import { EditProfilePage } from './pages/User/EditProfilePage'
import { NotFoundPage } from './pages/NotFoundPage'

function PrivateRoute({ children }: { children: ReactNode }) {
  const { isAuthenticated, isLoading } = useAuth()
  if (isLoading) return <LoadingSpinner />
  return isAuthenticated ? <>{children}</> : <Navigate to="/login" replace />
}

function AppRoutes() {
  return (
    <Layout>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />

        <Route path="/novels/create" element={
          <PrivateRoute><NovelCreatePage /></PrivateRoute>
        } />
        <Route path="/novels/:id" element={<NovelDetailPage />} />
        <Route path="/novels/:id/edit" element={
          <PrivateRoute><NovelEditPage /></PrivateRoute>
        } />
        <Route path="/novels/:id/episodes/create" element={
          <PrivateRoute><EpisodeCreatePage /></PrivateRoute>
        } />
        <Route path="/novels/:id/episodes/:episodeId" element={<EpisodeReadPage />} />
        <Route path="/novels/:id/episodes/:episodeId/edit" element={
          <PrivateRoute><EpisodeEditPage /></PrivateRoute>
        } />

        <Route path="/users/:id" element={<ProfilePage />} />
        <Route path="/users/:id/edit" element={
          <PrivateRoute><EditProfilePage /></PrivateRoute>
        } />

        <Route path="*" element={<NotFoundPage />} />
      </Routes>
    </Layout>
  )
}

function App() {
  return (
    <BrowserRouter future={{ v7_startTransition: true, v7_relativeSplatPath: true }}>
      <AuthProvider>
        <AppRoutes />
      </AuthProvider>
    </BrowserRouter>
  )
}

export default App
