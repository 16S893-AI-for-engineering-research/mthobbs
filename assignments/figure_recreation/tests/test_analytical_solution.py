import numpy as np

from kato_matsuda import (
    TM,
    TS,
    T0,
    amorphous_depth,
    crystalline_depth,
    interface_depth,
    temperature,
)


def test_figure_6_interface_depth_matches_reported_value():
    np.testing.assert_allclose(interface_depth(), 0.64e-3, atol=0.01e-3)


def test_depth_temperature_maps_satisfy_boundary_conditions():
    assert amorphous_depth(TS) == 0.0
    np.testing.assert_allclose(amorphous_depth(TM), interface_depth(), rtol=2e-13)
    assert crystalline_depth(TM) == 0.0


def test_temperature_is_continuous_at_phase_interface():
    delta = interface_depth()

    np.testing.assert_allclose(temperature(0.0), TS, atol=2e-10)
    np.testing.assert_allclose(temperature(delta), TM, atol=2e-10)
    np.testing.assert_allclose(temperature(0.05), T0, atol=1e-6)


def test_temperature_decreases_monotonically_with_depth():
    depths = np.linspace(0.0, 0.005, 251)
    temperatures = np.array([temperature(depth) for depth in depths])

    assert np.all(np.diff(temperatures) < 0.0)
    assert np.all((T0 < temperatures) & (temperatures <= TS))


def test_velocity_length_scaling_leaves_temperature_unchanged():
    """The quadrature contains x only through V*x."""
    depths = np.array([0.0, 0.0002, 0.0006, 0.0015, 0.004])
    scale = 3.7

    baseline = np.array([temperature(x) for x in depths])
    rescaled = np.array([temperature(x / scale, velocity=scale * 7.5545e-5) for x in depths])

    np.testing.assert_allclose(rescaled, baseline, rtol=2e-11, atol=2e-9)
