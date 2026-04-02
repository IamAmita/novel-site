import { Link } from 'react-router-dom'
import styles from './NotFoundPage.module.css'

export function NotFoundPage() {
  return (
    <div className={styles.page}>
      <div className={styles.code}>404</div>
      <h1 className={styles.title}>ページが見つかりません</h1>
      <p className={styles.description}>
        お探しのページは存在しないか、削除された可能性があります。
      </p>
      <Link to="/" className={styles.homeLink}>
        ホームへ戻る
      </Link>
    </div>
  )
}
