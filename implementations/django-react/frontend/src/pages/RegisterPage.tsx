import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { ApiError, api } from '../api/client'
import type { User } from '../api/types'
import { useAuth } from '../auth/AuthContext'

/** SC-01 ユーザー登録画面 */
export default function RegisterPage() {
  const { setUser } = useAuth()
  const navigate = useNavigate()
  const [form, setForm] = useState({ email: '', user_id: '', username: '', password: '' })
  const [showPassword, setShowPassword] = useState(false)
  const [errors, setErrors] = useState<Record<string, string>>({})
  const [submitting, setSubmitting] = useState(false)

  const onSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setSubmitting(true)
    setErrors({})
    try {
      const user = await api.post<User>('/api/auth/register/', form)
      setUser(user)
      navigate('/worlds')
    } catch (err) {
      if (err instanceof ApiError) {
        const fieldErrors: Record<string, string> = {}
        for (const [k, v] of Object.entries(err.body)) {
          fieldErrors[k] = Array.isArray(v) ? String(v[0]) : String(v)
        }
        setErrors(fieldErrors)
      }
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <div className="auth-card">
      <h1>ユーザー登録</h1>
      <form onSubmit={onSubmit}>
        <label>
          メールアドレス *
          <input
            type="email"
            required
            value={form.email}
            onChange={(e) => setForm({ ...form, email: e.target.value })}
          />
          {errors.email && <span className="field-error">{errors.email}</span>}
        </label>
        <label>
          ユーザーID *（変更不可）
          <input
            required
            value={form.user_id}
            onChange={(e) => setForm({ ...form, user_id: e.target.value })}
          />
          <span className="field-help">英数字・アンダースコアのみ、3〜20文字。登録後は変更できません</span>
          {errors.user_id && <span className="field-error">{errors.user_id}</span>}
        </label>
        <label>
          ユーザー名 *
          <input
            required
            value={form.username}
            onChange={(e) => setForm({ ...form, username: e.target.value })}
          />
          {errors.username && <span className="field-error">{errors.username}</span>}
        </label>
        <label>
          パスワード *
          <span className="password-row">
            <input
              type={showPassword ? 'text' : 'password'}
              required
              value={form.password}
              onChange={(e) => setForm({ ...form, password: e.target.value })}
            />
            <button type="button" className="link-button" onClick={() => setShowPassword((v) => !v)}>
              {showPassword ? '隠す' : '表示'}
            </button>
          </span>
          {errors.password && <span className="field-error">{errors.password}</span>}
        </label>
        <button type="submit" className="primary" disabled={submitting}>
          登録する
        </button>
      </form>
      <p>
        ログインは<Link to="/login">こちら</Link>
      </p>
    </div>
  )
}
