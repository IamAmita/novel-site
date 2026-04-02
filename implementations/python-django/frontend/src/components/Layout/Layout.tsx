import type { ReactNode } from 'react'
import { Header } from './Header'
import { Footer } from './Footer'
import styles from './Layout.module.css'

interface Props {
  children: ReactNode
}

export function Layout({ children }: Props) {
  return (
    <div className={styles.layout}>
      <Header />
      <main className={styles.main}>{children}</main>
      <Footer />
    </div>
  )
}
