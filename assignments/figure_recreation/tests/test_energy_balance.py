import numpy as np

from kato_matsuda import (
    AMORPHOUS,
    CRYSTALLINE,
    HM,
    TM,
    V,
    conductive_heat_flux,
    interface_density,
)


def test_interface_flux_jump_equals_latent_heat_rate():
    flux_amorphous = conductive_heat_flux(TM, phase="amorphous")
    flux_crystalline = conductive_heat_flux(TM, phase="crystalline")

    expected_jump = V * interface_density() * HM
    np.testing.assert_allclose(
        flux_amorphous - flux_crystalline, expected_jump, rtol=3e-14
    )


def test_temperature_gradient_is_negative_in_both_phases():
    for temperature, phase, properties in [
        (800.0, "amorphous", AMORPHOUS),
        (450.0, "crystalline", CRYSTALLINE),
    ]:
        flux = conductive_heat_flux(temperature, phase=phase)
        gradient = -flux / properties.k(temperature)

        assert flux > 0.0
        assert gradient < 0.0
