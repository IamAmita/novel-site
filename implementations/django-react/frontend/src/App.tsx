import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom'
import { AuthProvider } from './auth/AuthContext'
import Layout from './components/Layout'
import AccountPage from './pages/AccountPage'
import LoginPage from './pages/LoginPage'
import PenNameFormPage from './pages/PenNameFormPage'
import PenNameListPage from './pages/PenNameListPage'
import RegisterPage from './pages/RegisterPage'
import WorldDetailPage from './pages/WorldDetailPage'
import WorldFormPage from './pages/WorldFormPage'
import WorldListPage from './pages/WorldListPage'

export default function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/register" element={<RegisterPage />} />
          <Route path="/login" element={<LoginPage />} />
          <Route element={<Layout />}>
            <Route path="/" element={<Navigate to="/worlds" replace />} />
            <Route path="/worlds" element={<WorldListPage />} />
            <Route path="/worlds/new" element={<WorldFormPage />} />
            <Route path="/worlds/:id" element={<WorldDetailPage />} />
            <Route path="/worlds/:id/edit" element={<WorldFormPage />} />
            <Route path="/pennames" element={<PenNameListPage />} />
            <Route path="/pennames/new" element={<PenNameFormPage />} />
            <Route path="/pennames/:id/edit" element={<PenNameFormPage />} />
            <Route path="/account" element={<AccountPage />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  )
}
