import numpy as np

from compare_solutions import calculate_error_metrics, compare_case, generate_report


def test_error_metric_definitions_for_known_arrays():
    reference = np.array([100.0, 200.0, 300.0])
    candidate = np.array([101.0, 198.0, 303.0])

    metrics = calculate_error_metrics(candidate, reference)

    assert metrics.max_absolute_K == 3.0
    np.testing.assert_allclose(metrics.rmse_K, np.sqrt(14.0 / 3.0))
    assert metrics.max_relative_percent == 1.0
    np.testing.assert_allclose(
        metrics.normalized_rmse_percent, np.sqrt(14.0 / 3.0) / 200.0 * 100.0
    )


def test_figure_6_finite_difference_error_is_small_and_explicitly_bounded():
    comparison = compare_case(surface_temperature=950.0, maximum_depth=0.005)
    metrics = comparison["finite_difference"]

    assert metrics.max_absolute_K < 0.1
    assert metrics.rmse_K < 0.02
    assert metrics.max_relative_percent < 0.01


def test_figure_7_finite_difference_errors_are_small_for_all_three_curves():
    for surface_temperature in (900.0, 950.0, 1000.0):
        metrics = compare_case(
            surface_temperature=surface_temperature, maximum_depth=0.002
        )["finite_difference"]

        assert metrics.max_absolute_K < 0.2
        assert metrics.rmse_K < 0.02
        assert metrics.max_relative_percent < 0.02


def test_machine_readable_comparison_report_is_generated(tmp_path):
    output = generate_report(tmp_path / "metrics.json")

    assert output.is_file()
    text = output.read_text()
    assert "figure6_Ts_950K" in text
    assert "figure7_Ts_1000K" in text
    assert "normalized_rmse_percent" in text


def test_continuous_reference_matches_analytical_solution_to_solver_tolerance():
    # Unlike the lower-order finite-difference comparison, this adaptive direct
    # ODE solve should agree down to its requested numerical tolerance.  A
    # floating-point algebra test at 1e-14 would overstate differential-solver
    # accuracy, so the bound is tied to the 1e-8 BVP tolerance instead.
    for surface_temperature in (900.0, 950.0, 1000.0):
        comparison = compare_case(
            surface_temperature=surface_temperature, maximum_depth=0.002
        )
        metrics = comparison["continuous_reference"]

        assert metrics.max_absolute_K < 2e-8
        assert metrics.rmse_K < 5e-9
