import { useState, useEffect } from 'react'
import { useParams, Link, useNavigate } from 'react-router-dom'
import apiClient from '../../api/client'
import { novelsApi } from '../../api/novels'
import { useAuth } from '../../hooks/useAuth'
import { LoadingSpinner } from '../../components/Common/LoadingSpinner'
import { ErrorMessage } from '../../components/Common/ErrorMessage'
import type { Episode, EpisodeListItem, Comment } from '../../types'
import styles from './EpisodeReadPage.module.css'

function formatDate(str: string) {
  return new Date(str).toLocaleDateString('ja-JP', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
  })
}

export function EpisodeReadPage() {
  const { id, episodeId } = useParams<{ id: string; episodeId: string }>()
  const novelId = Number(id)
  const epId = Number(episodeId)
  const { user, isAuthenticated } = useAuth()
  const navigate = useNavigate()

  const [episode, setEpisode] = useState<Episode | null>(null)
  const [allEpisodes, setAllEpisodes] = useState<EpisodeListItem[]>([])
  const [comments, setComments] = useState<Comment[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [commentText, setCommentText] = useState('')
  const [commentSubmitting, setCommentSubmitting] = useState(false)

  useEffect(() => {
    const fetchData = async () => {
      setIsLoading(true)
      setError(null)
      try {
        const [epData, episodesData] = await Promise.all([
          novelsApi.getEpisode(epId),
          novelsApi.getEpisodes(novelId),
        ])
        setEpisode(epData)
        setAllEpisodes(episodesData)
        // クラスID 18 = episodes (MasterClass)
        const commentsRes = await apiClient.get('/comments/', {
          params: { class_id: 18, target_id: epId },
        })
        setComments(commentsRes.data.results || [])
      } catch {
        setError('話の取得に失敗しました。')
      } finally {
        setIsLoading(false)
      }
    }
    fetchData()
  }, [novelId, epId])

  const handleDeleteEpisode = async () => {
    if (!window.confirm('この話を削除しますか？')) return
    try {
      await novelsApi.deleteEpisode(epId)
      navigate(`/novels/${novelId}`)
    } catch {
      alert('削除に失敗しました。')
    }
  }

  const handleCommentSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!commentText.trim()) return
    setCommentSubmitting(true)
    try {
      const res = await apiClient.post('/comments/', {
        class_id: 18,
        target_id: epId,
        body: commentText,
      })
      setComments([...comments, res.data])
      setCommentText('')
    } catch {
      /* ignore */
    } finally {
      setCommentSubmitting(false)
    }
  }

  if (isLoading) return <LoadingSpinner />
  if (error) return <ErrorMessage message={error} title="エラー" />
  if (!episode) return null

  const currentIndex = allEpisodes.findIndex((ep) => ep.id === epId)
  const prevEpisode = currentIndex > 0 ? allEpisodes[currentIndex - 1] : null
  const nextEpisode = currentIndex < allEpisodes.length - 1 ? allEpisodes[currentIndex + 1] : null
  const isAuthor = user && episode.novel === novelId

  return (
    <div className={styles.page}>
      <div className={styles.breadcrumb}>
        <Link to="/" className={styles.breadcrumbLink}>ホーム</Link>
        <span>›</span>
        <Link to={`/novels/${novelId}`} className={styles.breadcrumbLink}>
          作品
        </Link>
        <span>›</span>
        <span>第{episode.episode_number}話</span>
      </div>

      <div className={styles.header}>
        <p className={styles.episodeNumber}>第{episode.episode_number}話</p>
        <h1 className={styles.title}>{episode.title}</h1>
      </div>

      {isAuthor && (
        <div className={styles.editActions}>
          <Link
            to={`/novels/${novelId}/episodes/${epId}/edit`}
            className={styles.editLink}
          >
            編集
          </Link>
          <button className={styles.editLink} onClick={handleDeleteEpisode} style={{ cursor: 'pointer', background: 'none' }}>
            削除
          </button>
        </div>
      )}

      <div className={styles.content}>
        {episode.body.split('\n').map((line, i) => (
          <p key={i}>{line || '\u00A0'}</p>
        ))}
      </div>

      <div className={styles.navigation}>
        {prevEpisode ? (
          <Link
            to={`/novels/${novelId}/episodes/${prevEpisode.id}`}
            className={styles.navButton}
          >
            ‹ 前の話
          </Link>
        ) : (
          <span className={`${styles.navButton} ${styles.navButtonDisabled}`}>‹ 前の話</span>
        )}
        <Link to={`/novels/${novelId}`} className={styles.backToList}>
          目次
        </Link>
        {nextEpisode ? (
          <Link
            to={`/novels/${novelId}/episodes/${nextEpisode.id}`}
            className={styles.navButton}
          >
            次の話 ›
          </Link>
        ) : (
          <span className={`${styles.navButton} ${styles.navButtonDisabled}`}>次の話 ›</span>
        )}
      </div>

      <div className={styles.section}>
        <h2 className={styles.sectionTitle}>コメント（{comments.length}件）</h2>
        {isAuthenticated ? (
          <form className={styles.commentForm} onSubmit={handleCommentSubmit}>
            <textarea
              className={styles.commentInput}
              value={commentText}
              onChange={(e) => setCommentText(e.target.value)}
              placeholder="コメントを入力..."
            />
            <button
              type="submit"
              className={styles.commentSubmit}
              disabled={commentSubmitting || !commentText.trim()}
            >
              投稿
            </button>
          </form>
        ) : (
          <p className={styles.loginPrompt}>
            コメントするには{' '}
            <Link to="/login" className={styles.loginPromptLink}>
              ログイン
            </Link>{' '}
            が必要です。
          </p>
        )}
        <div className={styles.commentList}>
          {comments.map((comment) => (
            <div key={comment.id} className={styles.comment}>
              <p className={styles.commentBody}>
                {comment.is_deleted ? '（削除されたコメントです）' : comment.body}
              </p>
              <p className={styles.commentDate}>{formatDate(comment.created_at)}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
