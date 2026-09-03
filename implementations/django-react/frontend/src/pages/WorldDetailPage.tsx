import { useEffect, useState } from 'react'
import { Link, useNavigate, useParams } from 'react-router-dom'
import { api } from '../api/client'
import type { World } from '../api/types'

/** SC-09 World詳細画面（DL-01 削除確認を含む） */
export default function WorldDetailPage() {
  const { id } = useParams()
  const navigate = useNavigate()
  const [world, setWorld] = useState<World | null>(null)
  const [showDelete, setShowDelete] = useState(false)

  useEffect(() => {
    api.get<World>(`/api/worlds/${id}/`).then(setWorld)
  }, [id])

  if (!world) return <div className="page-loading">読み込み中…</div>

  const onDelete = async () => {
    await api.delete(`/api/worlds/${world.id}/`)
    navigate('/worlds')
  }

  return (
    <div>
      <div className="page-header">
        <h1>{world.name}</h1>
        <span className="page-actions">
          <button className="button" disabled title="変更履歴は未実装（優先順位④）">
            変更履歴
          </button>
          <Link className="button" to={`/worlds/${world.id}/edit`}>
            編集
          </Link>
        </span>
      </div>
      <p className="row-meta">名義: {world.owner_pen_name_display}</p>
      <div className="detail-body">
        {world.cover_image ? (
          <img className="cover" src={world.cover_image} alt="" />
        ) : (
          <div className="cover cover-placeholder">表紙なし</div>
        )}
        <p className="description">{world.description || '（説明はありません）'}</p>
      </div>
      <p>
        <button className="button" disabled title="テンプレート管理は未実装（優先順位②）">
          設定テンプレートを管理
        </button>
      </p>
      <section className="danger-zone">
        <button className="danger" onClick={() => setShowDelete(true)}>
          このWorldを削除
        </button>
      </section>

      {showDelete && (
        <div className="modal-backdrop">
          <div className="modal">
            <h2>「{world.name}」を削除しますか？</h2>
            <p>削除後も一覧から復元できます。</p>
            <div className="modal-actions">
              <button onClick={() => setShowDelete(false)}>キャンセル</button>
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
