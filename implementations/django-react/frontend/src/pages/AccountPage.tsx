import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { ApiError, api } from '../api/client'
import type { User } from '../api/types'
import { useAuth } from '../auth/AuthContext'

/** SC-05 アカウント設定画面（DL-06 アカウント削除確認を含む） */
export default function AccountPage() {
  const { user, setUser } = useAuth()
  const navigate = useNavigate()
  const [username, setUsername] = useState(user?.username ?? '')
  const [bio, setBio] = useState(user?.bio ?? '')
  const [message, setMessage] = useState('')
  const [error, setError] = useState('')
  const [showDelete, setShowDelete] = useState(false)
  const [confirmId, setConfirmId] = useState('')

  if (!user) return null

  const onSave = async (e: React.FormEvent) => {
    e.preventDefault()
    setMessage('')
    setError('')
    try {
      const updated = await api.patch<User>('/api/auth/me/', { username, bio })
      setUser(updated)
      setMessage('保存しました。')
    } catch (err) {
      setError(err instanceof ApiError ? err.firstMessage() : '保存に失敗しました。')
    }
  }

  const onDelete = async () => {
    await api.delete('/api/auth/me/')
    setUser(null)
    navigate('/login')
  }

  return (
    <div className="form-card">
      <h1>アカウント設定</h1>
      <dl className="readonly-fields">
        <dt>ユーザーID</dt>
        <dd>@{user.user_id}（変更不可）</dd>
        <dt>メールアドレス</dt>
        <dd>{user.email}</dd>
      </dl>
      {message && <p className="form-message">{message}</p>}
      {error && <p className="form-error">{error}</p>}
      <form onSubmit={onSave}>
        <label>
          ユーザー名 *
          <input required value={username} onChange={(e) => setUsername(e.target.value)} />
        </label>
        <label>
          自己紹介
          <textarea rows={4} maxLength={1024} value={bio} onChange={(e) => setBio(e.target.value)} />
          <span className="field-help">残り {1024 - bio.length} 文字</span>
        </label>
        <button type="submit" className="primary">
          保存
        </button>
      </form>

      <section className="danger-zone">
        <h2>危険な操作</h2>
        <button className="danger" onClick={() => setShowDelete(true)}>
          アカウントを削除する
        </button>
      </section>

      {showDelete && (
        <div className="modal-backdrop">
          <div className="modal">
            <h2>アカウントを削除しますか？</h2>
            <p>ペンネーム・World・設定・作品などすべてのデータが削除されます。</p>
            <label>
              確認のためユーザーID（{user.user_id}）を入力してください
              <input value={confirmId} onChange={(e) => setConfirmId(e.target.value)} />
            </label>
            <div className="modal-actions">
              <button onClick={() => setShowDelete(false)}>キャンセル</button>
              <button className="danger" disabled={confirmId !== user.user_id} onClick={onDelete}>
                削除する
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
