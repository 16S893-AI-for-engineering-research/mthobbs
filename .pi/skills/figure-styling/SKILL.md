---
name: figure-styling
description: Style Matplotlib figures for papers, theses, slides, and posters using consistent fonts, colours, sizing, and export settings. Use when creating or restyling a figure for publication or presentation, not for exploratory plots.
license: MIT
---

# Figure styling

Use the bundled styles as defaults. Preserve the data and analysis; change the
presentation. Requires Matplotlib.

## Choose a style

- `assets/print.mplstyle`: papers and theses — 7–9 pt text, 1 pt lines, no grid.
- `assets/screen.mplstyle`: slides and posters — larger text, 2 pt lines, light grid.

Both use an Okabe–Ito colour cycle and sans-serif fonts with fallbacks. Resolve
asset paths relative to this `SKILL.md`, not the working directory. Copy the chosen
style into the project alongside the plotting script so it can run independently.

## Apply it

Set the figure dimensions before plotting. For papers, check the publication's
current column widths; for slides and posters, size for the intended placement.
If the destination is unknown, ask. Adjust height to fit the panels and labels.

This example assumes `print.mplstyle` is beside the script. Replace the sample
data and 90 × 65 mm dimensions with the project's data and target size.

```python
from pathlib import Path
import matplotlib.pyplot as plt

style = Path(__file__).resolve().parent / "print.mplstyle"
with plt.style.context(["default", str(style)]):
    fig, ax = plt.subplots(figsize=(90 / 25.4, 65 / 25.4), layout="constrained")
    ax.plot([0, 1, 2], [0, 1, 4], marker="o")
    ax.set(xlabel="Time (s)", ylabel="Displacement (m)")
    fig.savefig("figure.pdf")
    fig.savefig("figure.png", dpi=300)
    plt.close(fig)
```

The context starts from Matplotlib defaults and restores prior settings afterward.
Keep creation and export inside it. Avoid `bbox_inches="tight"` when exact output
dimensions matter: cropping changes the saved size.

## Check before exporting

- Label axes with quantities and units. Use a legend when series need identifying.
- Distinguish series with markers or line patterns as well as colour.
- Use `viridis` or `cividis` for ordered values; use a diverging map such as `RdBu_r`
  centred on zero when deviations from zero matter. Avoid rainbow maps for ordered data.
- Put manuscript titles in the caption; titles are useful on slides. Label panels
  `(a)`, `(b)`, etc. when the caption refers to them.
- Save PDF for vector graphics and PNG for previews or slides. Follow the venue's
  format and raster-resolution requirements; 300 dpi is a starting point.
- Inspect the export at its final display size for clipped labels, overlaps, and
  unreadable text. Enlarge screen-style text if the placement requires it.
- Keep the plotting script, style, and data source or retrieval instructions together.
