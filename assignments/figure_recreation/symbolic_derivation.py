"""Exact symbolic checks for the Kato--Matsuda first integral and interface balance."""

from __future__ import annotations

import sympy as sp


def derive() -> dict[str, sp.Expr]:
    """Return exact identities underlying equations (3.2-6) and (3.2-13)."""
    x = sp.symbols("x", real=True)
    velocity, latent_heat, rho_m = sp.symbols("V h_m rho_m", positive=True)
    temperature = sp.Function("T")(x)
    conductivity = sp.Function("k")
    volumetric_heat_capacity = sp.Function("c_v")
    enthalpy = sp.Function("H")

    gradient = sp.diff(temperature, x)
    governing_ode = sp.diff(conductivity(temperature) * gradient, x) + (
        velocity * volumetric_heat_capacity(temperature) * gradient
    )
    first_integral_derivative = sp.diff(
        conductivity(temperature) * gradient + velocity * enthalpy(temperature), x
    ).subs(sp.diff(enthalpy(temperature), temperature), volumetric_heat_capacity(temperature))

    crystalline_flux = sp.symbols("q_c", real=True)
    amorphous_flux = crystalline_flux + velocity * rho_m * latent_heat
    interface_balance = sp.expand(
        amorphous_flux - crystalline_flux - velocity * rho_m * latent_heat
    )

    theta, reference, evaluation = sp.symbols("u T_r T", real=True)
    rho0, rho1, rho2, cp0, cp1, cp2 = sp.symbols(
        "rho_0 rho_1 rho_2 C_p0 C_p1 C_p2", real=True
    )
    density_polynomial = rho0 + rho1 * theta + rho2 * theta**2
    heat_capacity_polynomial = cp0 + cp1 * theta + cp2 * theta**2
    volumetric_polynomial = sp.expand(
        density_polynomial * heat_capacity_polynomial
    )
    polynomial_enthalpy = sp.integrate(
        volumetric_polynomial, (theta, reference, evaluation)
    )
    polynomial_residual = sp.expand(
        sp.diff(polynomial_enthalpy, evaluation)
        - volumetric_polynomial.subs(theta, evaluation)
    )

    return {
        "governing_ode": governing_ode,
        "first_integral_derivative": first_integral_derivative,
        "interface_balance": interface_balance,
        "polynomial_variable": theta,
        "volumetric_polynomial": volumetric_polynomial,
        "polynomial_enthalpy": polynomial_enthalpy,
        "polynomial_residual": polynomial_residual,
    }


if __name__ == "__main__":
    result = derive()
    print("Governing quasi-steady equation:")
    print("  0 =", result["governing_ode"])
    print("\nDerivative of first integral:")
    print("  ", result["first_integral_derivative"])
    print("\nInterface balance residual:")
    print("  ", result["interface_balance"])
    print("\nPolynomial volumetric enthalpy:")
    print("  H(T; T_r) =", result["polynomial_enthalpy"])
    print("\nPolynomial differentiation residual:")
    print("  ", result["polynomial_residual"])
