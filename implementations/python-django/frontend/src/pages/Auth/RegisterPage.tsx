import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../../hooks/useAuth'
import { ErrorMessage } from '../../components/Common/ErrorMessage'
import { LoadingSpinner } from '../../components/Common/LoadingSpinner'
import styles from './RegisterPage.module.css'

export function RegisterPage() {
  const { register, isAuthenticated } = useAuth()
  const navigate = useNavigate()

  const [username, setUsername] = useState('')
  const [email, setEmail] = useState('')
  const [displayName, setDisplayName] = useState('')
  const [password, setPassword] = useState('')
  const [passwordConfirm, setPasswordConfirm] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  if (isAuthenticated) {
    navigate('/', { replace: true })
    return null
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (password !== passwordConfirm) {
      setError('パスワードが一致しません。')
      return
    }
    if (password.length < 8) {
      setError('パスワードは8文字以上で入力してください。')
      return
    }
    setError(null)
    setIsLoading(true)
    try {
      await register({ username, email, password, password_confirm: passwordConfirm, display_name: displayName })
      navigate('/')
    } catch (err: unknown) {
      const axiosError = err as { response?: { data?: Record<string, string[]> } }
      const data = axiosError.response?.data
      if (data) {
        const messages = Object.values(data).flat().join(' ')
        setError(messages || '登録に失敗しました。')
      } else {
        setError('登録に失敗しました。')
      }
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className={styles.page}>
      <div className={styles.card}>
        <h1 className={styles.title}>新規登録</h1>
        {error && <ErrorMessage message={error} />}
        <form className={styles.form} onSubmit={handleSubmit}>
          <div className={styles.field}>
            <label className={styles.label} htmlFor="username">
              ユーザー名
            </label>
            <span className={styles.hint}>ログイン時に使用します（英数字・アンダースコア）</span>
            <input
              id="username"
              className={styles.input}
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
              autoComplete="username"
            />
          </div>
          <div className={styles.field}>
            <label className={styles.label} htmlFor="displayName">
              表示名
            </label>
            <span className={styles.hint}>プロフィールに表示される名前（任意）</span>
            <input
              id="displayName"
              className={styles.input}
              type="text"
              value={displayName}
              onChange={(e) => setDisplayName(e.target.value)}
              autoComplete="nickname"
            />
          </div>
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
            <span className={styles.hint}>8文字以上</span>
            <input
              id="password"
              className={styles.input}
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              autoComplete="new-password"
            />
          </div>
          <div className={styles.field}>
            <label className={styles.label} htmlFor="passwordConfirm">
              パスワード（確認）
            </label>
            <input
              id="passwordConfirm"
              className={styles.input}
              type="password"
              value={passwordConfirm}
              onChange={(e) => setPasswordConfirm(e.target.value)}
              required
              autoComplete="new-password"
            />
          </div>
          <button type="submit" className={styles.submitButton} disabled={isLoading}>
            {isLoading && <LoadingSpinner inline />}
            登録する
          </button>
        </form>
        <p className={styles.footer}>
          すでにアカウントをお持ちの方は{' '}
          <Link to="/login" className={styles.link}>
            ログイン
          </Link>
        </p>
      </div>
    </div>
  )
}
