import styles from './Pagination.module.css'

interface Props {
  total: number
  limit: number
  offset: number
  onChange: (offset: number) => void
}

export function Pagination({ total, limit, offset, onChange }: Props) {
  const currentPage = Math.floor(offset / limit) + 1
  const totalPages = Math.ceil(total / limit)

  if (totalPages <= 1) return null

  const pages: (number | '...')[] = []
  if (totalPages <= 7) {
    for (let i = 1; i <= totalPages; i++) pages.push(i)
  } else {
    pages.push(1)
    if (currentPage > 3) pages.push('...')
    for (let i = Math.max(2, currentPage - 1); i <= Math.min(totalPages - 1, currentPage + 1); i++) {
      pages.push(i)
    }
    if (currentPage < totalPages - 2) pages.push('...')
    pages.push(totalPages)
  }

  return (
    <div className={styles.pagination}>
      <button
        className={styles.button}
        disabled={currentPage === 1}
        onClick={() => onChange(offset - limit)}
      >
        ‹
      </button>
      {pages.map((p, i) =>
        p === '...' ? (
          <span key={`ellipsis-${i}`} className={styles.info}>
            …
          </span>
        ) : (
          <button
            key={p}
            className={`${styles.button} ${p === currentPage ? styles.buttonActive : ''}`}
            onClick={() => onChange((p - 1) * limit)}
          >
            {p}
          </button>
        )
      )}
      <button
        className={styles.button}
        disabled={currentPage === totalPages}
        onClick={() => onChange(offset + limit)}
      >
        ›
      </button>
    </div>
  )
}
