# Project instructions

## Purpose

This is Madison T. Hobbs's public portfolio for MIT 16.S893: AI Agents for
Engineering Research. It is an Astro static site deployed to GitHub Pages.

## Working conventions

- Keep the site accessible: retain meaningful alt text, semantic HTML, and
  keyboard-operable interactive controls.
- Preserve the existing Astro + Tailwind approach and the shared layout in
  `src/layouts/BaseLayout.astro`.
- Use asset imports from `src/assets/` for images used by Astro pages.
- Do not add proprietary, employer-owned, sensitive, or export-controlled
  data, geometries, simulations, or results. Public-facing research claims
  should be supportable by public sources.
- Do not commit generated files in `dist/`, `.astro/`, `node_modules/`, or
  LaTeX build artifacts. The PDF and `.tex` source in `assignments/one_pager/`
  are intentional project materials.

## Local development and validation

Use a background development server only when live browser testing is useful;
do not leave one running unnecessarily:

```sh
npm run dev -- --background
npx astro dev status
npx astro dev logs
npx astro dev stop
```

After changing site code or configuration, run:

```sh
npm run build
```

The deployment workflow in `.github/workflows/deploy.yml` publishes the site
from `main` to GitHub Pages.

## Astro references

Consult the relevant Astro documentation before unfamiliar framework changes:

- [Routing](https://docs.astro.build/en/guides/routing/) for pages, routes, or middleware.
- [Astro components](https://docs.astro.build/en/basics/astro-components/) for component syntax and props.
- [Styling](https://docs.astro.build/en/guides/styling/) for CSS or Tailwind changes.

Do not add a UI-framework integration, content collection, or internationalization
configuration unless the requested change actually requires it.
