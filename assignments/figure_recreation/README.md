# Kato and Matsuda (2022), Figures 6 and 7

This project reproduces Figures 6 and 7 from Kato and Matsuda's analytical
model for one-dimensional, quasi-steady, non-charring Teflon ablation. The
calculation includes amorphous and crystalline material regions,
temperature-dependent properties, surface recession, and latent heat at the
phase interface.

The original paper is stored in `paper/kato-matsuda.pdf`.

## Directory layout

```text
figure_recreation/
├── paper/
│   └── kato-matsuda.pdf
├── plots/
│   ├── plot_figure6.py
│   ├── plot_figure7.py
│   ├── plot_paper_overlays.py
│   ├── print.mplstyle
│   ├── figure6.png
│   ├── figure7.png
│   ├── figure6_overlay.png
│   └── figure7_overlay.png
├── tests/
│   └── test_*.py
├── writeup/
│   ├── derivation.tex
│   ├── references.bib
│   └── derivation.pdf
├── kato_matsuda.py
├── finite_difference.py
├── continuous_reference.py
├── symbolic_derivation.py
├── compare_solutions.py
├── comparison_metrics.json
├── pyproject.toml
└── uv.lock
```

Only automated pytest files are kept in `tests/`. Plotting scripts, styles, and
figure outputs are grouped in `plots/`. The LaTeX source and compiled report
are grouped in `writeup/`. The three calculation modules remain in the project
root so the organization stays similar to the flat class example rather than
becoming an installable Python package.

## Set up the environment

Run these commands from `figure_recreation/`:

```bash
uv sync
```

`uv` reads `pyproject.toml` and `uv.lock` and creates the local environment.
The project is configured with `package = false`; it is a reproducibility
project, not an installed library.

## Run the tests

```bash
uv run pytest
```

The tests check the material-property ranges, boundary conditions,
phase-interface heat balance, constant-property limit, velocity--length
scaling, Figure 7 curve ordering, numerical error bounds, symbolic identities,
and generation of both figures and overlays.

## Reproduce the calculations and figures

```bash
uv run python symbolic_derivation.py
uv run python compare_solutions.py
uv run python -m plots.plot_figure6
uv run python -m plots.plot_figure7
uv run python -m plots.plot_paper_overlays
```

The overlay command also requires `pdftoppm` from Poppler. The generated error
metrics are written to `comparison_metrics.json`.

## Build the write-up

From `figure_recreation/`:

```bash
cd writeup
latexmk -pdf -interaction=nonstopmode -halt-on-error derivation.tex
cd ..
```

The report is written to `writeup/derivation.pdf`. `latexmk` also runs BibTeX
using the separate `writeup/references.bib` database.

## Calculation paths

`kato_matsuda.py` evaluates the analytical integral solution. The calculated
amorphous-layer thickness for Figure 6 is `0.637199 mm`, compared with the
paper's rounded value of `0.64 mm`.

`finite_difference.py` independently discretizes the original quasi-steady
energy equation. Across Figure 6, its maximum difference from the analytical
solution is `0.07535 K`, with an RMSE of `0.00813 K`.

`continuous_reference.py` directly solves the original differential equation
with adaptive collocation. Its maximum Figure 6 difference from the analytical
solution is approximately `8.6e-9 K`, consistent with the requested numerical
solver tolerance.

For Figure 7, the calculated amorphous-layer thicknesses are:

| Surface temperature | Layer thickness |
|---:|---:|
| 900 K | 0.600428 mm |
| 950 K | 0.637199 mm |
| 1000 K | 0.665689 mm |

Passing tests verify the derivation and implementation of this model. They do
not validate the quasi-steady or non-charring assumptions for a particular
flight or test environment.

## Reference

S. Kato and S. Matsuda, “Analytical solution for the problem of
one-dimensional quasi-steady non-charring ablation in a semi-infinite solid
with temperature-dependent thermo-physical properties,” *Thermal Science and
Engineering Progress*, vol. 31, 101181, 2022.
<https://doi.org/10.1016/j.tsep.2021.101181>
