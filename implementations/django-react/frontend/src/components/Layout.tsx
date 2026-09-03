import { Link, NavLink, Navigate, Outlet, useNavigate } from 'react-router-dom'
import { useAuth } from '../auth/AuthContext'

/** 上部固定ヘッダー＋コンテンツ（画面遷移-共通方針.md）。未ログインは /login へ */
export default function Layout() {
  const { user, loading, logout } = useAuth()
  const navigate = useNavigate()

  if (loading) return <div className="page-loading">読み込み中…</div>
  if (!user) return <Navigate to="/login" replace />

  const onLogout = async () => {
    try {
      await logout()
    } catch {
      alert('ログアウトに失敗しました。もう一度お試しください。')
      return
    }
    navigate('/login')
  }

  return (
    <div>
      <header className="app-header">
        <Link to="/worlds" className="logo">
          novel-site
        </Link>
        <nav>
          <NavLink to="/worlds">World一覧</NavLink>
          <NavLink to="/settings-list" className="nav-disabled" onClick={(e) => e.preventDefault()} title="未実装">
            設定一覧
          </NavLink>
          <NavLink to="/novels" className="nav-disabled" onClick={(e) => e.preventDefault()} title="未実装">
            作品一覧
          </NavLink>
        </nav>
        <div className="header-right">
          <NavLink to="/pennames">ペンネーム</NavLink>
          <NavLink to="/account">{user.username}</NavLink>
          <button className="link-button" onClick={onLogout}>
            ログアウト
          </button>
        </div>
      </header>
      <main className="app-main">
        <Outlet />
      </main>
    </div>
  )
}
