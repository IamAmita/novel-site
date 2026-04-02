import type { Novel } from '../../types'
import { NovelCard } from './NovelCard'
import styles from './NovelList.module.css'

interface Props {
  novels: Novel[]
  emptyMessage?: string
}

export function NovelList({ novels, emptyMessage = '作品が見つかりませんでした。' }: Props) {
  if (novels.length === 0) {
    return <p className={styles.empty}>{emptyMessage}</p>
  }
  return (
    <div className={styles.grid}>
      {novels.map((novel) => (
        <NovelCard key={novel.id} novel={novel} />
      ))}
    </div>
  )
}
