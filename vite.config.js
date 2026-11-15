import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import packageJson from './package.json' with { type: 'json' }

const buildVersion = (process.env.SANAD_BUILD_VERSION || packageJson.version).replace(/^v/, '')

export default defineConfig({
  plugins: [react()],
  define: {
    __SANAD_VERSION__: JSON.stringify(buildVersion),
    __SANAD_COMMIT__: JSON.stringify((process.env.GITHUB_SHA || process.env.SANAD_BUILD_COMMIT || 'local').slice(0, 12)),
  },
})
