import numpy as np

from kato_matsuda import TM, interface_depth, temperature
from plots.plot_figure7 import plot_figure_7


SURFACE_TEMPERATURES = (900.0, 950.0, 1000.0)


def test_amorphous_layer_thickness_increases_with_surface_temperature():
    thicknesses = [
        interface_depth(surface_temperature=value) for value in SURFACE_TEMPERATURES
    ]

    assert thicknesses[0] < thicknesses[1] < thicknesses[2]


def test_figure_7_profiles_obey_boundaries_and_ordering():
    for surface_temperature in SURFACE_TEMPERATURES:
        delta = interface_depth(surface_temperature=surface_temperature)
        assert temperature(0.0, surface_temperature=surface_temperature) == surface_temperature
        np.testing.assert_allclose(
            temperature(delta, surface_temperature=surface_temperature), TM, atol=1e-10
        )

    for depth in (0.0002, 0.0008, 0.0015):
        values = [
            temperature(depth, surface_temperature=value)
            for value in SURFACE_TEMPERATURES
        ]
        assert values[0] < values[1] < values[2]


def test_local_crystalline_profiles_are_translation_invariant():
    local_depth = 0.001
    values = []
    for surface_temperature in SURFACE_TEMPERATURES:
        global_depth = (
            interface_depth(surface_temperature=surface_temperature) + local_depth
        )
        values.append(
            temperature(global_depth, surface_temperature=surface_temperature)
        )

    np.testing.assert_allclose(values, values[1], rtol=0.0, atol=2e-10)


def test_figure_7_plot_is_generated(tmp_path):
    output = tmp_path / "figure7.png"

    thicknesses = plot_figure_7(output)

    assert output.is_file()
    assert output.stat().st_size > 20_000
    assert list(thicknesses) == sorted(thicknesses)
