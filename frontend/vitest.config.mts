import { defineConfig } from 'vitest/config'
import react from '@vitejs/plugin-react'

// Renderer unit tests: src/renderer/src/**/*.test.{ts,tsx}, jsdom instead of Electron.
export default defineConfig({
  plugins: [react()],
  test: {
    environment: 'jsdom',
    include: ['src/renderer/src/**/*.test.{ts,tsx}']
  }
})
