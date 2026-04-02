import { useState, useEffect } from 'react'
import { useParams, Link } from 'react-router-dom'
import { usersApi } from '../../api/users'
import { useAuth } from '../../hooks/useAuth'
import { NovelList } from '../../components/Novel/NovelList'
import { LoadingSpinner } from '../../components/Common/LoadingSpinner'
import { ErrorMessage } from '../../components/Common/ErrorMessage'
import type { User, Novel } from '../../types'
import styles from './ProfilePage.module.css'

export function ProfilePage() {
  const { id } = useParams<{ id: string }>()
  const userId = Number(id)
  const { user: currentUser, isAuthenticated } = useAuth()

  const [profile, setProfile] = useState<User | null>(null)
  const [novels, setNovels] = useState<Novel[]>([])
  const [followerCount, setFollowerCount] = useState(0)
  const [followingCount, setFollowingCount] = useState(0)
  const [isFollowing, setIsFollowing] = useState(false)
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [followLoading, setFollowLoading] = useState(false)

  useEffect(() => {
    const fetchData = async () => {
      setIsLoading(true)
      setError(null)
      try {
        const [profileData, novelsData, counts] = await Promise.all([
          usersApi.getUser(userId),
          usersApi.getUserNovels(userId),
          usersApi.getFollowCount(userId),
        ])
        setProfile(profileData)
        setNovels(novelsData.results)
        setFollowerCount(counts.followers)
        setFollowingCount(counts.following)

        if (isAuthenticated && currentUser && currentUser.id !== userId) {
          const following = await usersApi.isFollowing(currentUser.id, userId)
          setIsFollowing(following)
        }
      } catch {
        setError('ユーザー情報の取得に失敗しました。')
      } finally {
        setIsLoading(false)
      }
    }
    fetchData()
  }, [userId, isAuthenticated, currentUser])

  const handleFollow = async () => {
    if (!profile) return
    setFollowLoading(true)
    try {
      if (isFollowing) {
        await usersApi.unfollow(userId)
        setIsFollowing(false)
        setFollowerCount((c) => c - 1)
      } else {
        await usersApi.follow(userId)
        setIsFollowing(true)
        setFollowerCount((c) => c + 1)
      }
    } catch {
      /* ignore */
    } finally {
      setFollowLoading(false)
    }
  }

  if (isLoading) return <LoadingSpinner />
  if (error) return <ErrorMessage message={error} title="エラー" />
  if (!profile) return null

  const isOwnProfile = currentUser?.id === userId
  const displayName = profile.profile?.display_name || profile.username
  const initial = displayName.charAt(0).toUpperCase()

  return (
    <div className={styles.page}>
      <div className={styles.profileCard}>
        <div className={styles.avatar}>
          {profile.profile?.icon_url ? (
            <img src={profile.profile.icon_url} alt={displayName} className={styles.avatarImg} />
          ) : (
            initial
          )}
        </div>
        <div className={styles.profileInfo}>
          <h1 className={styles.displayName}>{displayName}</h1>
          <p className={styles.username}>@{profile.username}</p>
          {profile.profile?.biography && (
            <p className={styles.bio}>{profile.profile.biography}</p>
          )}
          <div className={styles.stats}>
            <span className={styles.stat}>
              <strong>{followerCount}</strong> フォロワー
            </span>
            <span className={styles.stat}>
              <strong>{followingCount}</strong> フォロー中
            </span>
            <span className={styles.stat}>
              <strong>{novels.length}</strong> 作品
            </span>
          </div>
          <div className={styles.profileActions}>
            {isOwnProfile ? (
              <Link to={`/users/${userId}/edit`} className={styles.editProfileLink}>
                プロフィールを編集
              </Link>
            ) : isAuthenticated ? (
              <button
                className={isFollowing ? styles.unfollowButton : styles.followButton}
                onClick={handleFollow}
                disabled={followLoading}
              >
                {isFollowing ? 'フォロー解除' : 'フォローする'}
              </button>
            ) : null}
          </div>
        </div>
      </div>

      <div className={styles.section}>
        <h2 className={styles.sectionTitle}>投稿作品</h2>
        <NovelList novels={novels} emptyMessage="まだ作品が投稿されていません。" />
      </div>
    </div>
  )
}
