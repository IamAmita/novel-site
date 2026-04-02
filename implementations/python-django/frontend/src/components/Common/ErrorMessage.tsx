import styles from './ErrorMessage.module.css'

interface Props {
  message: string
  title?: string
}

export function ErrorMessage({ message, title }: Props) {
  return (
    <div className={styles.error}>
      {title && <p className={styles.title}>{title}</p>}
      <p>{message}</p>
    </div>
  )
}
