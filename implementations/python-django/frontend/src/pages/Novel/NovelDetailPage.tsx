import { useState, useEffect } from 'react'
import { useParams, Link, useNavigate } from 'react-router-dom'
import apiClient from '../../api/client'
import { novelsApi } from '../../api/novels'
import { useAuth } from '../../hooks/useAuth'
import { LoadingSpinner } from '../../components/Common/LoadingSpinner'
import { ErrorMessage } from '../../components/Common/ErrorMessage'
import type { Novel, EpisodeListItem, Comment } from '../../types'
import styles from './NovelDetailPage.module.css'

function formatDate(str: string) {
  return new Date(str).toLocaleDateString('ja-JP', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
  })
}

export function NovelDetailPage() {
  const { id } = useParams<{ id: string }>()
  const novelId = Number(id)
  const { user, isAuthenticated } = useAuth()
  const navigate = useNavigate()

  const [novel, setNovel] = useState<Novel | null>(null)
  const [episodes, setEpisodes] = useState<EpisodeListItem[]>([])
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
        const [novelData, episodesData] = await Promise.all([
          novelsApi.getDetail(novelId),
          novelsApi.getEpisodes(novelId),
        ])
        setNovel(novelData)
        setEpisodes(episodesData)
        // クラスID 12 = novels (MasterClass)
        const commentsRes = await apiClient.get('/comments/', {
          params: { class_id: 12, target_id: novelId },
        })
        setComments(commentsRes.data.results || [])
      } catch {
        setError('作品の取得に失敗しました。')
      } finally {
        setIsLoading(false)
      }
    }
    fetchData()
  }, [novelId])

  const handleDeleteNovel = async () => {
    if (!window.confirm('この作品を削除しますか？')) return
    try {
      await novelsApi.delete(novelId)
      navigate('/')
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
        class_id: 12,
        target_id: novelId,
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
  if (!novel) return null

  const isAuthor = user?.id === novel.user

  return (
    <div className={styles.page}>
      <div className={styles.header}>
        <div className={styles.titleRow}>
          <h1 className={styles.title}>{novel.info.title}</h1>
          {novel.info.is_r18 && <span className={styles.r18Badge}>R18</span>}
        </div>

        <div className={styles.meta}>
          <span className={styles.metaItem}>
            作者：
            <Link to={`/users/${novel.author.id}`} className={styles.metaLink}>
              {novel.author.profile?.display_name || novel.author.username}
            </Link>
          </span>
          <span className={styles.metaItem}>📖 {novel.episode_count}話</span>
          <span className={styles.metaItem}>更新：{formatDate(novel.updated_at)}</span>
        </div>

        <div className={styles.tags}>
          {novel.category_detail && (
            <span className={styles.category}>{novel.category_detail.name}</span>
          )}
          {novel.tags.map((tag) => (
            <span key={tag.id} className={styles.tag}>
              #{tag.name}
            </span>
          ))}
        </div>

        {novel.info.synopsis && (
          <p className={styles.summary}>{novel.info.synopsis}</p>
        )}

        {isAuthor && (
          <div className={styles.actions}>
            <Link to={`/novels/${novelId}/edit`} className={styles.editLink}>
              編集
            </Link>
            <Link to={`/novels/${novelId}/episodes/create`} className={styles.editLink}>
              話を追加
            </Link>
            <button className={styles.deleteButton} onClick={handleDeleteNovel}>
              削除
            </button>
          </div>
        )}
      </div>

      <div className={styles.section}>
        <h2 className={styles.sectionTitle}>目次（{episodes.length}話）</h2>
        {episodes.length === 0 ? (
          <p style={{ color: '#999', fontSize: '0.9rem' }}>まだ話が投稿されていません。</p>
        ) : (
          <div className={styles.episodeList}>
            {episodes.map((ep) => (
              <Link
                key={ep.id}
                to={`/novels/${novelId}/episodes/${ep.id}`}
                className={styles.episodeItem}
              >
                <span className={styles.episodeNumber}>第{ep.episode_number}話</span>
                <span className={styles.episodeTitle}>{ep.title}</span>
                <span className={styles.episodeDate}>{formatDate(ep.updated_at)}</span>
              </Link>
            ))}
          </div>
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
