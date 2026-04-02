import { useState, useEffect } from 'react'
import { useNavigate, useParams, Link } from 'react-router-dom'
import { novelsApi } from '../../api/novels'
import { commonApi } from '../../api/common'
import { useAuth } from '../../hooks/useAuth'
import { LoadingSpinner } from '../../components/Common/LoadingSpinner'
import { ErrorMessage } from '../../components/Common/ErrorMessage'
import type { Category } from '../../types'
import styles from './NovelCreatePage.module.css'

export function NovelEditPage() {
  const { id } = useParams<{ id: string }>()
  const novelId = Number(id)
  const navigate = useNavigate()
  const { user } = useAuth()

  const [title, setTitle] = useState('')
  const [synopsis, setSynopsis] = useState('')
  const [categoryId, setCategoryId] = useState<number | null>(null)
  const [isR18, setIsR18] = useState(false)

  const [categories, setCategories] = useState<Category[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [isSaving, setIsSaving] = useState(false)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [novel, catsRes] = await Promise.all([
          novelsApi.getDetail(novelId),
          commonApi.getCategories(),
        ])
        if (user && user.id !== novel.user) {
          navigate(`/novels/${novelId}`)
          return
        }
        setTitle(novel.info.title)
        setSynopsis(novel.info.synopsis ?? '')
        setCategoryId(novel.category)
        setIsR18(novel.info.is_r18)
        setCategories(catsRes.results)
      } catch {
        setError('作品の取得に失敗しました。')
      } finally {
        setIsLoading(false)
      }
    }
    fetchData()
  }, [novelId, user, navigate])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError(null)
    setIsSaving(true)
    try {
      await novelsApi.update(novelId, {
        category: categoryId,
        info: { title, synopsis, is_r18: isR18 },
      })
      navigate(`/novels/${novelId}`)
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
      <h1 className={styles.title}>作品を編集</h1>
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
            maxLength={100}
          />
        </div>

        <div className={styles.field}>
          <label className={styles.label} htmlFor="synopsis">
            あらすじ
          </label>
          <textarea
            id="synopsis"
            className={styles.textarea}
            value={synopsis}
            onChange={(e) => setSynopsis(e.target.value)}
            maxLength={1000}
          />
        </div>

        <div className={styles.field}>
          <label className={styles.label} htmlFor="category">
            カテゴリ
          </label>
          <select
            id="category"
            className={styles.select}
            value={categoryId ?? ''}
            onChange={(e) => setCategoryId(e.target.value ? Number(e.target.value) : null)}
          >
            <option value="">選択なし</option>
            {categories.map((cat) => (
              <option key={cat.id} value={cat.id}>
                {cat.name}
              </option>
            ))}
          </select>
        </div>

        <div className={styles.field}>
          <label className={styles.checkboxLabel}>
            <input
              type="checkbox"
              checked={isR18}
              onChange={(e) => setIsR18(e.target.checked)}
            />
            成人向けコンテンツ（R-18）
          </label>
        </div>

        <div className={styles.actions}>
          <Link to={`/novels/${novelId}`} className={styles.cancelButton}>
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
