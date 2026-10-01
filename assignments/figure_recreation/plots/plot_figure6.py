"""Reproduce Kato and Matsuda (2022), Figure 6."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from finite_difference import figure_6_finite_difference
from kato_matsuda import TM, V, interface_depth, temperature

ROOT = Path(__file__).resolve().parent


def plot_figure_6(output: str | Path = ROOT / "figure6.png") -> float:
    """Generate the analytical/FDM comparison and return delta_m."""
    output = Path(output)
    delta = interface_depth()
    analytical_depth = np.linspace(0.0, 0.005, 401)
    analytical_temperature = np.array(
        [temperature(depth) for depth in analytical_depth]
    )
    finite_difference = figure_6_finite_difference()
    marker_depth = np.linspace(0.0, 0.005, 45)
    marker_temperature = finite_difference.temperature_at(marker_depth)

    with plt.style.context(["default", str(ROOT / "print.mplstyle")]):
        fig, ax = plt.subplots(figsize=(7.0, 5.0), layout="constrained")
        ax.plot(
            marker_depth,
            marker_temperature,
            linestyle="none",
            marker="o",
            markersize=4.8,
            markerfacecolor="none",
            markeredgecolor="#D55E00",
            markeredgewidth=0.9,
            label="Finite difference",
        )
        ax.plot(
            analytical_depth,
            analytical_temperature,
            color="#0072B2",
            label="Analytical solution",
        )
        ax.axvline(delta, color="0.25", linestyle=(0, (2, 2)), linewidth=0.9)
        ax.axhline(TM, xmin=0.0, xmax=delta / 0.005, color="0.65", linewidth=0.7)

        ax.annotate(
            r"$\delta_m$",
            xy=(delta / 2, 485),
            ha="center",
            fontsize=10,
        )
        ax.annotate(
            "Amorphous\nregion",
            xy=(delta / 2, 405),
            ha="center",
            va="center",
        )
        ax.annotate(
            "Crystalline region",
            xy=(0.00145, 405),
            ha="center",
            va="center",
        )
        ax.annotate(r"$T_m$", xy=(delta, TM), xytext=(delta + 0.00018, TM + 25))
        ax.text(
            0.00215,
            925,
            "Two-phase model (semi-infinite ablator)\n"
            r"$T_s=950$ K, $T_m=600$ K, $T_0=300$ K" "\n"
            r"$V=7.5545\times10^{-5}$ m/s",
            va="top",
        )
        ax.set(
            xlim=(0.0, 0.005),
            ylim=(300.0, 1000.0),
            xlabel=r"Depth, $x$ (m)",
            ylabel=r"Temperature, $T$ (K)",
        )
        ax.legend(loc="upper left", bbox_to_anchor=(0.03, 0.95))
        output.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(output, dpi=300)
        plt.close(fig)
    return delta


if __name__ == "__main__":
    layer_thickness = plot_figure_6()
    print(f"Wrote {ROOT / 'figure6.png'}")
    print(f"Amorphous layer thickness: {1e3 * layer_thickness:.6f} mm")
