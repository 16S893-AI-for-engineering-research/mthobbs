# Numerical tests worth keeping

Exercise an interface that callers depend on. Test a numerical kernel directly
when it has its own mathematical contract; also test how it is used in the larger
workflow. Avoid private caches, helper-call order, and exact iteration counts
unless those are part of a documented contract.

## Independent expectations

Choose the expectation before inspecting the implementation's output:

- Analytical or manufactured solutions for discretizations and solvers.
- Conservation or symmetry under the assumptions that imply it.
- Limiting cases, such as zero forcing or an identity transformation.
- Grid or time-step refinement within the method's convergence regime.
- Reference data with source, version, units, configuration, and uncertainty.

A saved result is useful for regression, but is not independent evidence of physical
correctness. Do not label an unexplained constant a published reference.

## Small exact case

This runnable Python example uses NumPy and pytest to test a linear solve against a
hand-solved system. In a project, import the solver being developed instead of
`numpy.linalg.solve`.

```python
import numpy as np
from numpy.linalg import solve


def test_two_equation_solution():
    # 3*x + y = 5; x + 2*y = 5. Exact solution: x=1, y=2.
    matrix = np.array([[3.0, 1.0], [1.0, 2.0]])
    rhs = np.array([5.0, 5.0])
    actual = solve(matrix, rhs)
    assert np.isfinite(actual).all()
    # A small, well-conditioned float64 system: allow accumulated roundoff.
    np.testing.assert_allclose(actual, [1.0, 2.0], rtol=1e-14, atol=1e-14)
```

Checking `matrix @ actual` against `rhs` is an additional residual check, not a
replacement for a solution-error check on ill-conditioned systems.

## Refinement check

The following is an interface sketch, not a bundled solver. It assumes the project
provides `integrate_decay(rate, initial, end_time, step)` returning the final scalar
for `dy/dt = -rate*y`, with time in seconds and rate in inverse seconds. This test
is appropriate only if first-order accuracy is part of the chosen method's contract.

```python
import math
from myproject import integrate_decay


def test_decay_first_order_refinement():
    exact = math.exp(-1.0)  # y(0)=1, rate=1 s^-1, end_time=1 s
    errors = [
        abs(integrate_decay(rate=1.0, initial=1.0, end_time=1.0, step=h) - exact)
        for h in (0.02, 0.01, 0.005)
    ]
    assert all(math.isfinite(e) and e > 0 for e in errors)
    # Error should roughly halve when h halves in this asymptotic regime.
    assert all(1.8 < a / b < 2.2 for a, b in zip(errors, errors[1:]))
```

Establish a suitable refinement range with analysis or a documented study. Once
roundoff, solver tolerances, or discontinuities dominate, an order check may not
apply. Changing the method can legitimately require changing this contract test.

## Tolerances

For a comparison of actual `a` with reference `b`, many tools use a bound like
`abs(a - b) <= atol + rtol * abs(b)`. Check the chosen library's exact definition.

- `atol` has the units of the compared quantity; it matters near zero.
- `rtol` is dimensionless; choose it for the scale and accuracy of the problem.
- Scale vector components deliberately when they have different units or magnitudes.
- Check NaN and infinity explicitly when they are invalid. A matching NaN is not
  evidence of agreement.
- Base tolerances on an error budget. Neither an analytical reference nor an
  iterative method determines a universal tolerance by itself.
- Fixing a random seed does not guarantee bitwise results across library versions,
  hardware, or parallel reduction orders. Test the appropriate statistical property.

## Failures and references

Test invalid units or shapes, singular systems, nonconvergence, and missing data
where the interface promises a specific response. A convergence flag alone is not
proof of an accurate result; inspect the returned solution and documented diagnostics.

For observational comparisons, account for measurement uncertainty, calibration,
and the model's range of validity. Keep slow validation studies separate from fast
unit tests, but include a small real end-to-end case in routine checks.
