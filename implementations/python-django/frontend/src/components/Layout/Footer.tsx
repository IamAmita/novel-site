import { Link } from 'react-router-dom'
import styles from './Footer.module.css'

export function Footer() {
  return (
    <footer className={styles.footer}>
      <div className={styles.inner}>
        <div className={styles.logo}>
          文<span>の</span>蔵
        </div>
        <nav className={styles.links}>
          <Link to="/" className={styles.link}>
            ホーム
          </Link>
          <Link to="/novels/create" className={styles.link}>
            作品を投稿
          </Link>
        </nav>
        <p className={styles.copy}>© 2026 文の蔵 — 学習プロジェクト</p>
      </div>
    </footer>
  )
}
