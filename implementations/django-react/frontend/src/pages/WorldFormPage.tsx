import { useEffect, useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import { ApiError, api } from '../api/client'
import type { PenName, World } from '../api/types'
import PenNameForm from '../components/PenNameForm'

/** SC-10 World作成・編集フォーム。ペンネーム0件時は作成モーダルを強制表示（SC-07モーダル版） */
export default function WorldFormPage() {
  const { id } = useParams()
  const navigate = useNavigate()
  const [pennames, setPennames] = useState<PenName[] | null>(null)
  const [showPenModal, setShowPenModal] = useState(false)
  const [form, setForm] = useState({ name: '', description: '', owner_pen_name: '' })
  const [cover, setCover] = useState<File | null>(null)
  const [error, setError] = useState('')
  const [submitting, setSubmitting] = useState(false)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const jobs: Promise<void>[] = [
      api.get<PenName[]>('/api/pennames/').then((rows) => {
        setPennames(rows)
        if (rows.length === 0) setShowPenModal(true)
        else if (!id) setForm((f) => (f.owner_pen_name ? f : { ...f, owner_pen_name: String(rows[0].id) }))
      }),
    ]
    if (id) {
      jobs.push(
        api.get<World>(`/api/worlds/${id}/`).then((w) => {
          setForm({ name: w.name, description: w.description, owner_pen_name: String(w.owner_pen_name) })
        }),
      )
    }
    Promise.all(jobs).finally(() => setLoading(false))
  }, [id])

  const onPenNameCreated = (pen: PenName) => {
    setPennames((rows) => [...(rows ?? []), pen])
    setForm((f) => ({ ...f, owner_pen_name: String(pen.id) }))
    setShowPenModal(false)
  }

  const onSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setSubmitting(true)
    setError('')
    const data = new FormData()
    data.append('name', form.name)
    data.append('description', form.description)
    data.append('owner_pen_name', form.owner_pen_name)
    if (cover) data.append('cover_image', cover)
    try {
      const saved = id
        ? await api.patch<World>(`/api/worlds/${id}/`, data)
        : await api.post<World>('/api/worlds/', data)
      navigate(`/worlds/${saved.id}`)
    } catch (err) {
      setError(err instanceof ApiError ? err.firstMessage() : '保存に失敗しました。')
    } finally {
      setSubmitting(false)
    }
  }

  if (loading) return <div className="page-loading">読み込み中…</div>

  const noPenName = (pennames ?? []).length === 0

  return (
    <div className="form-card">
      <h1>{id ? 'World編集' : 'World作成'}</h1>
      {error && <p className="form-error">{error}</p>}
      <form onSubmit={onSubmit}>
        <label>
          名前 *
          <input
            required
            maxLength={100}
            value={form.name}
            onChange={(e) => setForm({ ...form, name: e.target.value })}
          />
          <span className="field-help">残り {100 - form.name.length} 文字</span>
        </label>
        <label>
          説明
          <textarea
            rows={5}
            maxLength={1024}
            value={form.description}
            onChange={(e) => setForm({ ...form, description: e.target.value })}
          />
          <span className="field-help">残り {1024 - form.description.length} 文字</span>
        </label>
        <label>
          表紙画像
          <input type="file" accept="image/*" onChange={(e) => setCover(e.target.files?.[0] ?? null)} />
        </label>
        <label>
          名義 *
          {noPenName ? (
            <span className="field-error">
              ペンネームを作成してください{' '}
              <button type="button" className="link-button" onClick={() => setShowPenModal(true)}>
                作成する
              </button>
            </span>
          ) : (
            <select
              required
              value={form.owner_pen_name}
              onChange={(e) => setForm({ ...form, owner_pen_name: e.target.value })}
            >
              {(pennames ?? []).map((p) => (
                <option key={p.id} value={p.id}>
                  {p.display_name}
                </option>
              ))}
            </select>
          )}
        </label>
        <div className="form-actions">
          <button type="button" onClick={() => navigate(-1)}>
            キャンセル
          </button>
          <button type="submit" className="primary" disabled={submitting || noPenName}>
            保存
          </button>
        </div>
      </form>

      {showPenModal && (
        <div className="modal-backdrop">
          <div className="modal">
            <h2>ペンネーム作成</h2>
            <p>World作成にはペンネーム（名義）が必要です。</p>
            <PenNameForm onSaved={onPenNameCreated} onCancel={() => setShowPenModal(false)} />
          </div>
        </div>
      )}
    </div>
  )
}
