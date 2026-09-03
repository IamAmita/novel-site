import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { ApiError, api } from '../api/client'
import type { User } from '../api/types'
import { useAuth } from '../auth/AuthContext'

/** SC-02 ログイン画面 */
export default function LoginPage() {
  const { setUser } = useAuth()
  const navigate = useNavigate()
  const [identifier, setIdentifier] = useState('')
  const [password, setPassword] = useState('')
  const [showPassword, setShowPassword] = useState(false)
  const [error, setError] = useState('')
  const [submitting, setSubmitting] = useState(false)

  const onSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setSubmitting(true)
    setError('')
    try {
      const user = await api.post<User>('/api/auth/login/', { identifier, password })
      setUser(user)
      navigate('/worlds')
    } catch (err) {
      setError(err instanceof ApiError ? err.firstMessage() : 'ログインに失敗しました。')
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <div className="auth-card">
      <h1>ログイン</h1>
      {error && <p className="form-error">{error}</p>}
      <form onSubmit={onSubmit}>
        <label>
          メールアドレスまたはユーザーID
          <input required value={identifier} onChange={(e) => setIdentifier(e.target.value)} />
        </label>
        <label>
          パスワード
          <span className="password-row">
            <input
              type={showPassword ? 'text' : 'password'}
              required
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
            <button type="button" className="link-button" onClick={() => setShowPassword((v) => !v)}>
              {showPassword ? '隠す' : '表示'}
            </button>
          </span>
        </label>
        <button type="submit" className="primary" disabled={submitting}>
          ログインする
        </button>
      </form>
      <p>
        登録は<Link to="/register">こちら</Link>
      </p>
    </div>
  )
}
