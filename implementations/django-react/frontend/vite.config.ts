import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// /api・/media はDjango(8000)へプロキシし、同一オリジンでセッションクッキーを使う
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/api': 'http://localhost:8000',
      '/media': 'http://localhost:8000',
    },
  },
})
