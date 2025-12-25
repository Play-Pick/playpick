import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'

// https://vite.dev/config/
export default defineConfig(({ mode }) => ({
  plugins: [
    vue(),
    vueDevTools(),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    },
  },
  // 👇 [추가 1] 빌드 설정
  build: {
    outDir: 'dist', // 빌드 결과물이 나올 폴더 (Vercel 기본값)
    emptyOutDir: true, // 빌드할 때마다 기존 dist 폴더 깨끗이 비우기
  },
  // 👇 [추가 2] 배포 모드일 때만 console.log와 debugger 제거
  esbuild: {
    drop: mode === 'production' ? ['console', 'debugger'] : [],
  },
}))