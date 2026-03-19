import styles from './App.module.css'

function App() {
  return (
    <div className={styles.wrapper}>
      <header className={styles.header}>
        <div className={styles.headerInner}>
          <h1 className={styles.siteName}>小説投稿サイト</h1>
          <p className={styles.tagline}>あなたの物語を、世界へ。</p>
        </div>
      </header>

      <main className={styles.main}>
        <section className={styles.hero}>
          <div className={styles.heroContent}>
            <span className={styles.badge}>Python / Django 実装版</span>
            <h2 className={styles.heroTitle}>準備中</h2>
            <p className={styles.heroDescription}>
              小説投稿サイトを現在開発中です。<br />
              Django + React + PostgreSQL による実装です。
            </p>
            <div className={styles.techStack}>
              <span className={styles.tech}>Python 3.11</span>
              <span className={styles.tech}>Django 4</span>
              <span className={styles.tech}>React 18</span>
              <span className={styles.tech}>TypeScript</span>
              <span className={styles.tech}>PostgreSQL 15</span>
              <span className={styles.tech}>Redis</span>
            </div>
          </div>
        </section>
      </main>

      <footer className={styles.footer}>
        <p>小説投稿サイト — 学習プロジェクト</p>
      </footer>
    </div>
  )
}

export default App
