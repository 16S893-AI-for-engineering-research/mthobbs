import numpy as np

from finite_difference import figure_6_finite_difference
from kato_matsuda import TM, TS, T0, interface_depth, temperature


def test_finite_difference_solution_satisfies_boundaries_and_is_monotone():
    solution = figure_6_finite_difference(amorphous_nodes=61, crystalline_nodes=501)

    assert solution.amorphous_temperature[0] == TS
    assert solution.amorphous_temperature[-1] == TM
    assert solution.crystalline_temperature[0] == TM
    assert solution.crystalline_temperature[-1] == T0
    assert np.all(np.diff(solution.amorphous_temperature) < 0.0)
    # The far field reaches T0 to machine precision, so equality is admissible.
    assert np.all(np.diff(solution.crystalline_temperature) <= 1e-10)
    assert np.all(solution.crystalline_temperature >= T0 - 1e-10)


def test_finite_difference_solution_agrees_with_independent_analytical_solution():
    solution = figure_6_finite_difference(amorphous_nodes=81, crystalline_nodes=1001)
    sample_depths = np.array(
        [0.0001, 0.0004, interface_depth(), 0.001, 0.002, 0.004]
    )
    numerical = solution.temperature_at(sample_depths)
    analytical = np.array([temperature(depth) for depth in sample_depths])

    np.testing.assert_allclose(numerical, analytical, atol=0.15)
