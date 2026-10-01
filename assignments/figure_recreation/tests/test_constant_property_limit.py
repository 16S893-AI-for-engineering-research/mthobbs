import numpy as np

from kato_matsuda import constant_property_temperature


def test_constant_property_solution_has_exponential_round_trip():
    surface_temperature = 900.0
    initial_temperature = 300.0
    velocity = 8.0e-5
    conductivity = 0.3
    density = 2000.0
    specific_heat = 1000.0
    depths = np.linspace(0.0, 0.004, 21)

    values = constant_property_temperature(
        depths,
        surface_temperature=surface_temperature,
        initial_temperature=initial_temperature,
        velocity=velocity,
        conductivity=conductivity,
        density=density,
        specific_heat=specific_heat,
    )
    recovered_depths = -conductivity / (velocity * density * specific_heat) * np.log(
        (values - initial_temperature) / (surface_temperature - initial_temperature)
    )

    np.testing.assert_allclose(recovered_depths, depths, atol=2e-17)
