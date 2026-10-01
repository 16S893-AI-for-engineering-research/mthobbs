import numpy as np
import pytest

from kato_matsuda import AMORPHOUS, CRYSTALLINE, TM, TS, T0


@pytest.mark.parametrize(
    ("properties", "temperature_range"),
    [(AMORPHOUS, (TM, TS)), (CRYSTALLINE, (T0, TM))],
)
def test_material_properties_remain_positive_over_model_domain(
    properties, temperature_range
):
    temperatures = np.linspace(*temperature_range, 101)

    assert np.all(properties.k(temperatures) > 0.0)
    assert np.all(properties.cp(temperatures) > 0.0)
    assert np.all(properties.rho(temperatures) > 0.0)


def test_phase_transition_density_is_arithmetic_interface_average():
    expected = 0.5 * (AMORPHOUS.rho(TM) + CRYSTALLINE.rho(TM))

    assert AMORPHOUS.interface_density(CRYSTALLINE, TM) == expected
