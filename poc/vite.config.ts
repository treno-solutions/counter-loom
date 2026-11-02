import { defineConfig } from 'vite';
import tailwindcss from '@tailwindcss/vite';

export default defineConfig({
  plugins: [tailwindcss()],
  server: { host: '127.0.0.1', port: Number(process.env.COUNTERLOOM_WEB_PORT ?? 5173), strictPort: true, proxy: { '/api': `http://127.0.0.1:${process.env.COUNTERLOOM_API_PORT ?? 8765}` } },
});
