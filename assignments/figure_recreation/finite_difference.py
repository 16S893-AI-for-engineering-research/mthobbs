"""Independent conservative finite-difference reference for Figure 6."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy.optimize import root

from kato_matsuda import (
    AMORPHOUS,
    CRYSTALLINE,
    PolynomialProperties,
    TM,
    TS,
    T0,
    V,
    interface_depth,
)


@dataclass(frozen=True)
class FiniteDifferenceSolution:
    amorphous_depth: np.ndarray
    amorphous_temperature: np.ndarray
    crystalline_depth: np.ndarray
    crystalline_temperature: np.ndarray

    def temperature_at(self, depth) -> np.ndarray:
        """Interpolate the two finite-difference regions on global depth."""
        depth = np.asarray(depth, dtype=float)
        delta = self.amorphous_depth[-1]
        result = np.empty_like(depth)
        in_amorphous = depth <= delta
        result[in_amorphous] = np.interp(
            depth[in_amorphous],
            self.amorphous_depth,
            self.amorphous_temperature,
        )
        result[~in_amorphous] = np.interp(
            depth[~in_amorphous],
            self.crystalline_depth,
            self.crystalline_temperature,
        )
        return result


def _solve_region(
    *,
    length: float,
    left_temperature: float,
    right_temperature: float,
    properties: PolynomialProperties,
    nodes: int,
) -> tuple[np.ndarray, np.ndarray]:
    """Solve the quasi-steady equation with a three-point conservative stencil."""
    if nodes < 3:
        raise ValueError("at least three finite-difference nodes are required")
    coordinate = np.linspace(0.0, length, nodes)
    spacing = coordinate[1]
    midpoint_temperature = 0.5 * (left_temperature + right_temperature)
    decay = (
        V
        * properties.rho(midpoint_temperature)
        * properties.cp(midpoint_temperature)
        / properties.k(midpoint_temperature)
    )
    exponential = np.exp(-decay * coordinate)
    far_exponential = exponential[-1]
    initial = right_temperature + (left_temperature - right_temperature) * (
        exponential - far_exponential
    ) / (1.0 - far_exponential)

    scale = (
        properties.k(midpoint_temperature)
        * abs(left_temperature - right_temperature)
        / spacing**2
    )

    def residual(interior: np.ndarray) -> np.ndarray:
        values = np.concatenate(([left_temperature], interior, [right_temperature]))
        center = values[1:-1]
        conductivity = properties.k(values)
        k_left = 0.5 * (conductivity[:-2] + conductivity[1:-1])
        k_right = 0.5 * (conductivity[1:-1] + conductivity[2:])
        diffusion = (
            k_right * (values[2:] - center)
            - k_left * (center - values[:-2])
        ) / spacing**2
        advection = (
            properties.rho(center)
            * properties.cp(center)
            * V
            * (values[2:] - values[:-2])
            / (2.0 * spacing)
        )
        return (diffusion + advection) / scale

    solved = root(
        residual,
        initial[1:-1],
        method="hybr",
        options={"band": (1, 1), "xtol": 1e-10},
    )
    if not solved.success:
        raise RuntimeError(f"finite-difference solve failed: {solved.message}")
    temperature = np.concatenate(
        ([left_temperature], solved.x, [right_temperature])
    )
    return coordinate, temperature


def two_phase_finite_difference(
    *,
    surface_temperature: float = TS,
    amorphous_nodes: int = 81,
    crystalline_nodes: int = 1001,
) -> FiniteDifferenceSolution:
    """Compute an independent finite-difference two-phase temperature profile."""
    delta = interface_depth(surface_temperature=surface_temperature)
    amorphous_x, amorphous_temperature = _solve_region(
        length=delta,
        left_temperature=surface_temperature,
        right_temperature=TM,
        properties=AMORPHOUS,
        nodes=amorphous_nodes,
    )
    crystalline_z, crystalline_temperature = _solve_region(
        length=0.05,
        left_temperature=TM,
        right_temperature=T0,
        properties=CRYSTALLINE,
        nodes=crystalline_nodes,
    )
    return FiniteDifferenceSolution(
        amorphous_depth=amorphous_x,
        amorphous_temperature=amorphous_temperature,
        crystalline_depth=delta + crystalline_z,
        crystalline_temperature=crystalline_temperature,
    )


def figure_6_finite_difference(
    *, amorphous_nodes: int = 81, crystalline_nodes: int = 1001
) -> FiniteDifferenceSolution:
    """Compute the independent finite-difference reference shown in Figure 6."""
    return two_phase_finite_difference(
        surface_temperature=TS,
        amorphous_nodes=amorphous_nodes,
        crystalline_nodes=crystalline_nodes,
    )
