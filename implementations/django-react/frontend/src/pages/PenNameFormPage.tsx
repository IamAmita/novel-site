import { useEffect, useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import { api } from '../api/client'
import type { PenName } from '../api/types'
import PenNameForm from '../components/PenNameForm'

/** SC-07 ペンネーム作成・編集フォーム（ページ版） */
export default function PenNameFormPage() {
  const { id } = useParams()
  const navigate = useNavigate()
  const [initial, setInitial] = useState<PenName | undefined>()
  const [loading, setLoading] = useState(Boolean(id))

  useEffect(() => {
    if (id) {
      api.get<PenName>(`/api/pennames/${id}/`).then((p) => {
        setInitial(p)
        setLoading(false)
      })
    }
  }, [id])

  if (loading) return <div className="page-loading">読み込み中…</div>

  return (
    <div className="form-card">
      <h1>{id ? 'ペンネーム編集' : 'ペンネーム作成'}</h1>
      <PenNameForm
        initial={initial}
        onSaved={() => navigate('/pennames')}
        onCancel={() => navigate('/pennames')}
      />
    </div>
  )
}
