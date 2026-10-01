"""Quantify analytical, finite-difference, and direct ODE agreement."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from functools import lru_cache
import json
from pathlib import Path

import numpy as np

from continuous_reference import two_phase_continuous_reference
from finite_difference import two_phase_finite_difference
from kato_matsuda import interface_depth, temperature

ROOT = Path(__file__).resolve().parent


@dataclass(frozen=True)
class ErrorMetrics:
    max_absolute_K: float
    rmse_K: float
    max_relative_percent: float
    normalized_rmse_percent: float


def calculate_error_metrics(candidate, reference) -> ErrorMetrics:
    candidate = np.asarray(candidate, dtype=float)
    reference = np.asarray(reference, dtype=float)
    error = candidate - reference
    span = float(np.max(reference) - np.min(reference))
    return ErrorMetrics(
        max_absolute_K=float(np.max(np.abs(error))),
        rmse_K=float(np.sqrt(np.mean(error**2))),
        max_relative_percent=float(np.max(np.abs(error) / np.abs(reference)) * 100.0),
        normalized_rmse_percent=float(np.sqrt(np.mean(error**2)) / span * 100.0),
    )


@lru_cache(maxsize=None)
def compare_case(
    *, surface_temperature: float, maximum_depth: float, points: int = 501
) -> dict[str, ErrorMetrics]:
    depths = np.linspace(0.0, maximum_depth, points)
    analytical = np.array(
        [
            temperature(depth, surface_temperature=surface_temperature)
            for depth in depths
        ]
    )
    finite_difference = two_phase_finite_difference(
        surface_temperature=surface_temperature
    ).temperature_at(depths)
    continuous = two_phase_continuous_reference(surface_temperature).temperature_at(
        depths
    )
    return {
        "finite_difference": calculate_error_metrics(
            finite_difference, analytical
        ),
        "continuous_reference": calculate_error_metrics(continuous, analytical),
    }


def generate_report(output: str | Path = ROOT / "comparison_metrics.json") -> Path:
    output = Path(output)
    cases = {
        "figure6_Ts_950K": compare_case(
            surface_temperature=950.0, maximum_depth=0.005
        ),
        "figure7_Ts_900K": compare_case(
            surface_temperature=900.0, maximum_depth=0.002
        ),
        "figure7_Ts_950K": compare_case(
            surface_temperature=950.0, maximum_depth=0.002
        ),
        "figure7_Ts_1000K": compare_case(
            surface_temperature=1000.0, maximum_depth=0.002
        ),
    }
    payload = {
        "description": (
            "Errors use the analytical quadrature solution as the reference. "
            "Relative error uses absolute temperature in kelvin; normalized RMSE "
            "uses the temperature span sampled in each case."
        ),
        "interface_depth": {
            "computed_mm": interface_depth() * 1e3,
            "paper_rounded_mm": 0.64,
            "literal_percent_difference": abs(interface_depth() * 1e3 - 0.64)
            / 0.64
            * 100.0,
        },
        "cases": {
            name: {method: asdict(metrics) for method, metrics in comparisons.items()}
            for name, comparisons in cases.items()
        },
    }
    output.write_text(json.dumps(payload, indent=2) + "\n")
    return output


if __name__ == "__main__":
    report = generate_report()
    print(report.read_text())
