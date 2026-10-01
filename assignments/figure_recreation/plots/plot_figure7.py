"""Reproduce Kato and Matsuda (2022), Figure 7."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from kato_matsuda import TM, V, interface_depth, temperature

ROOT = Path(__file__).resolve().parent
SURFACE_TEMPERATURES = (900.0, 950.0, 1000.0)


def figure_7_profiles(points: int = 401):
    depths = np.linspace(0.0, 0.002, points)
    profiles = {
        surface_temperature: np.array(
            [
                temperature(depth, surface_temperature=surface_temperature)
                for depth in depths
            ]
        )
        for surface_temperature in SURFACE_TEMPERATURES
    }
    return depths, profiles


def plot_figure_7(output: str | Path = ROOT / "figure7.png") -> tuple[float, ...]:
    output = Path(output)
    depths, profiles = figure_7_profiles()
    styles = {
        1000.0: {"color": "#D55E00", "linestyle": "-.", "label": r"$T_s=1000$ K"},
        950.0: {"color": "black", "linestyle": "-", "label": r"$T_s=950$ K"},
        900.0: {"color": "#0072B2", "linestyle": "--", "label": r"$T_s=900$ K"},
    }

    with plt.style.context(["default", str(ROOT / "print.mplstyle")]):
        fig, ax = plt.subplots(figsize=(7.0, 5.0), layout="constrained")
        for surface_temperature in (1000.0, 950.0, 900.0):
            ax.plot(depths, profiles[surface_temperature], **styles[surface_temperature])
        ax.axhline(TM, color="#56B4E9", linestyle="--", linewidth=1.0)
        ax.text(0.0010, TM + 18.0, r"$T_m$", ha="center")
        ax.text(
            0.00038,
            870.0,
            r"$V=7.5545\times10^{-5}$ m/s",
            ha="left",
        )
        ax.set(
            xlim=(0.0, 0.002),
            ylim=(300.0, 1000.0),
            xlabel=r"Depth, $x$ (m)",
            ylabel=r"Temperature, $T$ (K)",
        )
        ax.legend(loc="upper right")
        output.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(output, dpi=300)
        plt.close(fig)

    return tuple(
        interface_depth(surface_temperature=value) for value in SURFACE_TEMPERATURES
    )


if __name__ == "__main__":
    thicknesses = plot_figure_7()
    print(f"Wrote {ROOT / 'figure7.png'}")
    for surface_temperature, thickness in zip(SURFACE_TEMPERATURES, thicknesses):
        print(f"Ts={surface_temperature:.0f} K: delta_m={1e3 * thickness:.6f} mm")
