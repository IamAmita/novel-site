import { useState, useEffect } from 'react'
import { useNavigate, useParams, Link } from 'react-router-dom'
import { novelsApi } from '../../api/novels'
import { LoadingSpinner } from '../../components/Common/LoadingSpinner'
import { ErrorMessage } from '../../components/Common/ErrorMessage'
import styles from './EpisodeCreatePage.module.css'

export function EpisodeEditPage() {
  const { id, episodeId } = useParams<{ id: string; episodeId: string }>()
  const novelId = Number(id)
  const epId = Number(episodeId)
  const navigate = useNavigate()

  const [title, setTitle] = useState('')
  const [body, setBody] = useState('')
  const [isLoading, setIsLoading] = useState(true)
  const [isSaving, setIsSaving] = useState(false)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    novelsApi.getEpisode(epId).then((ep) => {
      setTitle(ep.title)
      setBody(ep.body)
      setIsLoading(false)
    }).catch(() => {
      setError('話の取得に失敗しました。')
      setIsLoading(false)
    })
  }, [epId])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError(null)
    setIsSaving(true)
    try {
      await novelsApi.updateEpisode(epId, { title, body })
      navigate(`/novels/${novelId}/episodes/${epId}`)
    } catch {
      setError('更新に失敗しました。')
    } finally {
      setIsSaving(false)
    }
  }

  if (isLoading) return <LoadingSpinner />
  if (error && !title) return <ErrorMessage message={error} title="エラー" />

  return (
    <div className={styles.page}>
      <h1 className={styles.title}>話を編集</h1>
      {error && <ErrorMessage message={error} />}
      <form className={styles.form} onSubmit={handleSubmit}>
        <div className={styles.field}>
          <label className={styles.label} htmlFor="title">
            タイトル<span className={styles.required}>*</span>
          </label>
          <input
            id="title"
            className={styles.input}
            type="text"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            required
            maxLength={200}
          />
        </div>

        <div className={styles.field}>
          <label className={styles.label} htmlFor="body">
            本文<span className={styles.required}>*</span>
          </label>
          <textarea
            id="body"
            className={styles.textarea}
            value={body}
            onChange={(e) => setBody(e.target.value)}
            required
            maxLength={50000}
          />
          <span className={styles.charCount}>{body.length} / 50000文字</span>
        </div>

        <div className={styles.actions}>
          <Link to={`/novels/${novelId}/episodes/${epId}`} className={styles.cancelButton}>
            キャンセル
          </Link>
          <button type="submit" className={styles.submitButton} disabled={isSaving}>
            {isSaving && <LoadingSpinner inline />}
            保存する
          </button>
        </div>
      </form>
    </div>
  )
}
