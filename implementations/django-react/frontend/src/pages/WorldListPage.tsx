import { useEffect, useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { api } from '../api/client'
import type { World } from '../api/types'

/** SC-08 World一覧画面（検索・削除済みトグル・復元） */
export default function WorldListPage() {
  const navigate = useNavigate()
  const [worlds, setWorlds] = useState<World[]>([])
  const [query, setQuery] = useState('')
  const [showDeleted, setShowDeleted] = useState(false)
  const [loaded, setLoaded] = useState(false)

  const load = () => {
    const params = new URLSearchParams()
    if (query) params.set('q', query)
    if (showDeleted) params.set('include_deleted', '1')
    api.get<World[]>(`/api/worlds/?${params}`).then((rows) => {
      setWorlds(rows)
      setLoaded(true)
    })
  }
  useEffect(load, [query, showDeleted])

  const onRestore = async (w: World) => {
    await api.post(`/api/worlds/${w.id}/restore/`)
    load()
  }

  return (
    <div>
      <div className="page-header">
        <h1>World一覧</h1>
        <input
          className="search-box"
          placeholder="World名で検索"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />
        <Link className="button primary" to="/worlds/new">
          ＋新規作成
        </Link>
      </div>
      <label className="toggle">
        <input type="checkbox" checked={showDeleted} onChange={(e) => setShowDeleted(e.target.checked)} />
        削除済みを表示
      </label>

      {loaded && worlds.length === 0 ? (
        <p className="empty-state">
          {query ? '該当するWorldがありません。' : '最初のWorldを作りましょう。'}
        </p>
      ) : (
        <ul className="row-list">
          {worlds.map((w) => (
            <li
              key={w.id}
              className={`row clickable ${w.is_deleted ? 'row-deleted' : ''}`}
              onClick={() => !w.is_deleted && navigate(`/worlds/${w.id}`)}
            >
              <div className="row-main">
                <span className="row-title">
                  {w.name}
                  {w.is_deleted && <span className="badge">削除済み</span>}
                </span>
                <span className="row-sub">{w.description.split('\n')[0]}</span>
              </div>
              <div className="row-side">
                <span className="row-meta">名義: {w.owner_pen_name_display}</span>
                <span className="row-meta">
                  更新: {new Date(w.updated_at).toLocaleDateString('ja-JP')}
                </span>
                {w.is_deleted && (
                  <button
                    className="link-button"
                    onClick={(e) => {
                      e.stopPropagation()
                      onRestore(w)
                    }}
                  >
                    復元
                  </button>
                )}
              </div>
            </li>
          ))}
        </ul>
      )}
    </div>
  )
}
