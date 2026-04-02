import { useState, useEffect } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { novelsApi } from '../../api/novels'
import { commonApi } from '../../api/common'
import { ErrorMessage } from '../../components/Common/ErrorMessage'
import { LoadingSpinner } from '../../components/Common/LoadingSpinner'
import type { Category } from '../../types'
import styles from './NovelCreatePage.module.css'

export function NovelCreatePage() {
  const navigate = useNavigate()

  const [title, setTitle] = useState('')
  const [synopsis, setSynopsis] = useState('')
  const [categoryId, setCategoryId] = useState<number | null>(null)
  const [isR18, setIsR18] = useState(false)

  const [categories, setCategories] = useState<Category[]>([])
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    commonApi.getCategories().then((res) => setCategories(res.results))
  }, [])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!title.trim()) {
      setError('タイトルを入力してください。')
      return
    }
    setError(null)
    setIsLoading(true)
    try {
      const novel = await novelsApi.create({
        category: categoryId,
        info: {
          title,
          synopsis,
          is_r18: isR18,
        },
      })
      navigate(`/novels/${novel.id}`)
    } catch (err: unknown) {
      const axiosError = err as { response?: { data?: Record<string, unknown> } }
      const data = axiosError.response?.data
      if (data) {
        const messages = Object.values(data).flat().join(' ')
        setError(String(messages) || '作品の作成に失敗しました。')
      } else {
        setError('作品の作成に失敗しました。')
      }
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className={styles.page}>
      <h1 className={styles.title}>作品を投稿</h1>
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
            placeholder="作品のタイトル"
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
            placeholder="作品のあらすじを入力..."
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
          <Link to="/" className={styles.cancelButton}>
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
