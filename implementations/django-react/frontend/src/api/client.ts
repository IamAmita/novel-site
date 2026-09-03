/** DRFセッション認証用の薄いfetchラッパー。CSRFトークンをクッキーから読んで付与する */

function getCookie(name: string): string | null {
  const m = document.cookie.match(new RegExp(`(?:^|; )${name}=([^;]*)`))
  return m ? decodeURIComponent(m[1]) : null
}

export class ApiError extends Error {
  status: number
  body: Record<string, unknown>
  constructor(status: number, body: Record<string, unknown>) {
    super(`API error ${status}`)
    this.status = status
    this.body = body
  }
  /** フィールドごとのエラーを「1行のメッセージ」に潰す */
  firstMessage(): string {
    for (const v of Object.values(this.body)) {
      if (typeof v === 'string') return v
      if (Array.isArray(v) && v.length > 0) return String(v[0])
    }
    return '保存に失敗しました。'
  }
}

const CSRF_COOKIE_NAME = 'novelsite_csrftoken'

function isCsrfFailure(status: number, body: Record<string, unknown>): boolean {
  return status === 403 && typeof body.detail === 'string' && body.detail.includes('CSRF')
}

async function request<T>(method: string, url: string, body?: unknown, retried = false): Promise<T> {
  const headers: Record<string, string> = {}
  let payload: BodyInit | undefined
  if (body instanceof FormData) {
    payload = body
  } else if (body !== undefined) {
    headers['Content-Type'] = 'application/json'
    payload = JSON.stringify(body)
  }
  if (method !== 'GET') {
    headers['X-CSRFToken'] = getCookie(CSRF_COOKIE_NAME) ?? ''
  }
  const res = await fetch(url, { method, headers, body: payload, credentials: 'same-origin' })
  if (res.status === 204) return undefined as T
  const data = await res.json().catch(() => ({}))
  if (!res.ok) {
    // CSRFトークンのずれはクッキーを取り直して1回だけ自動リトライ
    if (isCsrfFailure(res.status, data) && !retried) {
      await ensureCsrf()
      return request<T>(method, url, body, true)
    }
    throw new ApiError(res.status, data)
  }
  return data as T
}

export const api = {
  get: <T>(url: string) => request<T>('GET', url),
  post: <T>(url: string, body?: unknown) => request<T>('POST', url, body),
  patch: <T>(url: string, body?: unknown) => request<T>('PATCH', url, body),
  delete: <T = void>(url: string) => request<T>('DELETE', url),
}

export function ensureCsrf(): Promise<unknown> {
  return api.get('/api/auth/csrf/')
}
