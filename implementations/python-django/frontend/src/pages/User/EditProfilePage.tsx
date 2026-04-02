import { useState, useEffect } from 'react'
import { useNavigate, useParams, Link } from 'react-router-dom'
import apiClient from '../../api/client'
import { usersApi } from '../../api/users'
import { useAuth } from '../../hooks/useAuth'
import { LoadingSpinner } from '../../components/Common/LoadingSpinner'
import { ErrorMessage } from '../../components/Common/ErrorMessage'
import styles from './EditProfilePage.module.css'

export function EditProfilePage() {
  const { id } = useParams<{ id: string }>()
  const userId = Number(id)
  const navigate = useNavigate()
  const { user: currentUser, updateUser } = useAuth()

  const [profileId, setProfileId] = useState<number | null>(null)
  const [displayName, setDisplayName] = useState('')
  const [biography, setBiography] = useState('')
  const [websiteUrl, setWebsiteUrl] = useState('')
  const [isLoading, setIsLoading] = useState(true)
  const [isSaving, setIsSaving] = useState(false)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    if (currentUser && currentUser.id !== userId) {
      navigate(`/users/${currentUser.id}/edit`, { replace: true })
      return
    }
    usersApi.getUser(userId).then((user) => {
      // プロフィールIDを取得するためにプロフィール一覧を検索
      apiClient.get('/profiles/', { params: { user: userId } }).then((res) => {
        const profiles = res.data.results || []
        if (profiles.length > 0) setProfileId(profiles[0].id)
      })
      setDisplayName(user.profile?.display_name ?? '')
      setBiography(user.profile?.biography ?? '')
      setWebsiteUrl(user.profile?.website_url ?? '')
      setIsLoading(false)
    }).catch(() => {
      setError('プロフィールの取得に失敗しました。')
      setIsLoading(false)
    })
  }, [userId, currentUser, navigate])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!profileId) {
      setError('プロフィール情報が見つかりません。')
      return
    }
    setError(null)
    setIsSaving(true)
    try {
      const updatedUser = await usersApi.updateProfile(profileId, {
        display_name: displayName,
        biography,
        website_url: websiteUrl || undefined,
      })
      updateUser(updatedUser)
      navigate(`/users/${userId}`)
    } catch {
      setError('プロフィールの更新に失敗しました。')
    } finally {
      setIsSaving(false)
    }
  }

  if (isLoading) return <LoadingSpinner />

  return (
    <div className={styles.page}>
      <h1 className={styles.title}>プロフィール編集</h1>
      {error && <ErrorMessage message={error} />}
      <form className={styles.form} onSubmit={handleSubmit}>
        <div className={styles.field}>
          <label className={styles.label} htmlFor="displayName">
            表示名
          </label>
          <input
            id="displayName"
            className={styles.input}
            type="text"
            value={displayName}
            onChange={(e) => setDisplayName(e.target.value)}
            maxLength={50}
            placeholder="表示名"
          />
        </div>

        <div className={styles.field}>
          <label className={styles.label} htmlFor="biography">
            自己紹介
          </label>
          <textarea
            id="biography"
            className={styles.textarea}
            value={biography}
            onChange={(e) => setBiography(e.target.value)}
            maxLength={1000}
            placeholder="自己紹介文を入力..."
          />
        </div>

        <div className={styles.field}>
          <label className={styles.label} htmlFor="websiteUrl">
            ウェブサイト
          </label>
          <input
            id="websiteUrl"
            className={styles.input}
            type="url"
            value={websiteUrl}
            onChange={(e) => setWebsiteUrl(e.target.value)}
            placeholder="https://example.com"
          />
        </div>

        <div className={styles.actions}>
          <Link to={`/users/${userId}`} className={styles.cancelButton}>
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
