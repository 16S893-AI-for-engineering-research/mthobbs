# mthobbs / 16.S893

**AI-assisted CFD meshing and validation for high-fidelity hypersonic simulations.**

A personal research portfolio for **MIT 16.S893 · AI Agents for Engineering
Research** by Madison T. Hobbs. The project considers an AI-assisted
Pointwise Glyph workflow for generating, qualifying, and systematically
refining CFD meshes—while keeping human engineering review gates in the loop.

[Live site ↗](https://16s893-ai-for-engineering-research.github.io/mthobbs/)

---

## / site map

| Location | Contents |
| --- | --- |
| `src/pages/index.astro` | Project overview |
| `src/pages/project.astro` | Problem, workflow, evaluation approach, and data boundaries |
| `src/pages/about.astro` | Background, research interests, and small interactive details |
| `src/pages/dev-log/index.astro` | Notes on developing the project and using AI tools |
| `src/layouts/BaseLayout.astro` | Shared navigation, page metadata, and footer |
| `src/styles/global.css` | Global styles and Tailwind imports |
| `assignments/one_pager/` | Project one-pager: LaTeX source and PDF |

## / work locally

**Requires:** Node.js 22.

```sh
npm install
npm run dev
```

Astro will print a local address, normally
`http://localhost:4321/mthobbs/`.

For a production build and local preview:

```sh
npm run build
npm run preview
```

`dist/` is generated output and is not committed.

## / deployment

Pushing to `main` builds and deploys the site to GitHub Pages through
[`.github/workflows/deploy.yml`](.github/workflows/deploy.yml).

## / public-data boundary

This is a public course repository. No export-controlled geometries, data, simulations, or results will be used or published. 
