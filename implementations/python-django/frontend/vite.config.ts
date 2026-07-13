import { defineConfig, loadEnv } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), '')

  return {
    plugins: [react()],
    server: {
      host: '0.0.0.0',
      port: 3000,
      proxy: {
        '/api': {
          // Docker Compose 内では 'backend' サービス名で解決される。
          // Compose を使わずローカル単体起動する場合は .env.local で上書きする。
          target: env.VITE_API_URL || 'http://backend:8000',
          changeOrigin: true,
        },
      },
    },
  }
})
