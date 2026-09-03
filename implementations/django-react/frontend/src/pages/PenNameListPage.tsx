import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { ApiError, api } from '../api/client'
import type { PenName } from '../api/types'

/** SC-06 ペンネーム一覧画面（DL-05 削除確認を含む） */
export default function PenNameListPage() {
  const [pennames, setPennames] = useState<PenName[]>([])
  const [deleting, setDeleting] = useState<PenName | null>(null)
  const [error, setError] = useState('')

  const load = () => {
    api.get<PenName[]>('/api/pennames/').then(setPennames)
  }
  useEffect(load, [])

  const onDelete = async () => {
    if (!deleting) return
    setError('')
    try {
      await api.delete(`/api/pennames/${deleting.id}/`)
      setDeleting(null)
      load()
    } catch (err) {
      setError(err instanceof ApiError ? err.firstMessage() : '削除に失敗しました。')
      setDeleting(null)
    }
  }

  return (
    <div>
      <div className="page-header">
        <h1>ペンネーム</h1>
        <Link className="button primary" to="/pennames/new">
          ＋新規作成
        </Link>
      </div>
      {error && <p className="form-error">{error}</p>}
      {pennames.length === 0 ? (
        <p className="empty-state">ペンネームはまだありません。World作成時にも作成できます。</p>
      ) : (
        <ul className="row-list">
          {pennames.map((p) => (
            <li key={p.id} className="row">
              <span className="row-icon">{p.icon ? <img src={p.icon} alt="" /> : '○'}</span>
              <span className="row-title">{p.display_name}</span>
              <span className="row-meta">World: {p.world_count}</span>
              <span className="row-actions">
                <Link to={`/pennames/${p.id}/edit`}>編集</Link>
                <button
                  className="link-button"
                  disabled={p.world_count > 0}
                  title={p.world_count > 0 ? 'Worldを保持しているため削除できません' : undefined}
                  onClick={() => setDeleting(p)}
                >
                  削除
                </button>
              </span>
            </li>
          ))}
        </ul>
      )}

      {deleting && (
        <div className="modal-backdrop">
          <div className="modal">
            <h2>「{deleting.display_name}」を削除しますか？</h2>
            <div className="modal-actions">
              <button onClick={() => setDeleting(null)}>キャンセル</button>
              <button className="danger" onClick={onDelete}>
                削除する
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
