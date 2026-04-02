import { useState, useEffect } from 'react'
import { useNavigate, useParams, Link } from 'react-router-dom'
import { novelsApi } from '../../api/novels'
import { ErrorMessage } from '../../components/Common/ErrorMessage'
import { LoadingSpinner } from '../../components/Common/LoadingSpinner'
import type { EpisodeListItem } from '../../types'
import styles from './EpisodeCreatePage.module.css'

export function EpisodeCreatePage() {
  const { id } = useParams<{ id: string }>()
  const novelId = Number(id)
  const navigate = useNavigate()

  const [title, setTitle] = useState('')
  const [body, setBody] = useState('')
  const [episodeNumber, setEpisodeNumber] = useState(1)
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    novelsApi.getEpisodes(novelId).then((eps: EpisodeListItem[]) => {
      setEpisodeNumber(eps.length + 1)
    }).catch(() => {})
  }, [novelId])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!title.trim()) {
      setError('タイトルを入力してください。')
      return
    }
    if (!body.trim()) {
      setError('本文を入力してください。')
      return
    }
    setError(null)
    setIsLoading(true)
    try {
      const episode = await novelsApi.createEpisode({
        novel: novelId,
        title,
        body,
        episode_number: episodeNumber,
      })
      navigate(`/novels/${novelId}/episodes/${episode.id}`)
    } catch (err: unknown) {
      const axiosError = err as { response?: { data?: Record<string, unknown> } }
      const data = axiosError.response?.data
      if (data) {
        const messages = Object.values(data).flat().join(' ')
        setError(String(messages) || '話の作成に失敗しました。')
      } else {
        setError('話の作成に失敗しました。')
      }
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className={styles.page}>
      <h1 className={styles.title}>新しい話を投稿</h1>
      {error && <ErrorMessage message={error} />}
      <form className={styles.form} onSubmit={handleSubmit}>
        <div className={styles.field}>
          <label className={styles.label} htmlFor="episodeNumber">
            話番号
          </label>
          <input
            id="episodeNumber"
            className={styles.input}
            type="number"
            value={episodeNumber}
            onChange={(e) => setEpisodeNumber(Number(e.target.value))}
            min={1}
          />
        </div>

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
            placeholder="話のタイトル"
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
            placeholder="本文を入力..."
            required
            maxLength={50000}
          />
          <span className={styles.charCount}>{body.length} / 50000文字</span>
        </div>

        <div className={styles.actions}>
          <Link to={`/novels/${novelId}`} className={styles.cancelButton}>
            キャンセル
          </Link>
          <button type="submit" className={styles.submitButton} disabled={isLoading}>
            {isLoading && <LoadingSpinner inline />}
            投稿する
          </button>
        </div>
      </form>
    </div>
  )
}
