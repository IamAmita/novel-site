import { useState } from 'react'
import { Link, useNavigate, useLocation } from 'react-router-dom'
import { useAuth } from '../../hooks/useAuth'
import { ErrorMessage } from '../../components/Common/ErrorMessage'
import { LoadingSpinner } from '../../components/Common/LoadingSpinner'
import styles from './LoginPage.module.css'

export function LoginPage() {
  const { login, isAuthenticated } = useAuth()
  const navigate = useNavigate()
  const location = useLocation()
  const from = (location.state as { from?: string })?.from || '/'

  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  if (isAuthenticated) {
    navigate(from, { replace: true })
    return null
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError(null)
    setIsLoading(true)
    try {
      await login({ email, password })
      navigate(from, { replace: true })
    } catch {
      setError('ユーザー名またはパスワードが正しくありません。')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className={styles.page}>
      <div className={styles.card}>
        <h1 className={styles.title}>ログイン</h1>
        {error && <ErrorMessage message={error} />}
        <form className={styles.form} onSubmit={handleSubmit}>
          <div className={styles.field}>
            <label className={styles.label} htmlFor="email">
              メールアドレス
            </label>
            <input
              id="email"
              className={styles.input}
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              autoComplete="email"
            />
          </div>
          <div className={styles.field}>
            <label className={styles.label} htmlFor="password">
              パスワード
            </label>
            <input
              id="password"
              className={styles.input}
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              autoComplete="current-password"
            />
          </div>
          <button type="submit" className={styles.submitButton} disabled={isLoading}>
            {isLoading && <LoadingSpinner inline />}
            ログイン
          </button>
        </form>
        <p className={styles.footer}>
          アカウントをお持ちでない方は{' '}
          <Link to="/register" className={styles.link}>
            新規登録
          </Link>
        </p>
      </div>
    </div>
  )
}
