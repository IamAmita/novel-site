import { useState, useRef, useEffect } from 'react'
import { Link, NavLink, useNavigate } from 'react-router-dom'
import { useAuth } from '../../hooks/useAuth'
import styles from './Header.module.css'

export function Header() {
  const { user, isAuthenticated, logout } = useAuth()
  const navigate = useNavigate()
  const [menuOpen, setMenuOpen] = useState(false)
  const menuRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    function handleClickOutside(e: MouseEvent) {
      if (menuRef.current && !menuRef.current.contains(e.target as Node)) {
        setMenuOpen(false)
      }
    }
    document.addEventListener('mousedown', handleClickOutside)
    return () => document.removeEventListener('mousedown', handleClickOutside)
  }, [])

  const handleLogout = () => {
    logout()
    setMenuOpen(false)
    navigate('/')
  }

  return (
    <header className={styles.header}>
      <div className={styles.inner}>
        <Link to="/" className={styles.logo}>
          文<span>の</span>蔵
        </Link>

        <nav className={styles.nav}>
          <NavLink
            to="/"
            className={({ isActive }) =>
              `${styles.navLink} ${isActive ? styles.navLinkActive : ''}`
            }
            end
          >
            ホーム
          </NavLink>
        </nav>

        <div className={styles.actions}>
          {isAuthenticated ? (
            <>
              <Link to="/novels/create" className={styles.postButton}>
                投稿する
              </Link>
              <div className={styles.userMenu} ref={menuRef}>
                <button
                  className={styles.userButton}
                  onClick={() => setMenuOpen((v) => !v)}
                >
                  {user?.profile?.display_name || user?.username}
                  <span>{menuOpen ? '▲' : '▼'}</span>
                </button>
                {menuOpen && (
                  <div className={styles.dropdown}>
                    <Link
                      to={`/users/${user?.id}`}
                      className={styles.dropdownLink}
                      onClick={() => setMenuOpen(false)}
                    >
                      マイページ
                    </Link>
                    <Link
                      to={`/users/${user?.id}/edit`}
                      className={styles.dropdownLink}
                      onClick={() => setMenuOpen(false)}
                    >
                      プロフィール編集
                    </Link>
                    <div className={styles.dropdownDivider} />
                    <button className={styles.logoutButton} onClick={handleLogout}>
                      ログアウト
                    </button>
                  </div>
                )}
              </div>
            </>
          ) : (
            <div className={styles.authLinks}>
              <Link to="/login" className={styles.loginLink}>
                ログイン
              </Link>
              <Link to="/register" className={styles.registerLink}>
                新規登録
              </Link>
            </div>
          )}
        </div>
      </div>
    </header>
  )
}
