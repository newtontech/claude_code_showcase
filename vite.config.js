import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  base: '/new_web/',  // GitHub Pages 仓库名作为基础路径
  server: {
    port: 3000,
    open: true
  }
})
