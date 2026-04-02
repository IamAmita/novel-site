import { Link } from 'react-router-dom'
import type { Novel } from '../../types'
import styles from './NovelCard.module.css'

interface Props {
  novel: Novel
}

export function NovelCard({ novel }: Props) {
  const authorName = novel.author.profile?.display_name || novel.author.username

  return (
    <Link to={`/novels/${novel.id}`} className={styles.card}>
      <div className={styles.header}>
        <h3 className={styles.title}>{novel.info.title}</h3>
        {novel.info.is_r18 && <span className={styles.r18}>R18</span>}
      </div>

      <p className={styles.author}>
        作者：
        <Link
          to={`/users/${novel.author.id}`}
          onClick={(e) => e.stopPropagation()}
        >
          {authorName}
        </Link>
      </p>

      {novel.info.synopsis && (
        <p className={styles.summary}>{novel.info.synopsis}</p>
      )}

      <div className={styles.tags}>
        {novel.category_detail && (
          <span className={styles.category}>{novel.category_detail.name}</span>
        )}
        {novel.tags.slice(0, 4).map((tag) => (
          <span key={tag.id} className={styles.tag}>
            #{tag.name}
          </span>
        ))}
      </div>

      <div className={styles.footer}>
        <span className={styles.stat}>📖 {novel.episode_count}話</span>
        <span className={styles.stat}>
          {new Date(novel.updated_at).toLocaleDateString('ja-JP')}
        </span>
      </div>
    </Link>
  )
}
