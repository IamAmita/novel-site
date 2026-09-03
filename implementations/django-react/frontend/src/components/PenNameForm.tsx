import { useState } from 'react'
import { ApiError, api } from '../api/client'
import type { PenName } from '../api/types'

interface Props {
  initial?: PenName
  onSaved: (pen: PenName) => void
  onCancel: () => void
}

/** SC-07 ペンネームフォームの本体。ページ版とモーダル版（World作成時の強制作成）で共用 */
export default function PenNameForm({ initial, onSaved, onCancel }: Props) {
  const [displayName, setDisplayName] = useState(initial?.display_name ?? '')
  const [bio, setBio] = useState(initial?.bio ?? '')
  const [icon, setIcon] = useState<File | null>(null)
  const [error, setError] = useState('')
  const [submitting, setSubmitting] = useState(false)

  const onSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setSubmitting(true)
    setError('')
    const form = new FormData()
    form.append('display_name', displayName)
    form.append('bio', bio)
    if (icon) form.append('icon', icon)
    try {
      const saved = initial
        ? await api.patch<PenName>(`/api/pennames/${initial.id}/`, form)
        : await api.post<PenName>('/api/pennames/', form)
      onSaved(saved)
    } catch (err) {
      setError(err instanceof ApiError ? err.firstMessage() : '保存に失敗しました。')
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <form onSubmit={onSubmit}>
      {error && <p className="form-error">{error}</p>}
      <label>
        表示名 *
        <input required maxLength={100} value={displayName} onChange={(e) => setDisplayName(e.target.value)} />
      </label>
      <label>
        アイコン
        <input type="file" accept="image/*" onChange={(e) => setIcon(e.target.files?.[0] ?? null)} />
      </label>
      <label>
        自己紹介
        <textarea rows={3} maxLength={1024} value={bio} onChange={(e) => setBio(e.target.value)} />
        <span className="field-help">残り {1024 - bio.length} 文字</span>
      </label>
      <div className="form-actions">
        <button type="button" onClick={onCancel}>
          キャンセル
        </button>
        <button type="submit" className="primary" disabled={submitting}>
          保存
        </button>
      </div>
    </form>
  )
}
