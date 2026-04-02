import { useState, useEffect, useCallback } from 'react'
import { novelsApi } from '../../api/novels'
import { commonApi } from '../../api/common'
import { NovelList } from '../../components/Novel/NovelList'
import { Pagination } from '../../components/Common/Pagination'
import { LoadingSpinner } from '../../components/Common/LoadingSpinner'
import { ErrorMessage } from '../../components/Common/ErrorMessage'
import type { Novel, Category } from '../../types'
import styles from './HomePage.module.css'

const LIMIT = 12

const SORT_OPTIONS = [
  { value: '-created_at', label: '新着順' },
  { value: '-updated_at', label: '更新順' },
  { value: 'created_at', label: '古い順' },
]

export function HomePage() {
  const [novels, setNovels] = useState<Novel[]>([])
  const [total, setTotal] = useState(0)
  const [offset, setOffset] = useState(0)
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const [searchInput, setSearchInput] = useState('')
  const [query, setQuery] = useState('')
  const [categoryId, setCategoryId] = useState<number | undefined>(undefined)
  const [sort, setSort] = useState('-created_at')
  const [categories, setCategories] = useState<Category[]>([])

  useEffect(() => {
    commonApi.getCategories().then((res) => setCategories(res.results)).catch(() => {})
  }, [])

  const fetchNovels = useCallback(async () => {
    setIsLoading(true)
    setError(null)
    try {
      const ordering = sort.startsWith('-') ? sort : sort
      const result = await novelsApi.getList({
        q: query || undefined,
        category: categoryId,
        sort: ordering,
        limit: LIMIT,
        offset,
      })
      setNovels(result.results)
      setTotal(result.count)
    } catch {
      setError('作品の取得に失敗しました。')
    } finally {
      setIsLoading(false)
    }
  }, [query, categoryId, sort, offset])

  useEffect(() => {
    fetchNovels()
  }, [fetchNovels])

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault()
    setQuery(searchInput)
    setOffset(0)
  }

  const handleCategoryChange = (id: number | undefined) => {
    setCategoryId(id)
    setOffset(0)
  }

  const handleSortChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    setSort(e.target.value)
    setOffset(0)
  }

  return (
    <div className={styles.page}>
      <div className={styles.hero}>
        <h1 className={styles.heroTitle}>
          文<span>の</span>蔵
        </h1>
        <p className={styles.heroSubtitle}>あなたの物語を、世界へ。</p>
        <form className={styles.searchForm} onSubmit={handleSearch}>
          <input
            className={styles.searchInput}
            type="text"
            placeholder="タイトル・キーワードで検索"
            value={searchInput}
            onChange={(e) => setSearchInput(e.target.value)}
          />
          <button type="submit" className={styles.searchButton}>
            検索
          </button>
        </form>
      </div>

      <div className={styles.controls}>
        <div className={styles.filterGroup}>
          <button
            className={`${styles.filterButton} ${categoryId === undefined ? styles.filterButtonActive : ''}`}
            onClick={() => handleCategoryChange(undefined)}
          >
            すべて
          </button>
          {categories.map((cat) => (
            <button
              key={cat.id}
              className={`${styles.filterButton} ${categoryId === cat.id ? styles.filterButtonActive : ''}`}
              onClick={() => handleCategoryChange(cat.id)}
            >
              {cat.name}
            </button>
          ))}
        </div>
        <select className={styles.sortSelect} value={sort} onChange={handleSortChange}>
          {SORT_OPTIONS.map((opt) => (
            <option key={opt.value} value={opt.value}>
              {opt.label}
            </option>
          ))}
        </select>
      </div>

      <div>
        <h2 className={styles.sectionTitle}>
          {query ? `「${query}」の検索結果` : '作品一覧'}
          {!isLoading && (
            <span className={styles.resultCount}> ({total}件)</span>
          )}
        </h2>

        {error && <ErrorMessage message={error} />}
        {isLoading ? (
          <LoadingSpinner />
        ) : (
          <>
            <NovelList novels={novels} />
            <Pagination
              total={total}
              limit={LIMIT}
              offset={offset}
              onChange={setOffset}
            />
          </>
        )}
      </div>
    </div>
  )
}
