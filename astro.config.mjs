// @ts-check
import { defineConfig } from 'astro/config';
import tailwindcss from '@tailwindcss/vite';

const base = process.env.NODE_ENV === 'production' ? '/mthobbs/' : '/';

export default defineConfig({
  site: 'https://16s893-ai-for-engineering-research.github.io',
  base,
  vite: {
    plugins: [tailwindcss()],
  },
});
