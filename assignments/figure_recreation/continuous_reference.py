"""High-accuracy direct solve of the original quasi-steady differential equation."""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache

import numpy as np
from scipy.integrate import solve_bvp

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
class ContinuousReferenceSolution:
    interface: float
    amorphous_solution: object
    crystalline_solution: object

    def temperature_at(self, depth) -> np.ndarray:
        depth = np.asarray(depth, dtype=float)
        result = np.empty_like(depth)
        amorphous = depth <= self.interface
        result[amorphous] = self.amorphous_solution.sol(depth[amorphous])[0]
        result[~amorphous] = self.crystalline_solution.sol(
            depth[~amorphous] - self.interface
        )[0]
        return result


def _solve_region(
    *,
    length: float,
    left_temperature: float,
    right_temperature: float,
    properties: PolynomialProperties,
):
    coordinate = np.linspace(0.0, length, 121)
    midpoint = 0.5 * (left_temperature + right_temperature)
    decay = V * properties.rho(midpoint) * properties.cp(midpoint) / properties.k(
        midpoint
    )
    exponential = np.exp(-decay * coordinate)
    endpoint = exponential[-1]
    guess_temperature = right_temperature + (
        left_temperature - right_temperature
    ) * (exponential - endpoint) / (1.0 - endpoint)
    guess_flux = properties.k(guess_temperature) * np.gradient(
        guess_temperature, coordinate
    )

    def equations(_coordinate, state):
        temperature = state[0]
        conductive_gradient = state[1]
        derivative = conductive_gradient / properties.k(temperature)
        return np.vstack(
            (
                derivative,
                -properties.rho(temperature)
                * properties.cp(temperature)
                * V
                * derivative,
            )
        )

    def boundaries(left, right):
        return np.array(
            [left[0] - left_temperature, right[0] - right_temperature]
        )

    solution = solve_bvp(
        equations,
        boundaries,
        coordinate,
        np.vstack((guess_temperature, guess_flux)),
        tol=1e-8,
        max_nodes=50_000,
    )
    if not solution.success:
        raise RuntimeError(f"continuous reference solve failed: {solution.message}")
    return solution


@lru_cache(maxsize=None)
def two_phase_continuous_reference(
    surface_temperature: float = TS,
) -> ContinuousReferenceSolution:
    """Solve the differential equation independently for both material phases."""
    delta = interface_depth(surface_temperature=surface_temperature)
    amorphous = _solve_region(
        length=delta,
        left_temperature=surface_temperature,
        right_temperature=TM,
        properties=AMORPHOUS,
    )
    crystalline = _solve_region(
        length=0.05,
        left_temperature=TM,
        right_temperature=T0,
        properties=CRYSTALLINE,
    )
    return ContinuousReferenceSolution(delta, amorphous, crystalline)
