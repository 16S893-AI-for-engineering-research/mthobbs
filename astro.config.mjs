// @ts-check
import { defineConfig } from 'astro/config';
import tailwindcss from '@tailwindcss/vite';

export default defineConfig({
  site: 'https://16s893-ai-for-engineering-research.github.io',
  base: '/mthobbs/',
  vite: {
    plugins: [tailwindcss()],
  },
});
