import styles from './LoadingSpinner.module.css'

interface Props {
  inline?: boolean
}

export function LoadingSpinner({ inline }: Props) {
  if (inline) {
    return <span className={styles.inline} />
  }
  return (
    <div className={styles.wrapper}>
      <div className={styles.spinner} />
    </div>
  )
}
