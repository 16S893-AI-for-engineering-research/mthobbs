"""Kato and Matsuda (2022) quasi-steady two-phase Teflon model.

The implementation uses the general integral solution in equations (3.2-6) and
(3.2-13)--(3.2-15).  It deliberately does not encode digitized points from
Figure 6.
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache

import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq

T0 = 300.0
TM = 600.0
TS = 950.0
V = 7.5545e-5
HM = 58_615.0


@dataclass(frozen=True)
class PolynomialProperties:
    """Temperature-polynomial properties, with coefficients in ascending order."""

    conductivity: tuple[float, ...]
    specific_heat: tuple[float, ...]
    density: tuple[float, ...]

    def k(self, temperature):
        return np.polynomial.polynomial.polyval(temperature, self.conductivity)

    def cp(self, temperature):
        return np.polynomial.polynomial.polyval(temperature, self.specific_heat)

    def rho(self, temperature):
        return np.polynomial.polynomial.polyval(temperature, self.density)

    def volumetric_enthalpy(self, lower: float, upper: float) -> float:
        """Return integral rho(T)*Cp(T) dT in J/m^3."""
        coefficients = np.polynomial.polynomial.polymul(
            self.density, self.specific_heat
        )
        antiderivative = np.polynomial.polynomial.polyint(coefficients)
        return float(
            np.polynomial.polynomial.polyval(upper, antiderivative)
            - np.polynomial.polynomial.polyval(lower, antiderivative)
        )

    def interface_density(
        self, other: "PolynomialProperties", temperature: float
    ) -> float:
        return float(0.5 * (self.rho(temperature) + other.rho(temperature)))


AMORPHOUS = PolynomialProperties(
    conductivity=(0.88090, -0.0013984, 5.8197e-7),
    specific_heat=(904.35, 0.65314),
    density=(2070.0, -0.7),
)
CRYSTALLINE = PolynomialProperties(
    conductivity=(0.050242, 0.00061420),
    specific_heat=(514.98, 1.5629),
    density=(2119.0, 0.792, -2.105e-3),
)


def interface_density() -> float:
    """Density used by the paper in the phase-transition latent heat term."""
    return AMORPHOUS.interface_density(CRYSTALLINE, TM)


def crystalline_sensible_energy(temperature: float) -> float:
    return CRYSTALLINE.volumetric_enthalpy(T0, temperature)


def amorphous_energy_denominator(temperature: float) -> float:
    sensible_crystalline = crystalline_sensible_energy(TM)
    latent = interface_density() * HM
    sensible_amorphous = AMORPHOUS.volumetric_enthalpy(TM, temperature)
    return sensible_amorphous + sensible_crystalline + latent


@lru_cache(maxsize=None)
def amorphous_depth(
    temperature: float,
    velocity: float = V,
    surface_temperature: float = TS,
) -> float:
    """Global depth x(T) in the amorphous region, equation (3.2-13)."""
    if not TM <= temperature <= surface_temperature:
        raise ValueError(
            f"amorphous temperature must be in [{TM}, {surface_temperature}] K"
        )
    integral, _ = quad(
        lambda value: AMORPHOUS.k(value) / amorphous_energy_denominator(value),
        temperature,
        surface_temperature,
        epsabs=1e-14,
        epsrel=2e-13,
    )
    return integral / velocity


@lru_cache(maxsize=None)
def interface_depth(
    velocity: float = V, surface_temperature: float = TS
) -> float:
    """Amorphous-layer thickness delta_m, equation (3.2-15)."""
    return amorphous_depth(TM, velocity, surface_temperature)


@lru_cache(maxsize=None)
def crystalline_depth(temperature: float, velocity: float = V) -> float:
    """Depth z(T) measured behind the phase plane, equation (3.2-6b)."""
    if not T0 < temperature <= TM:
        if temperature == T0:
            return np.inf
        raise ValueError(f"crystalline temperature must be in ({T0}, {TM}] K")
    integral, _ = quad(
        lambda value: CRYSTALLINE.k(value) / crystalline_sensible_energy(value),
        temperature,
        TM,
        epsabs=1e-14,
        epsrel=2e-13,
    )
    return integral / velocity


def temperature(
    depth: float,
    velocity: float = V,
    surface_temperature: float = TS,
) -> float:
    """Invert the analytical depth-temperature relation for Figures 6 and 7."""
    if depth < 0.0:
        raise ValueError("depth must be nonnegative")
    if surface_temperature < TM:
        raise ValueError("surface temperature must not be below the phase temperature")
    delta = interface_depth(velocity, surface_temperature)
    if depth <= delta:
        if depth == 0.0:
            return surface_temperature
        if depth == delta:
            return TM
        return brentq(
            lambda value: amorphous_depth(
                value, velocity, surface_temperature
            ) - depth,
            TM,
            surface_temperature,
            xtol=2e-12,
            rtol=1e-14,
        )

    target = depth - delta
    # Below this offset the profile is indistinguishable from T0 at plotting
    # precision; avoiding a smaller offset also avoids integrating directly
    # into the logarithmic far-field singularity in x(T).
    lower = T0 + 1e-6
    if target >= crystalline_depth(lower, velocity):
        return T0
    return brentq(
        lambda value: crystalline_depth(value, velocity) - target,
        lower,
        TM,
        xtol=2e-12,
        rtol=1e-14,
    )


def conductive_heat_flux(temperature: float, *, phase: str) -> float:
    """Return inward conductive heat flux -k dT/dx from the first integrals."""
    if phase == "crystalline":
        return V * crystalline_sensible_energy(temperature)
    if phase == "amorphous":
        return V * amorphous_energy_denominator(temperature)
    raise ValueError("phase must be 'amorphous' or 'crystalline'")


def constant_property_temperature(
    depth,
    *,
    surface_temperature: float,
    initial_temperature: float,
    velocity: float,
    conductivity: float,
    density: float,
    specific_heat: float,
):
    """Constant-property limit, equation (2.3-12d)."""
    depth = np.asarray(depth)
    exponent = -velocity * density * specific_heat * depth / conductivity
    return initial_temperature + (surface_temperature - initial_temperature) * np.exp(
        exponent
    )
