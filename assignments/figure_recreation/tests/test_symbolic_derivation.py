import sympy as sp

from symbolic_derivation import derive


def test_first_integral_differentiates_to_governing_equation():
    result = derive()

    assert sp.simplify(result["first_integral_derivative"] - result["governing_ode"]) == 0


def test_interface_balance_reduces_to_latent_flux_jump():
    result = derive()

    assert sp.simplify(result["interface_balance"]) == 0


def test_polynomial_enthalpy_differentiates_to_rho_cp():
    result = derive()

    assert result["polynomial_residual"] == 0
    assert sp.Poly(
        result["volumetric_polynomial"], result["polynomial_variable"]
    ).degree() == 4
