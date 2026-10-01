"""Overlay computed profiles on Kato and Matsuda's published Figures 6 and 7."""

from __future__ import annotations

import shutil
import subprocess
import tempfile
from pathlib import Path

import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as np

from finite_difference import figure_6_finite_difference
from kato_matsuda import temperature
from .plot_figure7 import SURFACE_TEMPERATURES

PLOTS_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = PLOTS_DIR.parent
# Fractional pixel bounds (left, top, right, bottom) on PDF page 11.
FIGURE6_AXES_BOUNDS = (0.1165, 0.6950, 0.4610, 0.8770)
FIGURE7_AXES_BOUNDS = (0.5625, 0.7005, 0.9150, 0.8750)


def _render_page(pdf: Path, output_stem: Path, dpi: int) -> Path:
    executable = shutil.which("pdftoppm")
    if executable is None:
        raise RuntimeError("pdftoppm is required to rasterize the reference PDF")
    subprocess.run(
        [
            executable,
            "-f",
            "11",
            "-l",
            "11",
            "-singlefile",
            "-png",
            "-r",
            str(dpi),
            str(pdf),
            str(output_stem),
        ],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return output_stem.with_suffix(".png")


def _crop(page, bounds):
    height, width = page.shape[:2]
    left, top, right, bottom = bounds
    return page[
        round(top * height) : round(bottom * height),
        round(left * width) : round(right * width),
    ]


def _reference_crop(reference_pdf: Path, bounds, render_dpi: int):
    if not reference_pdf.is_file():
        raise FileNotFoundError(reference_pdf)
    with tempfile.TemporaryDirectory() as temporary:
        rendered = _render_page(
            reference_pdf, Path(temporary) / "kato-matsuda-page-11", render_dpi
        )
        return _crop(mpimg.imread(rendered), bounds).copy()


def generate_figure6_overlay(
    reference_pdf: str | Path = PROJECT_ROOT / "paper" / "kato-matsuda.pdf",
    output: str | Path = PLOTS_DIR / "figure6_overlay.png",
    *,
    render_dpi: int = 600,
) -> Path:
    reference_pdf, output = Path(reference_pdf), Path(output)
    reference = _reference_crop(reference_pdf, FIGURE6_AXES_BOUNDS, render_dpi)
    depths = np.linspace(0.0, 0.005, 401)
    analytical = np.array([temperature(depth) for depth in depths])
    finite_difference = figure_6_finite_difference()
    marker_depths = np.linspace(0.0, 0.005, 35)

    with plt.style.context(["default", str(PLOTS_DIR / "print.mplstyle")]):
        fig, ax = plt.subplots(figsize=(7.0, 5.0), layout="constrained")
        ax.imshow(
            reference,
            extent=(0.0, 0.005, 300.0, 1000.0),
            origin="upper",
            aspect="auto",
            alpha=0.62,
        )
        ax.plot(depths, analytical, color="#D55E00", linewidth=2.0, label="computed analytical")
        ax.plot(
            marker_depths,
            finite_difference.temperature_at(marker_depths),
            linestyle="none",
            marker="x",
            markersize=4,
            color="#0072B2",
            label="computed finite difference",
        )
        ax.set(
            xlim=(0.0, 0.005),
            ylim=(300.0, 1000.0),
            xlabel=r"Depth, $x$ (m)",
            ylabel=r"Temperature, $T$ (K)",
        )
        ax.legend(loc="upper right", frameon=True, facecolor="white")
        output.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(output, dpi=300)
        plt.close(fig)
    return output


def generate_figure7_overlay(
    reference_pdf: str | Path = PROJECT_ROOT / "paper" / "kato-matsuda.pdf",
    output: str | Path = PLOTS_DIR / "figure7_overlay.png",
    *,
    render_dpi: int = 600,
) -> Path:
    reference_pdf, output = Path(reference_pdf), Path(output)
    reference = _reference_crop(reference_pdf, FIGURE7_AXES_BOUNDS, render_dpi)
    depths = np.linspace(0.0, 0.002, 401)
    styles = {
        900.0: ("#0072B2", "--"),
        950.0: ("#D55E00", "-"),
        1000.0: ("#CC79A7", "-."),
    }

    with plt.style.context(["default", str(PLOTS_DIR / "print.mplstyle")]):
        fig, ax = plt.subplots(figsize=(7.0, 5.0), layout="constrained")
        ax.imshow(
            reference,
            extent=(0.0, 0.002, 300.0, 1000.0),
            origin="upper",
            aspect="auto",
            alpha=0.62,
        )
        for surface_temperature in SURFACE_TEMPERATURES:
            profile = np.array(
                [
                    temperature(depth, surface_temperature=surface_temperature)
                    for depth in depths
                ]
            )
            color, linestyle = styles[surface_temperature]
            ax.plot(
                depths,
                profile,
                color=color,
                linestyle=linestyle,
                linewidth=2.0,
                label=rf"computed $T_s={surface_temperature:.0f}$ K",
            )
        ax.set(
            xlim=(0.0, 0.002),
            ylim=(300.0, 1000.0),
            xlabel=r"Depth, $x$ (m)",
            ylabel=r"Temperature, $T$ (K)",
        )
        ax.legend(loc="lower left", frameon=True, facecolor="white")
        output.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(output, dpi=300)
        plt.close(fig)
    return output


if __name__ == "__main__":
    print(generate_figure6_overlay())
    print(generate_figure7_overlay())
